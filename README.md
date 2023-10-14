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

Now that you have your bot token, proceed with setting up the Telegram Git Commit Bot:

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

4. Install the required Python packages:

   ```markdown
   pip install -r requirements.txt
   ```

5. Create a `.env` file with your configuration. Use the provided template and replace placeholders with your bot token and other information:

   ```markdown
   TOKEN=YOUR_BOT_TOKEN
   CHAT_ID=YOUR_CHAT_ID
   REFRESH_DELAY=5
   REPOSITORY_PATH=YOUR_GIT_REPOSITORY_PATH
   LAST_COMMIT_DATE=2023-10-14 16:34:03
   ```

6. Save the `.env` file.

## Obtaining Your Chat ID

To send messages from the Telegram Git Commit Bot to your chat, you need to find your chat ID:

1. **Open Telegram:** Use the Telegram app or [Telegram Web](https://web.telegram.org/).

2. **Start a Chat with Chat ID Bot:** Search for "Chat ID Bot" or use [this link](https://t.me/chatid_bot). Start a chat with the Chat ID Bot.

3. **Get Your Chat ID:** The Chat ID Bot will provide your unique chat or channel `CHAT_ID`, typically in a negative format (e.g., `-1001234567890`).

4. **Copy Your CHAT_ID:** Copy the obtained `CHAT_ID` and paste it into the `.env` file in your Python script.

   ```markdown
   CHAT_ID=YOUR_CHAT_ID
   ```

## Usage

To use the Telegram Git Commit Bot, follow these steps:

1. Ensure your virtual environment is activated.

2. Run the bot script:

   ```markdown
   python bot.py
   ```

The bot will start running and checking for new commits in your Git repository. It will send updates to your specified Telegram chat whenever there's a new commit.

## Commands

The bot responds to the following commands in the Telegram chat:

- `/ping`: Sends a "pong" response to check the bot's availability.
- `/cat`: Allows you to view the content of a file in the Git repository.
- `/setdelay`: Modifies the refresh delay for checking commits.
- `/ls`: Lists the contents of a specified directory in the Git repository.
- `/help`: Displays a help message with a list of available commands.

## Troubleshooting

If you encounter any issues while using the bot, make sure to check the following:

- The `.env` file contains the correct values for `TOKEN`, `CHAT_ID`, `REFRESH_DELAY`, `REPOSITORY_PATH`, and `LAST_COMMIT_DATE`.

- Your Git repository path is correct and accessible from the script location.

- Your virtual environment is activated when running the bot.

- You have installed the required Python packages as specified in the installation steps.

The Telegram Git Commit Bot is a useful tool for staying updated on your Git repository's commits and changes. Enjoy using it to streamline your development workflow.
