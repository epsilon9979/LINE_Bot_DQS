from linebot.models import *
from functions.database import record
import random

def question(item):
    database = record() 
    cursor, cnx = database.setting()
    counties = ['基隆','新北市','臺北市','桃園市','新竹','苗栗縣','臺中市','彰化縣','南投縣','雲林縣','嘉義','臺南市','高雄市','屏東縣','臺東縣','花蓮縣','宜蘭縣','連江縣','金門縣','澎湖縣','國際議題','能源議題','防災資訊']
    index = counties.index(item)
    which_table = ['Keelung', 'New_Taipei', 'Taipei', 'Taoyuan', 'Hsinchu', 'Miaoli', 'Taichung',
                    'Changhua', 'Nantou', 'Yunlin', 'Chiayi', 'Tainan', 'Kaohsiung', 'Pingtung',
                    'Taitung', 'Hualien', 'Yilan', 'Lienchiang', 'Kinmen', 'Penghu', 'international','energy','disaster'][index]
    if which_table not in database.show_tables(cursor) or database.fetch(cursor, cnx, which_table, "id", None)==[]:
        product = f"目前沒有 {item} 的相關題目"
        return [TextSendMessage(text=product), "empty", "empty"]
    
    existed_id = database.fetch(cursor, cnx, which_table, 'id', None) #[(1,), (2,), (3,)...]
    number = random.choice(existed_id)
    criteria = f"id={number[0]}"
    result = database.fetch(cursor, cnx, which_table, '*', criteria)[0]
    # database.fetch = [(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url)]
    
    description = f"#{item}-{result[0]}\n\n{result[1]}"
    data = [TextSendMessage(text = description), result, which_table, item] #which_table是英文，item是中文
    return data
