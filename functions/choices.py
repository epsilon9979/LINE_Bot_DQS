from linebot.models import *
from datetime import datetime, timedelta
from functions.database import record
import random

def choice(data): # data = [TextSendMessage(questions), (id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url), which_table, item]

    #增加正確選項的隨機性
    options = list(data[1][2:6]) 
    random_options = {}
    for i in range(0,4):
        orin_option = options.pop( random.randint(0, len(options)-1) )
        random_options[i] = orin_option.split(")")
    orin_answer = data[1][6].split("：")[1].strip().split(")")[0]
    for key, value in random_options.items():
        if orin_answer in value:
            answer = ["A", "B", "C", "D"][key]
    
    #將題目進行客製化編號        
    database = record()
    cursor, cnx = database.setting()
    existed_tables = database.show_tables(cursor)
    if 'Memory' not in existed_tables:
        database.create_table(cursor, 'Memory')
    which_table = ['Keelung', 'New_Taipei', 'Taipei', 'Taoyuan', 'Hsinchu', 'Miaoli', 'Taichung',
                    'Changhua', 'Nantou', 'Yunlin', 'Chiayi', 'Tainan', 'Kaohsiung', 'Pingtung',
                    'Taitung', 'Hualien', 'Yilan', 'Lienchiang', 'Kinmen', 'Penghu', 'international', 'energy', 'disaster']
    table_code = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    index = which_table.index(data[2])
    code = int(table_code[index])
    id_mem = 10000000+code*100000+int(data[1][0])*100 #1-table_code(11)-id(111)-num(11)
    while True:
        existed_id = database.fetch(cursor, cnx, "Memory", 'id', None)[0] #[[(1,), (2,), (3,)...]]
        if (id_mem,) not in existed_id:
            break
        else:
            id_mem = id_mem + 1
    
    #計時開始，並進入作答記憶區
    now = datetime.now() 
    delta = timedelta(seconds=60) 
    criteria = f"time<'{now - delta}'"       
    database.delete(cursor, cnx, "Memory", criteria) 
    question_2 = (id_mem, data[1][1], random_options[0][1], random_options[1][1], random_options[2][1],
                  random_options[3][1], answer, data[1][7], data[1][8], now, data[1][10])
    database.append(cursor, cnx, question_2, "Memory")
    
    # 輪播範本訊息進行題目呈現
    template_message = FlexSendMessage(
        alt_text="pick up a correct option",
        contents={
            "type": "carousel",
            "contents": [
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "A",
                        "color": "#000000"
                    },
                    {
                        "type": "text",
                        "text": random_options[0][1],
                        "margin": "md",
                        "color": "#000000",
                        "wrap": True
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "separator",
                        "color": "#000000"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "Select",
                        "text": f"{data[3]}-{id_mem}\nA"
                        },
                        "offsetTop": "xs"
                    }
                    ],
                    "paddingAll": "xs"
                }
                },
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "B",
                        "color": "#000000"
                    },
                    {
                        "type": "text",
                        "text": random_options[1][1],
                        "margin": "md",
                        "color": "#000000",
                        "wrap": True
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "separator",
                        "color": "#000000"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "Select",
                        "text": f"{data[3]}-{id_mem}\nB"
                        },
                        "offsetTop": "xs"
                    }
                    ],
                    "paddingAll": "xs"
                }
                },
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "C",
                        "color": "#000000"
                    },
                    {
                        "type": "text",
                        "text": random_options[2][1],
                        "margin": "md",
                        "color": "#000000",
                        "wrap": True
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "separator",
                        "color": "#000000"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "Select",
                        "text": f"{data[3]}-{id_mem}\nC"
                        },
                        "offsetTop": "xs"
                    }
                    ],
                    "paddingAll": "xs"
                }
                },
                {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "D",
                        "color": "#000000"
                    },
                    {
                        "type": "text",
                        "text": random_options[3][1],
                        "margin": "md",
                        "color": "#000000",
                        "wrap": True
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "separator",
                        "color": "#000000"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "message",
                        "label": "Select",
                        "text": f"{data[3]}-{id_mem}\nD"
                        },
                        "offsetTop": "xs"
                    }
                    ],
                    "paddingAll": "xs"
                }
                }
            ]
            }
    )
    
    return template_message