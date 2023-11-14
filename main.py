import os
import datetime
import time
import signal
import threading
import mimetypes
import git
import telebot
import logging
from dotenv import dotenv_values
from dotenv import set_key
from telebot import types

# BOT SETUP
env_path = '.env'
env_data = dotenv_values(env_path)
BOT_TOKEN = env_data['TOKEN']
chat_id = env_data['CHAT_ID']
refresh_delay = int(env_data['REFRESH_DELAY'])
repository_path = env_data['REPOSITORY_PATH']
last_commit_date = env_data['LAST_COMMIT_DATE']
bot = telebot.TeleBot(BOT_TOKEN)



class Logger:
    def __init__(self, name, log_file):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def log(self, level, message):
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)

    def close(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)


logger = Logger(__name__, "file_log.log")


# graceful exit
class ProcessKiller:
    kill = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.better_exit)
        signal.signal(signal.SIGTERM, self.brutal_exit)

    def better_exit(self, *args):
        self.kill = True
        status = os.wait()
        bot.send_message(chat_id, f"I'm dead! Status: {status[1]}")
        logger.log("info", "process shutdown with better exit")
        # let process die on while exit

    def brutal_exit(self, *args):
        self.kill = True
        status = os.wait()
        bot.send_message(chat_id, f"I'm dead! Status: {status[1]}")
        logger.log("info", "process shutdown with brutal shutdown")
        exit(0)  # brutal shutdown


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


# FUNCTION NOT USED
"""def find_first(filename: str, dir_name: str) -> str:
    result = ""
    if os.path.exists(filename):
        return os.path.relpath(filename, os.path.abspath(
            repository_path))  # todo: change the relpath start argument to be dynamic
    else:
        list_dir = list(path_names.name for path_names in os.scandir(dir_name))
        if len(list_dir) == 0:
            return ""
        for dir in list_dir:
            if os.path.isdir(dir_name + "/" + dir):
                previous_list = list_dir[:]
                result = find_first(filename, (dir_name + "/" + dir))
                list_dir = previous_list[:]
                if result:
                    return result
            elif dir == filename:
                treasure = dir_name + "/" + dir
                return os.path.relpath(treasure, os.path.abspath(repository_path))
        return result"""


def find(filename: str, dir_name: str) -> []:
    result = []
    if os.path.exists(filename):
        result += [os.path.relpath(filename, os.path.abspath(repository_path))]
        return result
    else:
        list_dir = list(path_names.name for path_names in os.scandir(dir_name))
        if len(list_dir) == 0:
            return result
        for dir in list_dir:
            if os.path.isdir(dir_name + "/" + dir):
                previous_list = list_dir[:]
                result += find(filename, (dir_name + "/" + dir))
                list_dir = previous_list[:]
            elif dir == filename:
                treasure = dir_name + "/" + dir
                result += [os.path.relpath(treasure, os.path.abspath(repository_path))]
                return result
        return result


def start_commit_updater():
    # run check_commit() in a separate thread
    periodic_thread = threading.Thread(target=check_commit)
    periodic_thread.daemon = True
    periodic_thread.start()


def check_commit():
    global last_commit_date
    repo_dir = repository_path
    g = git.cmd.Git(repo_dir)
    repo = git.Repo(repo_dir)
    master = repo.head.reference
    repo_name = repo.remotes.origin.url.split('.git')[0].split('/')[-1]

    while not killer.kill:
        try:
            my_date = datetime.datetime.now()
            date = my_date.strftime('%Y-%m-%d %H:%M:%S')
            chat_info = bot.get_chat(chat_id)
            pinned_message_id = chat_info.pinned_message.message_id
            bot.edit_message_text(f"Last check: {date}", chat_id, pinned_message_id)
            result = g.pull()
        except Exception as failed_commit:
            logger.log("error", str(failed_commit))
            dolphin_sleep()
            continue

        logger.log("info", "executing check_commit")
        commit_date = datetime.datetime.fromtimestamp(master.commit.committed_date)
        commit_message = master.commit.message
        commit_author = master.commit.author.name

        # New commit
        if str(commit_date) != str(last_commit_date):
            bot.send_message(chat_id, "New commit in " + repo_name + "\nTitle: " + commit_message + "  " "\nBy: " +
                             commit_author + "\nDate: " + str(commit_date))
            if result != "Already up to date.":
                bot.send_message(chat_id, result)
            last_commit_date = commit_date
            set_key(env_path, "LAST_COMMIT_DATE", str(last_commit_date))
        dolphin_sleep()


