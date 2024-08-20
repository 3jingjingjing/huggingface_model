from flask import Flask, render_template, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage
import os
import tempfile
import datetime
import time
import string
##from huggingface_model import hug_response

app = Flask(__name__, template_folder='templates')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))

# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/")
def index():
    return render_template("./index.html")

@app.route("/heroku_wake_up")
def heroku_wake_up():
    return "Hey!Wake Up!!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

##@handler.add(MessageEvent, message=TextMessage)
##def handle_message(event):
    msg = event.message.text
    hug_answer = hug_response(msg)
    print(hug_answer)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(hug_answer))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
