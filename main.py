"""All the crap r in this file, Load messages, and stuff like that"""
import logging #Logger
import requests #GET
import base64 #Decode the base64 string to utf-8
import json #For reading token from config.json
import os #For deleting files
import libs #Landscape for useful craps

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
#Telegram stuff

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    #Reply sth when the user first time using this bot.
    update.message.reply_text('Hi.\nSend /help to see how this work.')

def GrabItDown(update, context):
    user_text = update.message.text
    if len(user_text) <= 6:
        text = 'Invaild url.'
    else:
        try:
            remote_url = user_text.split(' ')[-1].split('//')[-1]
            result = requests.get(f"https://{remote_url}")
            if result.status_code == 200 and result.text != '':
                b64_bytes = base64.b64decode(result.text)
                text = str(b64_bytes, 'utf-8')
            else:
                text = f"Can't retrive data from the given links\nStatus code: {result.status_code}\nRaw data: {result.text}"
        except Exception as feedback:
            text = str(feedback)
    if len(text) >= 4096:
        with open('cache.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        update.message.reply_text("Too long! Will be send as a txt file\n(We will delete the one on our server after sending it)")
        update.message.reply_document(open('cache.txt', 'rb'))
        os.remove('cache.txt')
    else:
        update.message.reply_text(text)

def LoadToken():
    #Maybe will add debug function here later
    with open('config.json', 'r') as container:
        loaded_json = json.loads(container.read())
        try:
            token = loaded_json['token']
        except Exception as feedback:
            print(feedback)
            token = ''
        return token

def Help(update, context):
    """Show some text that might help"""
    update.message.reply_text("""/get [argument]
Argument: The subscription link that your proxy service provider provided to you.
Info: Get your vmess or other links asap
/ping
Argument: None
Info: Check this bot is dead or not, Pong!
/help
Arugument: None
Info: As you see, It show this crap you are looking right now
/update [argument]
Argument: ['v2rayng', 'shadowsocks-android', 'shadowsocks-win', 'shadowsocks-qt5', 'v2ray-core-win32', 'v2ray-core-linux-amd64',  'v2ray-core-linux-arm32']
Info: Update(Download) the software on the server that hosting this bot, Recommend running this when u first deploy it
    """)

def ping(update, context):
    #Pong
    update.message.reply_text('Pong!')

def echo(update, context):
    #Return sth when the user is not giving the correct command.
    update.message.reply_text('Unrecognized command.')

def error(update, context):
    #Logging those errors
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def download_latest(update, context):
    update.message.reply_text('Running...') #Just letting the user know this bot is working
    response = libs.get_latest.main(command_string=update.message.text)
    update.message.reply_text(response)

def send_it(update, context):
    user_text = update.message.text
    response, file_loca = libs.sending_file.main(user_text)
    update.message.reply_text(response)
    if file_loca is not '' or None:
        update.message.reply_document(open(file_loca, 'rb'))
    else:
        pass

def main():
    #Do the job
    updater = Updater(LoadToken(), use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', Help))
    updater.dispatcher.add_handler(CommandHandler('get', GrabItDown))
    updater.dispatcher.add_handler(CommandHandler('ping', ping))
    updater.dispatcher.add_handler(CommandHandler('update', download_latest))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
