from linebot.models import *
from database import record
import random

def choice(data): # data = [TextSendMessage(questions), (id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url), item]
    
    #增加正確選項的隨機性
    options = list(data[1])[2:6] 
    random_options = {}
    for i in range[0:4]:
        orin_option = options.pop( random.randint(0, len(options)-i) )
        random_options[i] = orin_option.split(")")
    for key, value in random_options.items():
        if data[1][6] in value:
            answer = ["A", "B", "C", "D"][key]
    question_2 = (1000, data[1][1], random_options[0][1], random_options[1][1], random_options[2][1], random_options[3][1],
                  answer, data[1][7], data[1][8], data[1][9], data[1][10])
    
    database = record()
    cursor, cnx = database.setting()
    database.append(cursor, cnx, question_2, data[2])
    
    template_message = TemplateSendMessage(
        alt_text = "pick up a correct option",
        template = {
            "type": "carousel",
            "columns":[
                {"title": "A", "text": random_options[0][1], "actions": [{"type": "message", "label": "選擇", "text": f"{data[2]}-{data[1][0]}\nA"}] },
                {"title": "B", "text": random_options[1][1], "actions": [{"type": "message", "label": "選擇", "text": f"{data[2]}-{data[1][0]}\nB"}] },
                {"title": "C", "text": random_options[2][1], "actions": [{"type": "message", "label": "選擇", "text": f"{data[2]}-{data[1][0]}\nC"}] },
                {"title": "D", "text": random_options[3][1], "actions": [{"type": "message", "label": "選擇", "text": f"{data[2]}-{data[1][0]}\nD"}] }
            ]
        }
    )
    
    return template_message