# github-commit-updater

# Telegram Git Commit Bot

The Telegram Git Commit Bot is a Python script that monitors a Git repository and sends updates to a Telegram chat whenever a new commit is made. This README provides instructions on how to install and use the bot.

## Prerequisites

Before you can use the Telegram Git Commit Bot, you'll need to have the following:

1. **Telegram Account:** You'll need a Telegram account to create a bot and receive notifications.

2. **Git Repository:** You should have a Git repository that you want to monitor. Make sure you have the repository URL handy.

3. **Python Environment:** The bot is written in Python, so you should have Python installed on your system. You can download Python from [Python's official website](https://www.python.org/downloads/).

Sure, here's a tutorial on how to create a Telegram bot:

## Creating a Telegram Bot

To create a Telegram bot, you'll need to interact with the BotFather, a Telegram bot that helps you create and manage other bots. Follow these steps to create your own bot:

1. **Open Telegram:** Ensure you have the Telegram app installed on your device or use the [Telegram Web](https://web.telegram.org/) version.

2. **Search for the BotFather:** Open Telegram and use the search bar to find the "BotFather" bot. You can do this by searching for "@BotFather."

3. **Start a Chat:** Once you find the BotFather, start a chat with it by clicking on the "Start" button.

4. **Create a New Bot:** To create a new bot, you need to send the command `/newbot` to the BotFather. Type `/newbot` and follow the on-screen instructions.

   - **Choose a Name:** You will be asked to choose a name for your bot. This name will be the display name of your bot. Choose a unique and descriptive name.

   - **Choose a Username:** Next, you'll be asked to choose a username for your bot. This username must be unique and end with "bot." For example, if your bot's name is "MyGitCommitBot," your username could be "@MyGitCommitBot." The BotFather will confirm if the username is available.

5. **Bot Created:** Once you successfully create your bot, the BotFather will provide you with a message containing your bot's token. This token is essential for authenticating your bot with the Telegram API and should be kept secret. It will look something like this:

   ```
   Use this token to access the HTTP API:
   1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqr
   ```

6. **Keep Your Token Safe:** Store your bot's token in a safe place. Do not share it publicly or expose it in your code or repositories.

Now that you've created your Telegram bot, you can use the provided token to integrate it with the Telegram Git Commit Bot as described in the previous instructions. The bot will use this token to send messages to your Telegram chat.

## Setting Up the Telegram Bot in Your Code

After creating your Telegram bot and obtaining the bot token, you can use it in your code to send messages to your Telegram chat. Here's how to set up the bot in your code:

1. In your code, replace the `BOT_TOKEN` value in the `.env` file with the token you received from the BotFather:

   ```markdown
   TOKEN=YOUR_BOT_TOKEN
   ```

2. Ensure that the chat ID (`CHAT_ID`) in your `.env` file is set to the chat or channel where you want to receive bot messages. You can create a new chat or use an existing one.

3. Run your bot script. It will use the provided token to authenticate with the Telegram API and start sending messages to the specified chat whenever there's a new Git commit.

That's it! You've successfully created a Telegram bot and integrated it with your Python script to monitor and send updates about Git commits.

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