'''@bot.message_handler(commands=['stop'])
def stop(message):
    logger.log("info", "stopping...")
    bot.reply_to(message, "Stopping...")
    bot.stop_polling()'''


@bot.message_handler(commands=['lastcommit'])
def lastcommit(message):
    logger.log("info", "executing lastcommit")
    repo_dir = repository_path
    repo = git.Repo(repo_dir)
    master = repo.head.reference
    repo_name = repo.remotes.origin.url.split('.git')[0].split('/')[-1]

    commit_date = datetime.datetime.fromtimestamp(master.commit.committed_date)
    commit_message = master.commit.message
    commit_author = master.commit.author.name

    # New commit
    bot.reply_to(message, "Last commit in " + repo_name + "\nTitle: " + commit_message + "  " "\nBy: " +
                 commit_author + "\nDate: " + str(commit_date))


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    logger.log("info", "executing send_welcome")
    response = "Ue " + message.from_user.first_name
    bot.reply_to(message, response)


# /ping command handler
@bot.message_handler(commands=['ping'])
def ping_pong(message):
    logger.log("info", "executing ping_pong")
    bot.reply_to(message, "pong")


@bot.message_handler(commands=['find'])
def start_find(message):
    logger.log("info", "executing start_find")
    # filename = str(message.text.split(" ", 1)[1:])
    # tmp = filename.strip("['")
    # filename = tmp.strip("']")
    filename = message.text.replace("/find ", "")
    filename = filename.strip()

    # finds file in repo recursively (finds the first one with matching name)
    try:
        # if no filename is provided
        if not filename:
            logger.log("warning", "In start_find: no file provided")
            response = "Specify the file to search!"
            bot.reply_to(message, response)
        else:
            res = find(filename, repository_path)
            if not res:
                logger.log("info", "In start_find: no file found")
                response = "File Not found!"
                bot.reply_to(message, response)
            else:
                logger.log("info", "In start_find: 1 or more files found")
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                for x in res:
                    button = types.InlineKeyboardButton(f"{str(x)}", callback_data=f"/cat {str(x)}")
                    keyboard.add(button)
                bot.reply_to(message, "File corrispondenti alla ricerca", reply_markup=keyboard)

    except Exception as e:
        logger.log("error", f"In start_find: {str(e)}")
        return

@bot.callback_query_handler(func=lambda call: call.data)
def find_to_cat(call):
    bot.answer_callback_query(call.id, call.data)


# /cat command handler
@bot.message_handler(commands=['cat'])
def cat_file(message):
    logger.log("info", "Executing cat_file")
    file_path = ""

    try:
        file_path = obtain_path(message.text, "/cat ")  # get file_path
        # if no path is provided
        if file_path == "":
            logger.log("warning", "In cat_file: no path provided")
            response = "Meow! Specify the path or the file in the repo!"

        # check if the file exists
        elif not os.path.exists(file_path):
            logger.log("info", "In cat_file: no file found")
            response = "File Not Found!"

        else:
            logger.log("info", "In cat_file: file found")
            # get the MIME type of the file (_ ignores the rest of the result)
            mime_type, _ = mimetypes.guess_type(file_path)

            # check if the MIME type is a text type
            if mime_type and mime_type.startswith('text'):
                logger.log("info", "In cat_file: file sent as text")
                # writes the file into the message text
                with open(file_path, 'r') as filereader:
                    response = filereader.read()
            else:
                logger.log("info", "In cat_file: file sent as document")
                # open the file in binary mode a send the file as a document
                with open(file_path, 'rb') as file:
                    bot.send_document(message.chat.id, file)
                return

    except Exception as read_file_error:
        logger.log("warning", response)
        logger.log("error", str(read_file_error))
        response = "Error: " + str(read_file_error)

    response = "I got this path: " + file_path + '\n\n' + response
    bot.reply_to(message, response)


