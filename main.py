import os
import datetime
import time
import threading
import mimetypes
import git
import telebot
from dotenv import dotenv_values
from dotenv import set_key

# BOT SETUP
env_data = dotenv_values('.env')
BOT_TOKEN = env_data['TOKEN']
chat_id = env_data['CHAT_ID']
refresh_delay = int(env_data['REFRESH_DELAY'])
repository_path = env_data['REPOSITORY_PATH']
last_commit_date = env_data['LAST_COMMIT_DATE']
bot = telebot.TeleBot(BOT_TOKEN)
bot.send_message(chat_id, "I'm alive!")


# log to console
def log(val):
    print("[" + datetime.datetime.now().isoformat() + "] " + str(val))


def start_commit_updater():
    # run check_commit() in a separate thread
    periodic_thread = threading.Thread(target=check_commit)
    periodic_thread.daemon = True
    periodic_thread.start()
    return


def check_commit():
    global last_commit_date
    repo_dir = repository_path
    g = git.cmd.Git(repo_dir)
    repo = git.Repo(repo_dir)  # create git repo object to work on
    master = repo.head.reference
    repo_name = repo.remotes.origin.url.split('.git')[0].split('/')[-1]

    while True:
        try:
            result = g.pull()
        except Exception as failed_commit:
            print(failed_commit)
            time.sleep(refresh_delay)
            continue

        commit_date = datetime.datetime.fromtimestamp(master.commit.committed_date)
        commit_message = master.commit.message
        commit_author = master.commit.author.name

        # new commit
        if str(commit_date) != str(last_commit_date):
            bot.send_message(chat_id, "Last commit in " + repo_name + "\nTitle: " + commit_message + "  " "\nBy: " +
                             commit_author + "\nDate: " + str(commit_date))
            bot.send_message(chat_id, result)
            last_commit_date = commit_date
            set_key('.env', "LAST_COMMIT_DATE", str(last_commit_date))
        time.sleep(refresh_delay)


# /ping command handler
@bot.message_handler(commands=['ping'])
def ping_pong(message):
    bot.send_message(message.chat.id, "pong")


# /cat command handler
@bot.message_handler(commands=['cat'])
def cat_file(message):
    try:
        file_path = message.text.split()[1]  # get file_path
        file_path = repository_path + "/" + file_path
        if len(file_path) < 2:
            response = "Meow, specify the full path to the file in the repo"

        # check if the file exists
        elif not os.path.exists(file_path):
            response = "The file doesn't exist"

        else:
            # get the MIME type of the file (_ ignores the rest of the result)
            mime_type, _ = mimetypes.guess_type(file_path)

            # check if the MIME type is a text type
            if mime_type and mime_type.startswith('text'):
                # writes the file into the message text
                with open(file_path, 'r') as filereader:
                    response = filereader.read()
            else:
                response = "This is not a plain text file and cannot be displayed."

    except Exception as read_file_error:
        response = "An error occurred: " + str(read_file_error)
        log(response)

    bot.reply_to(message, response)


if __name__ == '__main__':
    log("I'm alive!")
    start_commit_updater()

    while True:
        try:
            bot.polling(interval=5)
        except Exception as connection_timeout:
            print(str(datetime.datetime) + str(connection_timeout))
            time.sleep(refresh_delay)
