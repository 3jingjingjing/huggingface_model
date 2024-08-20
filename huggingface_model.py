from flask import Flask, render_template, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage
from transformers import pipeline
import os
import string

app = Flask(__name__, template_folder='templates')

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))

# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

pipe = pipeline("text-generation", model="khrisintw/merge1")

def hug_response(text):
    response = pipeline("text-generation", model="khrisintw/merge1")

    answer = response.choices[0].message['content']

    answer = answer.translate(str.maketrans('', '', string.punctuation))

    return answer


@app.route("/")
def index():
    return render_template("./index.html")


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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    hug_answer = hug_response(msg)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(hug_answer))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
