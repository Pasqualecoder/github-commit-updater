import os
import subprocess
import datetime
import pwd


# Input function with validation
def get_input(prompt, validation_func):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print("Invalid input. Please try again.")
def get_user() -> str:
    try: 
        return pwd.getpwuid(os.stat(os.getcwd()).st_uid).pw_name
    except Exception as e:
        print(f"Error getting user: {e}")
        return os.getlogin()  

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


def edit_service_config():
    try:
        if subprocess.run(['sudo','cp', 'service_template.conf', 'github-commit-updater.service'], check=True):
             print("Error copying service config template, aborting...")
             return 1
        with open('github-commit-updater.service', 'r') as service_file:
            service_data = service_file.read()
        #setting the working directory to the current directory
        service_data = service_data.replace('WorkingDirectory=', f'WorkingDirectory={os.getcwd()}')
        service_data = service_data.replace('User=', f'User={os.getlogin if os.getlogin() in os.getcwd else get_user()}')   
        service_data = service_data.replace('ExecStart=', f'ExecStart={os.getcwd()}/venv/bin/python3 -m main')
        with open('github-commit-updater.service', 'w') as service_file:
            service_file.write(service_data)
    except Exception as e:
        print(f"Error editing service config: {e}")
        return 1
     


def install_service():
     try:
        #check if systemd is installed
          checkpkg =  subprocess.run(['sudo', 'which', 'systemctl'], check=True, capture_output=True, text=True)
          if checkpkg.returncode != 0 or checkpkg.stdout.strip() != "/usr/bin/systemctl":
                print("systemd not found, installing systemd...")
                subprocess.run(['sudo', 'apt', 'install', 'systemd'], check=True)   
        #check if the service is already installed  
          checkservice = subprocess.run(['sudo', 'systemctl', 'status', 'github-commit-updater.service'], check=True, capture_output=True, text=True) 
          if checkservice.returncode == 0:
                    print("Service already installed, removing...")
                    subprocess.run(['sudo', 'systemctl', 'stop', 'github-commit-updater.service'], check=True)
                    subprocess.run(['sudo', 'systemctl', 'disable', 'github-commit-updater.service'], check=True)
                    subprocess.run(['sudo', 'rm', '/etc/systemd/system/github-commit-updater.service'], check=True)
                    subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
                    subprocess.run(['sudo', 'systemctl', 'reset-failed'], check=True)       
        #check if the service config was edited successfully   
          if   edit_service_config():  
               print("Error editing service config, aborting...")
               return 0
          subprocess.run(['sudo', 'cp', 'github-commit-updater.service', '/etc/systemd/system/github-commit-updater.service'], check=True)
          subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
          subprocess.run(['sudo', 'systemctl', 'enable', 'github-commit-updater.service'], check=True)
          subprocess.run(['sudo', 'systemctl', 'start', 'github-commit-updater.service'], check=True)
          print("Service installed successfully!")
     except subprocess.CalledProcessError as e:
          print(f"Error installing service: {e}")    

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
    installservice = input("Do you want to install the bot as a systemd service? (y/n): ").strip().lower()
    if installservice == 'y':
        install_service()
