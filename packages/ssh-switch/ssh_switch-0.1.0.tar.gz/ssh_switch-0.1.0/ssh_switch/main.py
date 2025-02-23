#!/usr/bin/env python3

import os
import re
import stat
import shutil
import subprocess
import questionary
from pathlib import Path

SSH_DIR = Path.home() / ".ssh"
RECENT_KEYS_FILE = Path.home() / ".ssh_recent_keys"

SSH_ENV_FILE = Path.home() / ".ssh-agent-env"
BASHRC_FILE = Path.home() / ".bashrc"
ZSHRC_FILE = Path.home() / ".zshrc"

def ensure_ssh_agent_auto_start():
    """Ensure SSH agent auto-start is added to shell profile and effective."""
    snippet = '\n# Auto-load ssh-agent environment\nif [ -f ~/.ssh-agent-env ]; then\n    source ~/.ssh-agent-env > /dev/null\nfi\n'

    def add_snippet_if_missing(file_path):
        """Check if the snippet exists in a shell profile and add it if missing."""
        if file_path.exists():
            with open(file_path, "r") as f:
                if snippet.strip() in f.read():
                    return  # Snippet already exists, no changes needed
        with open(file_path, "a") as f:
            f.write(snippet)
        print(f"✅ Added SSH agent auto-start snippet to {file_path}")

    # Add to ~/.bashrc and ~/.zshrc if they exist
    add_snippet_if_missing(BASHRC_FILE)
    add_snippet_if_missing(ZSHRC_FILE)

    # Ensure ~/.ssh-agent-env exists
    if not SSH_ENV_FILE.exists():
        SSH_ENV_FILE.touch()
        print(f"✅ Created {SSH_ENV_FILE} to store ssh-agent environment.")

    # Apply changes immediately
    os.system(f"source {SSH_ENV_FILE} > /dev/null 2>&1")

def find_ssh_agent():
    """Find the full path of ssh-agent."""
    ssh_agent_path = shutil.which("ssh-agent")
    if not ssh_agent_path:
        print("❌ Error: ssh-agent not found in system PATH.")
        exit(1)
    return ssh_agent_path


def is_private_key(file_path):
    """Check if a file is a valid SSH private key."""
    # Skip files with extensions (e.g., .pub files)
    if file_path.suffix:
        return False

    # Check file permissions: should be readable and writable only by the owner (0600)
    try:
        st = os.stat(file_path)
        if st.st_mode & (stat.S_IRWXG | stat.S_IRWXO) == 0:
            return True
    except Exception:
        return False

    return False


def is_valid_ssh_key(file_path):
    """Check if a file is a valid SSH private key using ssh-keygen."""
    try:
        result = subprocess.run(
            ["ssh-keygen", "-y", "-f", str(file_path)],
            capture_output=True,
            text=True
        )
        return result.returncode == 0  # If ssh-keygen succeeds, it's a valid private key
    except Exception:
        return False  # If any error occurs, treat it as invalid

def list_ssh_keys():
    """Find all valid SSH private keys in ~/.ssh using ssh-keygen for verification."""
    private_keys = []

    for file in SSH_DIR.iterdir():
        if file.is_file() and is_private_key(file) and is_valid_ssh_key(file):
            private_keys.append(file)

    return sorted(private_keys)

def load_recent_keys():
    """Load recently used SSH keys from a file."""
    if RECENT_KEYS_FILE.exists():
        with open(RECENT_KEYS_FILE, "r") as f:
            return [Path(line.strip()) for line in f.readlines()]
    return []


def save_recent_key(key_path):
    """Save recently used SSH key to a file."""
    recent_keys = load_recent_keys()

    if key_path in recent_keys:
        recent_keys.remove(key_path)  # Move it to the top

    recent_keys.insert(0, key_path)  # Add as most recent
    recent_keys = recent_keys[:5]  # Keep only the last 5 keys

    with open(RECENT_KEYS_FILE, "w") as f:
        f.writelines(f"{key}\n" for key in recent_keys)


