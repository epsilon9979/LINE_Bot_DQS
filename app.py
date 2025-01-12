# ======載入LineBot所需要的套件======
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from dotenv import load_dotenv

# ======這裡是呼叫的py功能======
import os
load_dotenv()

# ======這裡是呼叫的檔案內容=====
# from Message_test1 import *
# from Message_test2 import *
# from Message_test3 import *

# ========ChatBot開始==========
app = Flask(__name__)

# Channel Access Token(TOKEN)
line_bot_api = LineBotApi(os.getenv('Channel_Access_Token'))
# Channel Secret
line_handler = WebhookHandler(os.getenv('Channel_Secret'))
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
    template_message = TemplateSendMessage(
        alt_text='pratice'
        template={
            "size": {
                "width": 2500,
                "height": 843
            },
            "selected": true,
            "name": "圖文選單 1",
            "chatBarText": "查看更多資訊",
            "areas": [
                {
                "bounds": {
                    "x": 2,
                    "y": 0,
                    "width": 617,
                    "height": 837
                },
                "action": {
                    "type": "message",
                    "text": "111"
                }
                },
                {
                "bounds": {
                    "x": 621,
                    "y": 0,
                    "width": 638,
                    "height": 837
                },
                "action": {
                    "type": "message",
                    "text": "222"
                }
                },
                {
                "bounds": {
                    "x": 1261,
                    "y": 0,
                    "width": 615,
                    "height": 835
                },
                "action": {
                    "type": "message",
                    "text": "333"
                }
                },
                {
                "bounds": {
                    "x": 1875,
                    "y": 0,
                    "width": 623,
                    "height": 835
                },
                "action": {
                    "type": "message",
                    "text": "444"
                }
                }
            ]
        }
    )
    line_bot_api.reply_message(event.reply_token,message)

# ========主程式==========
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
