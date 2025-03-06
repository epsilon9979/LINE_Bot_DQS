from linebot.models import *
from datetime import datetime, timedelta
from functions.database import record

def answer(response): 
    mark, selection = response.split("\n")
    county, id_mem = mark.split("-")
    id_mem = int(id_mem)
    database = record()
    cursor, cnx = database.setting()
    if (id_mem,) not in database.fetch(cursor, cnx, "Memory", 'id', None): #[(1,), (2,), (3,)...]
        return TextSendMessage(text = f"{database.fetch(cursor, cnx, "Memory", 'id', None)}")
    question_2 = database.fetch(cursor, cnx, "Memory", '*', f'id = {id_mem}')
    # question_2 = [(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url)]
    now = datetime.now() 
    delta = timedelta(seconds=30)       
    for time in database.fetch(cursor, cnx, "Memory", 'time', None):
        if now - time[0] > delta:
            database.delete(cursor, cnx, "Memory", f"time = {time[0]}")
    database.delete(cursor, cnx, "Memory", f"id = {id_mem}") #刪除臨時性作答紀錄
    
    if question_2[0][6] == selection:
        border_color = "#22FF00"
        text_color = "#22FF00"
        text_top = "恭喜答對！"
    else:
        border_color = "#FF0000"
        text_color = "#FF0000"
        text_top = "很可惜，答錯了..."
        
    flex_message = FlexSendMessage(
        alt_text = 'answer',
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {"type": "text", "text": text_top, "weight": "bold", "color": text_color, "size": "xxl"},
                {"type": "text", "text": f"正確答案為 {question_2[0][6]}", "weight": "bold", "size": "xxl", "margin": "md", "color": text_color},
                {"type": "separator", "margin": "lg", "color": border_color},
                {"type": "box", "layout": "vertical","contents": [{
                        "type": "text",
                        "text": question_2[0][7],
                        "color": "#FFFFFF",
                        "position": "relative",
                        "wrap": True
                    }],
                    "spacing": "md", "position": "relative", "margin": "xxl", "alignItems": "center"},
                {"type": "separator", "margin": "lg", "color": border_color},
                {"type": "box", "layout": "horizontal", "contents": [{
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {"type": "text", "text": "資料日期", "weight": "regular", "decoration": "none", "align": "center", "size": "md", "style": "normal", "gravity": "center", "margin": "sm", "color": "#FFFFFF", "offsetStart": "none", "offsetEnd": "none"},
                        {"type": "text", "text": question_2[0][8].strftime("%Y-%m-%d"), "gravity": "center", "size": "md", "align": "center", "color": "#FFFFFF"}
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
                        "action": {"type": "uri", "label": "資料原文", "uri": question_2[0][10]},
                        "gravity": "bottom",
                        "margin": "none",
                        "style": "primary",
                        "height": "md",
                        "offsetTop": "none",
                        "offsetStart": "none"
                    }],
                    "position": "relative",
                    "margin": "xxl",
                    "spacing": "xxl",
                    "borderWidth": "none"
                }
                ],
                "backgroundColor": "#000000",
                "borderWidth": "medium",
                "borderColor": border_color
            },
            
            "styles": {"footer": {"separator": True}}
        }
    )
    
    return flex_message
   