from mysql.connector import errorcode
import mysql.connector
import random

def data(stuff): 
    
    def setting():
        try:
            cnx = mysql.connector.connect(user='root', password='999999',host='127.0.0.1',database='questions_warehouse')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            
        cursor = cnx.cursor()
        return cursor, cnx

    def fetch(cursor, cnx, which_table, which_item, criteria):
        #items:(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, source)
        if criteria:
            query = (f"SELECT {which_item} FROM {which_table} WHERE {criteria}")
        else:
            query = (f"SELECT {which_item} FROM {which_table}")
        cursor.execute(query)
        box = []
        for goals in cursor:
            box.append(goals)
        return box

    def show_tables(cursor):
        cursor.execute("SHOW TABLES")
        existed_tables = []
        for table in cursor:
            table = str(table[0])
            existed_tables.append(table)
        return existed_tables

    cursor, cnx = setting()
    counties = ['基隆','新北市','臺北市','桃園市','新竹','苗栗縣','臺中市','彰化縣','南投縣','雲林縣','嘉義','臺南市','高雄市','屏東縣','臺東縣','花蓮縣','宜蘭縣','連江縣','金門縣','澎湖縣','國際議題','能源議題','防災資訊']
    index = counties.index(stuff)
    which_table = ['keelung', 'new_taipei', 'taipei', 'taoyuan', 'hsinchu', 'miaoli', 'taichung',
                'changhua', 'nantou', 'yunlin', 'chiayi', 'tainan', 'kaohsiung', 'pingtung',
                'taitung', 'hualien', 'yilan', 'lienchiang', 'kinmen', 'penghu', 'international'][index]
    if which_table not in show_tables(cursor):
        product = f"目前沒有 '{which_table}' 的相關題目"
        return product
    existed_id = fetch(cursor, cnx, which_table, 'id', None)
    sequence = ['questions', 'optionA', 'optionB', 'optionC', 'optionD', 'answer', 'explaination','source']
    