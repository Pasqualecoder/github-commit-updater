# Telegram Git Commit Bot

The Telegram Git Commit Bot is a Python script that monitors a Git repository and sends updates to a Telegram chat whenever a new commit is made. This README provides instructions on how to install and use the bot.

## Prerequisites

Before setting up and using the Telegram Git Commit Bot, you should have the following:

1. **Telegram Account:** You need a Telegram account to create and manage a bot, as well as to receive notifications.

2. **Git Repository:** Ensure that you have a Git repository that you want to monitor. Have the repository URL ready.

3. **Python Environment:** Make sure you have Python installed on your system. If not, you can download it from [Python's official website](https://www.python.org/downloads/).

## Creating a Telegram Bot

Before you proceed with setting up the Telegram Git Commit Bot, you need to create a Telegram bot. Here's how:

1. **Open Telegram:** Use the Telegram app on your device or access [Telegram Web](https://web.telegram.org/).

2. **Search for BotFather:** In Telegram, search for "BotFather," a bot that helps you create and manage other bots.

3. **Start a Chat:** Initiate a chat with BotFather by clicking "Start."

4. **Create a New Bot:** Use the `/newbot` command to create a new bot. Follow the prompts to choose a name and username for your bot. The username must end with "bot" (e.g., `@MyGitCommitBot`).

5. **Get Bot Token:** Upon successful creation, BotFather will provide you with a unique bot token. Keep this token secure.

## Installation

To simplify the installation process, you can use the provided setup script:

1. Clone the repository or download the script to your local machine.

2. Create a virtual environment for the project:

   ```markdown
   python -m venv venv
   ```

3. Activate the virtual environment:

   - **Windows:**
     ```markdown
     venv\Scripts\activate
     ```

   - **macOS and Linux:**
     ```markdown
     source venv/bin/activate
     ```

4. Run the setup script to configure the bot. This script will guide you through setting up the bot by entering the required information, such as your bot token, chat ID, refresh delay, repository path, and the current date and time.

   ```markdown
   python first)setup.py
   ```

   The script will generate an `.env` file with the provided data and, optionally, install the required dependencies.

5. After running the setup script, your bot is ready to use.

## Usage

To use the Telegram Git Commit Bot, run the following command:

```markdown
python main.py
```

The bot will start running and checking for new commits in your Git repository. It will send updates to your specified Telegram chat whenever there's a new commit.

## Commands

The bot responds to the following commands in the Telegram chat:

- `/ping`: Sends a "pong" response to check the bot's availability.
- `/cat`: Allows you to view the content of a file in the Git repository.
- `/setdelay`: Modifies the refresh delay for checking commits.
- `/ls`: Lists the contents of a specified directory in the Git repository.
- `/update`: Manually checks for new commits and sends an update message. If no new commits are available, it will send a "Last update already sent!" message.
- `/help`: Displays a help message with a list of available commands.

## Troubleshooting

If you encounter any issues while using the bot, make sure to check the following:

- The `.env` file contains the correct values for `TOKEN`, `CHAT_ID`, `REFRESH_DELAY`, `REPOSITORY_PATH`, and `LAST_COMMIT_DATE`.

- Your Git repository path is correct and accessible from the script location.

- Your virtual environment is activated when running the bot.

The Telegram Git Commit Bot is a useful tool for staying updated on your Git repository's commits and changes. Enjoy using it to streamline your development workflow.
