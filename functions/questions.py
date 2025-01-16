from linebot.models import *
from database import record
import random

def question(item):
    database = record()
    cursor, cnx = database.setting()
    database.delete(cursor, cnx, item, "id = 1000") #確保沒有臨時性作答紀錄
    
    counties = ['基隆','新北市','臺北市','桃園市','新竹','苗栗縣','臺中市','彰化縣','南投縣','雲林縣','嘉義','臺南市','高雄市','屏東縣','臺東縣','花蓮縣','宜蘭縣','連江縣','金門縣','澎湖縣','國際議題','能源議題','防災資訊']
    index = counties.index(item)
    which_table = ['keelung', 'new_taipei', 'taipei', 'taoyuan', 'hsinchu', 'miaoli', 'taichung',
                'changhua', 'nantou', 'yunlin', 'chiayi', 'tainan', 'kaohsiung', 'pingtung',
                'taitung', 'hualien', 'yilan', 'lienchiang', 'kinmen', 'penghu', 'international'][index]
    if which_table not in database.show_tables(cursor):
        product = f"目前沒有 '{which_table}' 的相關題目"
        return product
    existed_id = database.fetch(cursor, cnx, which_table, 'id', None)
    number = random.choice(existed_id)
    criteria = f"id = '{number[0]}'"
    result = database.fetch(cursor, cnx, which_table, '*', criteria)[0]
    # database.fetch = [(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url)]
    data = [TextSendMessage(result[1]), result, item]
    return data
