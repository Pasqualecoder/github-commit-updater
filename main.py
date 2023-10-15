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
env_path = '.env'
env_data = dotenv_values(env_path)
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


# allows to check if refresh_delay has been changed while sleeping
# if it has been changed, dolphin_sleep() will stop
def dolphin_sleep():
    global refresh_delay
    before_delay = refresh_delay
    i = 0
    while i < before_delay == refresh_delay:
        time.sleep(1)
        i += 1


#  if the path wasn't specified returns ""
#  else UNISA/path
def obtain_path(arg: str, old: str) -> str:
    arg = arg.replace(old, "")
    return "" if arg == "" else repository_path + "/" + arg


def start_commit_updater():
    # run check_commit() in a separate thread
    periodic_thread = threading.Thread(target=check_commit)
    periodic_thread.daemon = True
    periodic_thread.start()


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
            dolphin_sleep()
            continue

        print("provo commit")
        print(refresh_delay)

        commit_date = datetime.datetime.fromtimestamp(master.commit.committed_date)
        commit_message = master.commit.message
        commit_author = master.commit.author.name

        # new commit
        if str(commit_date) != str(last_commit_date):
            bot.send_message(chat_id, "Last commit in " + repo_name + "\nTitle: " + commit_message + "  " "\nBy: " +
                             commit_author + "\nDate: " + str(commit_date))
            bot.send_message(chat_id, result)
            last_commit_date = commit_date
            set_key(env_path, "LAST_COMMIT_DATE", str(last_commit_date))
        dolphin_sleep()


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    response = "Ue " + message.from_user.first_name
    bot.reply_to(message, response)


# /ping command handler
@bot.message_handler(commands=['ping'])
def ping_pong(message):
    bot.reply_to(message, "pong")


# /cat command handler
@bot.message_handler(commands=['cat'])
def cat_file(message):
    file_path = ""

    try:
        file_path = obtain_path(message.text, "/cat ")  # get file_path

        # if no path is provided
        if file_path == "":
            response = "Meow! Specify the full path to the file in the repo!"

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
                # open the file in binary mode a send the file as a document
                with open(file_path, 'rb') as file:
                    bot.send_document(message.chat.id, file)
                return

    except Exception as read_file_error:
        log(response)
        response = "Error: " + str(read_file_error)

    response = "I got this path: " + file_path + '\n' + response
    bot.reply_to(message, response)


# /setdelay command handler
@bot.message_handler(commands=['setdelay'])
def set_delay(message):
    global refresh_delay

    try:
        delay = int(message.text.split()[1])
        refresh_delay = delay
        set_key(env_path, "REFRESH_DELAY", str(refresh_delay))
        response = "refresh_delay" + " has been set to " + str(refresh_delay) + " sec or " + str(
            round((delay / 60), 2)) + " min"  # by peppe
    except Exception as convert_error:
        response = "Error: " + str(convert_error)
        log(convert_error)

    bot.reply_to(message, response)


@bot.message_handler(commands=['ls'])  # credt
def ls(message):
    try:
        dir_path = message.text.replace("/ls ", "")  # Correct the path extraction

        if dir_path == "/ls":
            dir_path = repository_path  # Set the root directory path
        else:
            dir_path = repository_path + dir_path.strip()  # Remove leading/trailing spaces

        response = f"ls of {dir_path}\n"

        # check if the path is an existing directory
        if os.path.isdir(dir_path):
            # get a list of all files in the dir
            file_list = os.listdir(dir_path)
            # print the name of each file
            for filename in file_list:
                response += f"{filename}\n"
        else:
            response = "Directory not found."

    except Exception as error:
        response = f"Error: {str(error)}"

    bot.reply_to(message, response)


@bot.message_handler(commands=['help_it'])
def send_help_it(message):
    help_message = """/start - Inizia l'interazione con il bot\n\n/ping - Ottieni una risposta "pong" dal bot per 
    verificare la sua disponibilità.\n\n/cat - Visualizza il contenuto di un file specificato come parametro. Se il 
    file è un file di testo, verrà stampato nel chat, altrimenti verrà inviato come documento.\nUtilizzo: /cat 
    percorsoAlFile\n\n/setdelay - Modifica il ritardo per il controllo dei commit. Imposta un ritardo specifico in 
    millisecondi.\nUtilizzo: /setdelay intero\n\n/ls - Visualizza l'elenco completo del contenuto di una cartella o 
    directory specificata. \nUtilizzo: /ls percorsoCartella, /ls (per visualizzare il contenuto della directory 
    radice).\n\n/help - Visualizza il seguente messaggio\n"""

    bot.reply_to(message, help_message)


@bot.message_handler(commands=['help'])
def send_help_en(message):
    help_message = """/start - Start the interaction with the bot\n\n/ping - Get a "pong" response from the bot to 
    check its availability.\n\n/cat - View the contents of a file specified as a parameter. If the file is a text 
    file, it will be printed in the chat, otherwise it will be sent as a document.\nUsage: /cat pathToFile\n\n/setdelay 
    - Change the delay for checking commits. Set a specific delay in milliseconds.\nUsage: /setdelay integer\n\n/ls - 
    Displays the complete list of the contents of a specified folder or directory. \nUsage: /ls folderPath, /ls (to 
    view the contents of the root directory).\n\n/help - Displays this message\n"""

    bot.reply_to(message, help_message)


if __name__ == '__main__':
    log("I'm alive!")
    start_commit_updater()

    while True:
        try:
            bot.polling(interval=5)
        except Exception as connection_timeout:
            print(str(datetime.datetime) + str(connection_timeout))
            dolphin_sleep()
