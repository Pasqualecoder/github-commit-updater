import os
import subprocess
import datetime


# Input function with validation
def get_input(prompt, validation_func):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print("Invalid input. Please try again.")


# Validate token
def validate_token(token):
    return len(token) > 0


# Validate chat ID
def validate_chat_id(chat_id):
    return chat_id.lstrip('-').isdigit()


# Validate directory path
def validate_directory_path(path):
    return os.path.isdir(path)


# Create or update .env file
def create_or_update_env_file():
    bot_token = get_input("Enter your bot token: ", validate_token)
    chat_id = get_input("Enter your chat ID: ", validate_chat_id)
    refresh_delay = input("Enter the refresh delay in seconds (e.g., '5'): ")
    repository_path = get_input("Enter the repository path (e.g., /path/to/repo/): ", validate_directory_path)

    # Add single quotes around refresh_delay, repository_path, and current_date_time
    refresh_delay = f"'{refresh_delay}'"
    repository_path = f"'{repository_path.strip('/')}/'"
    current_date_time = f"'{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'"

    with open('.env', 'w') as env_file:
        env_file.write(f'TOKEN={bot_token}\n')
        env_file.write(f'CHAT_ID={chat_id}\n')
        env_file.write(f'REFRESH_DELAY={refresh_delay}\n')
        env_file.write(f'REPOSITORY_PATH={repository_path}\n')
        env_file.write(f'LAST_COMMIT_DATE={current_date_time}\n')

    print(".env file created successfully!")


def install_dependencies():
    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        print("Please install the required dependencies manually using 'pip install -r requirements.txt'.")


if __name__ == "__main__":
    if os.path.exists('.env'):
        overwrite = input("An .env file already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite == 'y':
            create_or_update_env_file()
    else:
        create_or_update_env_file()

    install = input("Do you want to install required dependencies? (y/n): ").strip().lower()
    if install == 'y':
        install_dependencies()