def start_ssh_agent():
    """Start a new ssh-agent and store environment variables in a file."""
    ssh_agent_path = find_ssh_agent()

    # Kill any existing ssh-agent (ignoring errors if it doesn't exist)
    subprocess.run("eval $(ssh-agent -k) > /dev/null 2>&1", shell=True)

    # Start a new ssh-agent and capture its output
    agent_process = subprocess.run(
        [ssh_agent_path, "-s"], capture_output=True, text=True
    )
    agent_output = agent_process.stdout

    # Extract SSH_AUTH_SOCK and SSH_AGENT_PID
    sock_match = re.search(r"SSH_AUTH_SOCK=([^;]+);", agent_output)
    pid_match = re.search(r"SSH_AGENT_PID=([0-9]+);", agent_output)

    if sock_match and pid_match:
        ssh_env_file = Path.home() / ".ssh-agent-env"
        with open(ssh_env_file, "w") as f:
            f.write(f"export SSH_AUTH_SOCK={sock_match.group(1)}\n")
            f.write(f"export SSH_AGENT_PID={pid_match.group(1)}\n")

        print(f"✅ ssh-agent started. Run `source {ssh_env_file}` to use it.")
    else:
        print("❌ Failed to start ssh-agent properly.", file=sys.stderr)
        exit(1)


def switch_ssh_key(key_path):
    """Switch SSH key by removing old keys and adding the new key."""
    key_full_path = str(Path(key_path).resolve())

    # Load SSH Agent environment variables if they exist
    ssh_env_file = Path.home() / ".ssh-agent-env"
    if ssh_env_file.exists():
        with open(ssh_env_file, "r") as f:
            env_lines = f.readlines()
        for line in env_lines:
            key, value = line.strip().split("=")
            os.environ[key] = value.replace('"', '')  # Remove quotes if present

    # Ensure ssh-agent is running
    if not os.environ.get("SSH_AUTH_SOCK"):
        print("❌ ssh-agent is not running.")
        print("\n👉 To activate the SSH agent environment, run the following command:\n")
        print("\033[1;32m source ~/.bashrc \033[0m\n")  # Green bold text
        return


    # Remove all previously added keys
    subprocess.run(["ssh-add", "-D"], capture_output=True, text=True)

    # Add the new SSH key
    result = subprocess.run(["ssh-add", key_full_path], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Switched to SSH key: {key_full_path}")
    else:
        print(f"❌ Failed to add SSH key: {result.stderr.strip()}")


def verify_ssh_agent():
    """Check if ssh-agent is running properly."""
    result = subprocess.run(["ssh-add", "-l"], capture_output=True, text=True)
    if "no identities" in result.stdout.lower():
        print("❌ ssh-agent is running but has no identities loaded.")
    elif result.returncode != 0:
        print(f"❌ Error verifying ssh-agent: {result.stderr}")
    else:
        print("✅ ssh-agent is working correctly.")


def interactive_key_selection():
    """Interactive selection of SSH keys using questionary."""
    all_keys = list_ssh_keys()
    recent_keys = load_recent_keys()

    if not all_keys:
        print("❌ No valid SSH private keys found in ~/.ssh/")
        return None

    choices = []
    for key in recent_keys + [k for k in all_keys if k not in recent_keys]:
        label = f"{key.name} {'*recent' if key in recent_keys else ''}"
        choices.append(questionary.Choice(label, value=key))

    selected_key = questionary.select(
        "Select SSH private key:", choices=choices, use_arrow_keys=True
    ).ask()
    return selected_key


def main():
    """Main function for selecting and switching SSH keys."""
    key_path = interactive_key_selection()

    if key_path:
        switch_ssh_key(key_path)
    else:
        print("❌ No key selected. Exiting.")


if __name__ == "__main__":
    ensure_ssh_agent_auto_start()
    main()
