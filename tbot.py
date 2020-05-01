from flask import Flask, request 
import telegram

from BankFAQbot import FaqAPI

bot_user_name = "emurgobot"
URL = "https://3f5c5ab1.ngrok.io/"

global bot
global TOKEN
TOKEN = "1139283991:AAG9lzTb7-Oe-de5fhXrZxEhLquOjnVvfdQ"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    if text == "/faq":
        ask_question = """
       You may ask your question now
       """
        bot.sendMessage(chat_id=chat_id,
                        text=ask_question,
                        reply_to_message_id=msg_id)

    else:
        try:
            answer = FaqAPI(text)
            bot.sendMessage(chat_id=chat_id,
                            text=answer,
                            reply_to_message_id=msg_id)
        except Exception:
            bot.sendMessage(
                chat_id=chat_id,
                text=
                "There was a problem in the name you used, please enter different name",
                reply_to_message_id=msg_id)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=3002)
