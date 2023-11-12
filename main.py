
import os
import datetime
import time
import sys
import signal
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

# graceful exit  
class Process_Killer:
   kill = False
   def __init__(self):
      signal.signal(signal.SIGINT, self.better_exit)
      signal.signal(signal.SIGTERM, self.brutal_exit)
   def better_exit(self, *args):
      self.kill = True
      pid = os.getpid()
      status = os.wait()
      bot.send_message(chat_id,f"I'm dead! Status: {status[1]}")
      # let process die on while exit
   def brutal_exit(self, *args):
      self.kill = True
      pid = os.getpid()
      status = os.wait()
      bot.send_message(chat_id,f"I'm dead! Status: {status[1]}")
      exit(0) # brutal shutdown
     

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



def find_first(filename: str, dir_name: str) -> str:
       result = ""
       if os.path.exists(filename):
            return os.path.relpath(filename,os.path.abspath(repository_path)) #todo: change the relpath start argument to be dynamic 
       else:
            list_dir = list(path_names.name for path_names in os.scandir(dir_name))
            if len(list_dir) == 0:
                return ""
            for dirc in list_dir:
                if os.path.isdir(dir_name + "/" + dirc):
                   previous_list = list_dir[:]
                   result = find_first(filename,(dir_name + "/" + dirc))
                   list_dir = previous_list[:]
                   if result:
                      return result
                elif dirc == filename:
                   treasure = dir_name + "/" + dirc
                   return os.path.relpath(treasure,os.path.abspath(repository_path))
            return result


def find(filename: str, dir_name: str) -> []:
       result = []
       if os.path.exists(filename):
            result += [os.path.relpath(filename,os.path.abspath(repository_path))]
            return result
       else:
            list_dir = list(path_names.name for path_names in os.scandir(dir_name))
            if len(list_dir) == 0:
                return result
            for dirc in list_dir:
                if os.path.isdir(dir_name + "/" + dirc):
                   previous_list = list_dir[:]
                   result += find(filename,(dir_name + "/" + dirc))
                   list_dir = previous_list[:]
                elif dirc == filename:
                   treasure = dir_name + "/" + dirc
                   result += [os.path.relpath(treasure,os.path.abspath(repository_path))] 
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
            result = g.pull()
        except Exception as failed_commit:
            print(failed_commit)
            dolphin_sleep()
            continue

        commit_date = datetime.datetime.fromtimestamp(master.commit.committed_date)
        commit_message = master.commit.message
        commit_author = master.commit.author.name

        # New commit
        if str(commit_date) != str(last_commit_date):
            bot.send_message(chat_id, "New commit in " + repo_name + "\nTitle: " + commit_message + "  " "\nBy: " +
                             commit_author + "\nDate: " + str(commit_date))
            if(result != "Already up to date."):
                bot.send_message(chat_id, result)
            last_commit_date = commit_date
            set_key(env_path, "LAST_COMMIT_DATE", str(last_commit_date))
        dolphin_sleep()


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.reply_to(message, "Stopping...")
    bot.stop_polling()

@bot.message_handler(commands=['lastcommit'])
def lastcommit(message):
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
    response = "Ue " + message.from_user.first_name
    bot.reply_to(message, response)


# /ping command handler
@bot.message_handler(commands=['ping'])
def ping_pong(message):
    bot.reply_to(message, "pong")


@bot.message_handler(commands=['find_first', 'findfirst', 'first'])
def start_find_first(message):
    res = ""

    filename = str(message.text.split(" ",1)[1:])
    tmp = filename.strip("['")
    filename = tmp.strip("']")
    #finds the first occourrence of a file, given its name.
    try:
             #no filename is provided
           if not filename:
              response = "Specify  the file to search!"
              bot.reply_to(message, response)
           else:
               res = find_first(filename, repository_path)

               if not res :
                 response = "File Not found!"
                 bot.reply_to(message, response)
               else:
                 response = res
                 bot.reply_to(message, response)

    except Exception as e:
         print(e)
         return

@bot.message_handler(commands=['find', 'all', 'findall'])
def start_find(message):
    res = []

    filename = str(message.text.split(" ",1)[1:])
    tmp = filename.strip("['")
    filename = tmp.strip("']")
    #finds file in repo recursively (finds the first one with matching name)
    try:
             # if no filename is provided
           if not filename:
              response = "Specify  the file to search!"
              bot.reply_to(message, response)
           else:
               res = find(filename, repository_path)
               if not res :
                 response = "File Not found!"
                 bot.reply_to(message, response)
               else:
                 for x in res:
                              bot.reply_to(message, x)

    except Exception as e:
         print(e)
         return




# /cat command handler
@bot.message_handler(commands=['cat'])
def cat_file(message):
    file_path = ""

    try:
        file_path = obtain_path(message.text, "/cat ")  # get file_path
        # if no path is provided
        if file_path == "":
            response = "Meow! Specify the path or the file in the repo!"

        # check if the file exists
        elif not os.path.exists(file_path):
               response = "File Not Found!"

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

    response = "I got this path: " + file_path + '\n\n' + response
    bot.reply_to(message, response)



# /setdelay command handler
@bot.message_handler(commands=['delay'])
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
    killer = Process_Killer()
    log("I'm alive!")
    start_commit_updater()

    while not killer.kill:
        try:
            bot.infinity_polling(interval=5)
            pid = os.get_pid()
        except Exception as connection_timeout:
            print(str(datetime.datetime) + str(connection_timeout))
            dolphin_sleep()
        if (pid == 0):
            bot.send_message(chatid,"sto per morire")
