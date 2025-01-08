# ======載入LineBot所需要的套件======
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# ======這裡是呼叫的py功能======
import os

# ======這裡是呼叫的檔案內容=====
# from Message_test1 import *
# from Message_test2 import *
# from Message_test3 import *

# ========ChatBot開始==========
app = Flask(__name__)

# Channel Access Token(TOKEN)
line_bot_api = LineBotApi(os.getenv('Channel_Access_Token'))
# Channel Secret
handler = WebhookHandler(os.getenv('Channel_Secret'))
# Your user ID
line_bot_api.push_message(os.getenv('User_ID'), TextSendMessage(text='omg!終於成功了終於成功了！'))

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
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# ========訊息傳遞區塊==========
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

# ========主程式==========
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
