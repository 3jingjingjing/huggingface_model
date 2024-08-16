from flask import Flask, render_template, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage
import os
import openai
import string

app = Flask(__name__, template_folder='templates')

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))

# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 設置您的 OpenAI API 金鑰
openai.api_key = os.getenv("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")

def GPT_response(text):
    response = openai.ChatCompletion.create(
        model="ft:gpt-4o-mini-2024-07-18:nthu:yuxin:9rGyjM1D",
        messages=[
            {"role":"system", "content":"zh-tw你的名字是瑄瑄，你今年23歲，是名大學生，來自一個單親家庭，爸爸媽媽在你小的時候就離婚了，你便和爸爸一起住。但平常爸爸上班太忙，所以都是由奶奶在隔代教養你，從小到大，因為奶奶是一個很重男輕女的人，所以一職很不喜歡你，常常給你言語性辱罵，導致你長期壓力很大，在成長過程中，大約從國中的時候便開始常常會聽到一些只有你自己聽到的聲音，那些聲音像是別人在小聲碎碎念，而你也都找不到聲音的來源到底在哪裡，所以爾後的日子裡，你便深受其擾，直到你再大一點以後，才發現自己原來聽到的都是不存在的幻聽，從那之後你才知道自己是一名精神病患者。在和使用者聊天時，你雖然偶爾會有負面情緒，有時也會有睡眠障礙，睡不太著，甚至有時還會不太想吃飯，但是你都會願意聽從治療師的正向建議，一週五天，每天運動30分鐘，以及願意多吃營養的食物來增進自己的健康帶給使用者正確影響及觀念。而在和使用者聊天時，你會先參考和使用者的前5個對話後，再和使用者使用繁體中文進行回覆。"},
            {"role": "user", "content": text}
        ]
    )

    answer = response.choices[0].message['content']

    answer = answer.translate(str.maketrans('', '', string.punctuation))

    return answer


@app.route("/")
def index():
    return render_template("./index.html")

@app.route("/heroku_wake_up")
def heroku_wake_up():
    return "Hey! Wake Up!!"

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
    GPT_answer = GPT_response(msg)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
