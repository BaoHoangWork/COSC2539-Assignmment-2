import os
import subprocess

# Replace setting of misconfigured user
def replace_insecure_sudo_config(target_user, secure_command):
    sudoers_file = "/etc/sudoers"
    insecure_config = f"{target_user} ALL=(ALL) NOPASSWD: ALL"
    secure_config = f"{target_user} ALL=(ALL) {secure_command}\n"

    try:
        with open(sudoers_file, "r") as file:
            lines = file.readlines()
        
        # Replace as new config
        with open(sudoers_file, "w") as file:
            for line in lines:
                if insecure_config in line:
                    file.write(secure_config)
                else:
                    file.write(line)

        print(f"Sudoers configuration for {target_user} updated successfully.")
    except PermissionError:
        print("Permission denied. Run this script as root.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Create group for specific command
def add_secure_sudo_config(target_user, command):
    try:
        secure_config = f"{target_user} ALL=(ALL) {command}\n"
        with open("/etc/sudoers", "a") as file:
            file.write(secure_config)
        print(f"Secure sudoers configuration added for {target_user}.")
    except PermissionError:
        print("Permission denied. Run this script as root.")
    except Exception as e:
        print(f"An error occurred: {e}")

#  Add to group
def add_user_to_group(target_user, group_name):
    try:
        subprocess.run(["groupadd", "-f", group_name], check=True)
        subprocess.run(["usermod", "-aG", group_name, target_user], check=True)
        print(f"User {target_user} added to group {group_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing system command: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    target_user = "user_1" 
    secure_group = "limited_group"
    specific_command = "/usr/bin/apt-get"

    replace_insecure_sudo_config(target_user, specific_command)
    add_user_to_group(target_user, secure_group)
    add_secure_sudo_config(secure_group, specific_command)