# /delay command handler
@bot.message_handler(commands=['delay'])
def set_delay(message):
    global refresh_delay

    logger.log("info", "executing set_delay")
    try:
        delay = int(message.text.split()[1])
        refresh_delay = delay
        set_key(env_path, "REFRESH_DELAY", str(refresh_delay))
        response = "refresh_delay" + " has been set to " + str(refresh_delay) + " sec or " + str(
            round((delay / 60), 2)) + " min"  # by peppe
        logger.log("info", "changed delay to: " + str(delay))

    except Exception as convert_error:
        response = "Error: " + str(convert_error)
        logger.log("error", str(convert_error))

    bot.reply_to(message, response)


@bot.message_handler(commands=['ls'])  # credt
def ls(message):
    logger.log("info", "executing ls")
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
            logger.log("info", "in ls: directory not found")
            response = "Directory not found."

    except Exception as error:
        response = f"Error: {str(error)}"

    bot.reply_to(message, response)


# BUG non funziona quando altre persone mandano messaggi (da testare)
'''
@bot.message_handler(commands=['push'])
def push(message):
    logger.log("info", "executing push")
    dir_path = message.text.replace("/push ", "")
    if dir_path == "/push":
        dir_path = repository_path
    else:

        dir_path = repository_path + dir_path.strip()  # Remove leading/trailing spaces

    logger.log("debug", f"in push: Directory received: {dir_path}")
    if os.path.isdir(dir_path):
        logger.log("debug", f"in push: Directory: {dir_path} Found!")
        markup = types.ForceReply(selective=True)
        bot.reply_to(message, f"Directory {dir_path} found, send the image/document/text to push in the repo",
                     reply_markup=markup)

        # Let's use the msg_to_push function directly instead of registering next step handler
        bot.register_next_step_handler(message, msg_to_push, dir_path, message.from_user.id)
    else:
        bot.reply_to(message, f"Directory {dir_path} not found!")


def msg_to_push(message, dir_path, user_id):
    if message.from_user.id == user_id:  # prima era un if da testare con il while
        content_type = ""
        filename = "None"
        if message.text:
            content_type = "text"
            i = 0
            filename = f"file_{i}.txt"
            while os.path.isfile(f"{dir_path}/{filename}"):
                i += 1
                filename = f"file_{i}.txt"
            try:
                with open(f"{dir_path}/{filename}", "w") as file:
                    file.write(message.text)
                logger.log("info", f"In push: Text message saved as {filename} in {dir_path}")
            except Exception as e:
                logger.log("error", f"In push: Error writing text message: {e}")

            repo = git.Repo(repository_path)
            repo.index.add([f"{dir_path}/{filename}"])

        if message.photo:
            content_type = "photo"
            i = 0
            filename = f"photo_{i}.jpg"
            while os.path.isfile(f"{dir_path}/{filename}"):
                i += 1
                filename = f"photo_{i}.jpg"
            photo = message.photo[-1]
            file_id = photo.file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(dir_path + "/" + filename, 'wb') as new_file:
                try:
                    new_file.write(downloaded_file)
                    logger.log("info", f"In push: Photo saved as {filename} in {dir_path}")
                except Exception as e:
                    logger.log("error", f"In push: Error downloading photo: {e}")

        # FIXME non funziona download non e' la funzione giusta
        if message.document:
            content_type = "document"
            document = message.document
            i = 0
            filename = document.file_name
            while os.path.isfile(f"{dir_path}/{filename}"):
                i += 1
                name, extension = os.path.splitext(filename)
                filename = f"{name}_{i}{extension}"
            file_id = document.file_id
            try:
                bot.get_file(file_id).download(f'{dir_path}/{filename}')  # !!!!!!
                logger.log("info", f"In push: Document saved as {filename} in {dir_path}")
            except Exception as e:
                logger.log("error", f"In push: Error downloading document: {e}")

        logger.log("debug", f"In msg_to_push: Received {content_type} from user {message.from_user.username}")

        commit_message = f"commit from telegram, adding {filename} to {dir_path}"
        try:
            repo = git.Repo(repository_path)
            repo.index.commit(commit_message)
            origin = repo.remote(name='origin')
            origin.push()
            logger.log("info", f"In push: Changes committed and pushed to the repository")
        except Exception as e:
            logger.log("error", f"In push: Error in git commit and push: {e}")
'''

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
    killer = ProcessKiller()
    logger.log('info', "Bot Running!")
    start_commit_updater()

    while not killer.kill:
        try:
            bot.infinity_polling(interval=5)
        except Exception as connection_timeout:
            print(str(datetime.datetime) + str(connection_timeout))
            dolphin_sleep()

    logger.close()
