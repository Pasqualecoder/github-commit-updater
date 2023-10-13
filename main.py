#!/usr/bin/env python3

import os
import datetime
import time
import threading
import git
import telebot
from dotenv import dotenv_values
from dotenv import set_key

env_data = dotenv_values('.env')
BOT_TOKEN = env_data['TOKEN']
chat_id = env_data['CHAT_ID']
refresh_delay = int(env_data['REFRESH_DELAY'])
repository_path = env_data['REPOSITORY_PATH']
last_commit_date = env_data['LAST_COMMIT_DATE']


bot = telebot.TeleBot(BOT_TOKEN)

print("I'm alive!")
bot.send_message(chat_id, "I'm alive!")


def start_commit_updater():
    # Esegui la funzione in un thread separato
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
        result = g.pull()
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


# Gestore per il comando /ping
@bot.message_handler(commands=['ping'])
def ping_pong(message):
    bot.send_message(message.chat.id, "pong")


start_commit_updater()
bot.polling(interval=5)
