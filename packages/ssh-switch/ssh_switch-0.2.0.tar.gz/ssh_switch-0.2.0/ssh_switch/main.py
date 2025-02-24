#!/usr/bin/env python3

"""
ssh-switch: A CLI tool to manage SSH keys and switch between them easily.

This script provides functionalities for listing SSH keys, switching between them,
and managing the ssh-agent environment.
"""

import os
import sys
import re
import stat
import subprocess
import platform
from pathlib import Path
from collections import OrderedDict
import questionary

SSH_DIR = Path.home() / ".ssh"
RECENT_KEYS_FILE = Path.home() / ".ssh_recent_keys"
SSH_ENV_FILE = Path.home() / ".ssh-agent-env"

BASHRC_FILE = Path.home() / ".bashrc"
ZSHRC_FILE = Path.home() / ".zshrc"

MAX_KEYS_PER_PAGE = 5
ACTIVATION_MESSAGE = False 

def get_os_shell_profile():
    """Return the correct shell profile file based on OS."""
    return ZSHRC_FILE if platform.system() == "Darwin" else BASHRC_FILE

def print_ACTIVATION_MESSAGE():
    """Prints a message to activate the SSH agent environment."""
    print(f"\n 👉 SSH agent is not correctly configured in the terminal session. To fix this, run:\n")
    print(f"\033[1;32m source {get_os_shell_profile()} \033[0m\n")

def ensure_ssh_agent_auto_start():
    """Ensure SSH agent environment is auto-loaded in shell profile."""
    shell_profile = get_os_shell_profile()
    snippet = (
        "\n# Auto-load ssh-agent environment\n"
        "if [ -f ~/.ssh-agent-env ]; then\n"
        "    source ~/.ssh-agent-env > /dev/null\n"
        "fi\n"
    )

    if not shell_profile.exists() or snippet.strip() not in shell_profile.read_text():
        with shell_profile.open("a") as f:
            f.write(snippet)
        print(f"✅ Added SSH agent auto-start snippet to {shell_profile}")

def is_ssh_agent_running():

    global ACTIVATION_MESSAGE

    """Check if ssh-agent is running and export environment variables if needed."""
    if not SSH_ENV_FILE.exists():
        return False

    with SSH_ENV_FILE.open("r") as f:
        env_lines = f.readlines()

    file_ssh_auth_sock, file_ssh_agent_pid = None, None

    for line in env_lines:
        if "SSH_AUTH_SOCK" in line:
            file_ssh_auth_sock = line.strip().split("=")[1].replace('"', "")
        if "SSH_AGENT_PID" in line:
            file_ssh_agent_pid = line.strip().split("=")[1].replace('"', "")

    if not file_ssh_auth_sock or not file_ssh_agent_pid:
        return False

    # Get current terminal environment variables
    env_ssh_auth_sock = os.environ.get("SSH_AUTH_SOCK")
    env_ssh_agent_pid = os.environ.get("SSH_AGENT_PID")

    # Check if the agent process is running
    if subprocess.run(["ps", "-p", file_ssh_agent_pid], capture_output=True).returncode == 0:
        # If the values in the environment and file differ, update them
        if file_ssh_auth_sock != env_ssh_auth_sock or file_ssh_agent_pid != env_ssh_agent_pid:
            ACTIVATION_MESSAGE = True

        return True  # Agent is running and environment is up to date

    return False  # Agent is not running, so we need to start a new one

def start_ssh_agent():
    
    global ACTIVATION_MESSAGE

    """Start ssh-agent only if it's not already running."""
    if is_ssh_agent_running():
        print("✅ ssh-agent is already running.")
        return

    result = subprocess.run(["ssh-agent", "-s"], check=True, text=True, capture_output=True)
    agent_output = result.stdout

    sock_match = re.search(r"SSH_AUTH_SOCK=([^;]+);", agent_output)
    pid_match = re.search(r"SSH_AGENT_PID=([0-9]+);", agent_output)

    if sock_match and pid_match:
        with SSH_ENV_FILE.open("w") as f:
            f.write(f"export SSH_AUTH_SOCK={sock_match.group(1)}\n")
            f.write(f"export SSH_AGENT_PID={pid_match.group(1)}\n")

        os.environ["SSH_AUTH_SOCK"] = sock_match.group(1)
        os.environ["SSH_AGENT_PID"] = pid_match.group(1)

        print("✅ ssh-agent started successfully.")
    else:
        print("❌ Failed to start ssh-agent.")
        sys.exit(1)

    ACTIVATION_MESSAGE = True

