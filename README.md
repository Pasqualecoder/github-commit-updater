# github-commit-updater

# Telegram Git Commit Bot

The Telegram Git Commit Bot is a Python script that monitors a Git repository and sends updates to a Telegram chat whenever a new commit is made. This README provides instructions on how to install and use the bot.

## Prerequisites

Before you can use the Telegram Git Commit Bot, you'll need to have the following:

1. **Telegram Account:** You'll need a Telegram account to create a bot and receive notifications.

2. **Git Repository:** You should have a Git repository that you want to monitor. Make sure you have the repository URL handy.

3. **Python Environment:** The bot is written in Python, so you should have Python installed on your system. You can download Python from [Python's official website](https://www.python.org/downloads/).

## Installation

1. Clone the repository or download the script to your local machine.

2. Navigate to the directory containing the script and create a virtual environment for the project:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```
     venv\Scripts\activate
     ```

   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required Python packages by running the following command:

   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file with your configuration. You can use the provided `.env` template and add your Telegram bot token, chat ID, repository path, and refresh delay. Make sure to replace the example values with your own.

   ```
   TOKEN=YOUR_BOT_TOKEN
   CHAT_ID=YOUR_CHAT_ID
   REFRESH_DELAY=5
   REPOSITORY_PATH=YOUR_GIT_REPOSITORY_PATH
   LAST_COMMIT_DATE=2023-10-14 16:34:03
   ```

   - `TOKEN`: Your Telegram bot token (you can create a bot on Telegram and obtain a token).
   - `CHAT_ID`: The chat ID where you want to receive updates (you can create a dedicated channel or group for this purpose).
   - `REFRESH_DELAY`: The refresh delay in seconds (how often the bot checks for new commits).
   - `REPOSITORY_PATH`: The path to your Git repository (relative to the script location).
   - `LAST_COMMIT_DATE`: The last commit date (initially set to a date before your repository's first commit).

6. Save the `.env` file.

## Usage

To use the Telegram Git Commit Bot, follow these steps:

1. Make sure your virtual environment is activated (you should see the environment name in your terminal prompt).

2. Run the bot script:

   ```
   python main.py
   ```

3. The bot will start running and checking for new commits in your Git repository. It will send updates to your specified Telegram chat whenever a new commit is made.

## Commands

The bot responds to the following commands in the Telegram chat:

- `/ping`: Sends a "pong" response to check the bot's availability.
- `/cat`: Allows you to view the content of a file in the Git repository. You can specify the file's path as a parameter.
- `/setdelay`: Modifies the refresh delay for checking commits. Set a new delay in seconds.
- `/ls`: Lists the contents of a specified directory in the Git repository.
- `/help`: Displays a help message with a list of available commands.

## Examples

- To view the content of a file in the repository:
  ```
  /cat path/to/file
  ```

- To change the refresh delay to 10 seconds:
  ```
  /setdelay 10
  ```

- To list the contents of a specific directory:
  ```
  /ls path/to/directory
  ```

## Troubleshooting

If you encounter any issues while using the bot, make sure to check the following:

- The `.env` file contains the correct values for `TOKEN`, `CHAT_ID`, `REFRESH_DELAY`, `REPOSITORY_PATH`, and `LAST_COMMIT_DATE`.

- Your Git repository path is correct and accessible from the script location.

- Your virtual environment is activated when running the bot.

- You have installed the required Python packages as specified in the installation steps.

The Telegram Git Commit Bot is a handy tool for staying updated on your Git repository's commits and changes. Enjoy using it to streamline your development workflow.
