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
    template_message = FlexSendMessage(
        alt_text = 'answer',
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "恭喜答對",
                    "weight": "bold",
                    "color": "#22FF00",
                    "size": "xxl"
                },
                {
                    "type": "text",
                    "text": "正確答案是 A",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md",
                    "color": "#22FF00"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#22FF00"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": " 由於美國政府對 TikTok 的潛在禁令，許多美國用戶開始尋找替代性的社交媒體應用。而中國社交媒體應用小紅書（Xiaohongshu，美國用戶常常縮寫為 RedNote）在最近一週 的美國手機下載量翻了近三倍，並在美國 App Store 的排名中一度攀升至首位，成為美國用戶選擇的主要 TikTok 替代方案。",
                        "color": "#FFFFFF",
                        "position": "relative",
                        "wrap": True
                    }
                    ],
                    "spacing": "md",
                    "position": "relative",
                    "margin": "xxl",
                    "alignItems": "center"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#22FF00"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "資料日期",
                            "weight": "regular",
                            "decoration": "none",
                            "align": "center",
                            "size": "md",
                            "style": "normal",
                            "gravity": "center",
                            "margin": "sm",
                            "color": "#FFFFFF",
                            "offsetStart": "none",
                            "offsetEnd": "none"
                        },
                        {
                            "type": "text",
                            "text": "2024/12/12",
                            "gravity": "center",
                            "size": "md",
                            "align": "center",
                            "color": "#FFFFFF"
                        }
                        ],
                        "position": "relative",
                        "alignItems": "center",
                        "spacing": "sm",
                        "margin": "sm",
                        "offsetStart": "none",
                        "offsetEnd": "xxl",
                        "paddingStart": "none",
                        "paddingEnd": "none",
                        "justifyContent": "space-evenly"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "資料原文",
                        "uri": "http://linecorp.com/"
                        },
                        "gravity": "bottom",
                        "margin": "none",
                        "style": "primary",
                        "height": "md",
                        "offsetTop": "none",
                        "offsetStart": "none"
                    }
                    ],
                    "action": {
                    "label": "action",
                    "data": "hello",
                    "displayText": "123123"
                    },
                    "position": "relative",
                    "margin": "xxl",
                    "spacing": "xxl",
                    "borderWidth": "none"
                }
                ],
                "backgroundColor": "#000000",
                "borderWidth": "medium",
                "borderColor": "#22FF00"
            },
            "styles": {
                "footer": {
                "separator": TRUE
                }
            }
            }

    )

    
    line_bot_api.reply_message(event.reply_token, template_message)


# ========主程式==========
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)