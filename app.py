from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from dotenv import load_dotenv
import os
import re

# ======這裡是呼叫的檔案內容=====
# from functions.questions import question
# from Message_test2 import *
# from Message_test3 import *

# ========ChatBot開始==========
load_dotenv()
app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('Channel_Access_Token'))
line_handler = WebhookHandler(os.getenv('Channel_Secret'))
category = ['基隆','新北市','臺北市','桃園市','新竹','苗栗縣','臺中市','彰化縣','南投縣','雲林縣','嘉義','臺南市','高雄市','屏東縣','臺東縣','花蓮縣','宜蘭縣','連江縣','金門縣','澎湖縣','國際議題']
# Your user ID
# line_bot_api.push_message(os.getenv('User_ID'), TextSendMessage(text='他媽的終於成功了'))

# ========監聽所有來自 /callback 的 Post Request==========
@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature) 
    except InvalidSignatureError:
        abort(400)
    return "OK"

# ========訊息傳遞區塊==========
##### 基本上程式編輯都在這個function #####
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    AAA = 'ABCDEFG'
    template_message = TemplateSendMessage(
        alt_text = "this is a carousel template",
        template = {
            "type": "carousel",
            "columns":[
                {"title": "A", "text": f"A\n{AAA}", "actions": [{"type": "message", "label": "選擇", "text": "A"}] },
                {"title": "B", "text": "bbb", "actions": [{"type": "message", "label": "選擇", "text": "B"}] },
                {"title": "C", "text": "c", "actions": [{"type": "message", "label": "選擇", "text": "C"}] },
                {"title": "D", "text": "d", "actions": [{"type": "message", "label": "選擇", "text": "D"}] }
            ]
        }
    )

    
    line_bot_api.reply_message(event.reply_token, template_message)


# ========主程式==========
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)