def list_ssh_keys():
    """List all valid SSH private keys in ~/.ssh."""
    return sorted(
        file for file in SSH_DIR.iterdir()
        if file.is_file()
        and not file.suffix
        and file.stat().st_mode & (stat.S_IRWXG | stat.S_IRWXO) == 0
        and subprocess.run(
            ["ssh-keygen", "-y", "-f", str(file)], check=False, capture_output=True
            ).returncode == 0
    )

def load_recent_keys():
    """Load recently used SSH keys from a file as strings."""
    if RECENT_KEYS_FILE.exists():
        with open(RECENT_KEYS_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]  # Return strings
    return []

def save_recent_key(key_path):
    """Save recently used SSH key to a file."""
    key_path = str(key_path)  # Ensure key_path is a string
    recent_keys = load_recent_keys()

    if key_path in recent_keys:
        recent_keys.remove(key_path)  # Move it to the top

    recent_keys.insert(0, key_path)  # Add as most recent
    recent_keys = recent_keys[:MAX_KEYS_PER_PAGE]  # Keep only the last 5 keys

    with open(RECENT_KEYS_FILE, "w") as f:
        f.writelines(f"{key}\n" for key in recent_keys)


def switch_ssh_key(key_path):

    global ACTIVATION_MESSAGE
    
    """Switch SSH key by removing old keys and adding the new key."""
    if not is_ssh_agent_running():
        print("❌ ssh-agent is not running.")
        ACTIVATION_MESSAGE = True
        return

    subprocess.run(["ssh-add", "-D"], check=False, capture_output=True)
    result = subprocess.run(
        ["ssh-add", str(Path(key_path).resolve())], check=False, capture_output=True
        )

    if result.returncode == 0:
        print(f"✅ Switched to SSH key: {key_path}")
        save_recent_key(key_path)
    else:
        print(f"❌ Failed to add SSH key: {result.stderr.strip()}")

def verify_ssh_agent():
    """Check if ssh-agent is working correctly."""
    result = subprocess.run(["ssh-add", "-l"], check=False, text=True, capture_output=True)
    if "no identities" in result.stdout.lower():
        print("❌ ssh-agent is running but has no identities loaded.")
    elif result.returncode != 0:
        print(f"❌ Error verifying ssh-agent: {result.stderr.strip()}")
    else:
        print("✅ ssh-agent is working correctly.")

def interactive_key_selection():
    """Interactive selection of SSH keys using left/right arrow pagination."""
    all_keys = list_ssh_keys()  # Get all available keys
    recent_keys = load_recent_keys()  # Get recently used keys

    if not all_keys:
        print("❌ No valid SSH private keys found in ~/.ssh/")
        return None

    all_keys = [Path(key).resolve() for key in all_keys]
    recent_keys = [Path(key).resolve() for key in recent_keys]

    unique_keys = OrderedDict()

    # Add recent keys first (if they exist in all_keys)
    for key in recent_keys:
        if key in all_keys:
            unique_keys[key] = f"{key.name}"

    # Add remaining keys that are not in recent_keys
    for key in all_keys:
        if key not in unique_keys:
            unique_keys[key] = key.name

    key_list = list(unique_keys.items())

    # Pagination setup
    page = 0

    while True:
        start = page * MAX_KEYS_PER_PAGE
        end = start + MAX_KEYS_PER_PAGE
        display_keys = key_list[start:end]

        choices = [
            questionary.Choice(label, value=str(key)) for key, label in display_keys
        ]

        # Add navigation options if there are more pages
        if page > 0:
            choices.insert(0, questionary.Choice("⬅️ Previous", value="prev"))

        if end < len(key_list):
            choices.append(questionary.Choice("➡️ Next", value="next"))

        selected_key = questionary.select(
            "🔑 Select SSH private key:", choices=choices, use_arrow_keys=True
        ).ask()

        if selected_key == "next":
            page += 1  # Go to next page
        elif selected_key == "prev":
            page -= 1  # Go to previous page
        else:
            return selected_key  # Return selected key

def main():
    """Main function to set up ssh-agent and switch keys."""
    ensure_ssh_agent_auto_start()
    start_ssh_agent()

    key_path = interactive_key_selection()
    if key_path:
        switch_ssh_key(key_path)
    else:
        print("❌ No key selected. Exiting.")

    if ACTIVATION_MESSAGE:
        print_ACTIVATION_MESSAGE()  

if __name__ == "__main__":
    main()