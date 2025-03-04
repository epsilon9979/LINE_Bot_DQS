import mysql.connector
from mysql.connector import errorcode

class record:   
    
    def __init__(self):
        pass
    
    
    def setting(self): 
        try:
            # cnx = mysql.connector.connect(
            #     user='vercel',                         # 資料庫用戶名稱
            #     password='iloveroyals941/O100659329',  # 資料庫密碼
            #     host='140.118.138.234',                   # 公網 IP
            #     database='questions_warehouse',        # 要連接的資料庫名稱（請改為你的資料庫名稱）
            #     port=3306                              # MySQL 默認埠號
            # )
            cnx = mysql.connector.connect(
                user='vercel',                         # 資料庫用戶名稱
                password='iloveroyals941/O100659329',  # 資料庫密碼
                host='35.234.3.230',                   # 公網 IP
                database='questions_warehouse',        # 要連接的資料庫名稱（請改為你的資料庫名稱）
                port=3306                              # MySQL 默認埠號
            )
            cursor = cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err) 
                    
        return cursor, cnx 
    
    
    def create_table(self, cursor, name):
        TABLES = {}
        TABLES[name] = (
            f"CREATE TABLE {name} ("
            "  `id` int NOT NULL,"
            "  `questions` varchar(1000) NOT NULL,"
            "  `optionA` varchar(100) NOT NULL,"
            "  `optionB` varchar(100) NOT NULL,"
            "  `optionC` varchar(100) NOT NULL,"
            "  `optionD` varchar(100) NOT NULL,"
            "  `answer` varchar(100) NOT NULL,"
            "  `explaintion` varchar(1000) NOT NULL,"
            "  `date` DATETIME,"
            "  `title` varchar(100) NOT NULL,"
            "  `url` varchar(1000) NOT NULL,"
            "  PRIMARY KEY(`id`)"
            ") ENGINE=InnoDB")


        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else: 
                    print(err.msg)
            else:
                print("OK")
        
            
    def append(self, cursor, cnx, content, which_table):
        add_product = (f"INSERT ignore INTO {which_table}"
                       "(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(add_product, content)
        cnx.commit()
              
              
    def fetch(self, cursor, cnx, which_table, which_item, criteria): 
        #items:(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url)
        if criteria:
            query = (f"SELECT {which_item} FROM {which_table} WHERE {criteria}")
        else:
            query = (f"SELECT {which_item} FROM {which_table}")
        cursor.execute(query)
        box = []
        for goals in cursor:
            box.append(goals)
        return box


    def delete(self, cursor, cnx, which_table, criteria):
        delete_query = ( f"DELETE FROM {which_table} WHERE {criteria}" )
        cursor.execute(delete_query)
        cnx.commit()
        
        
    def show_tables(self, cursor):
        cursor.execute("SHOW TABLES")
        existed_tables = []
        for table in cursor:
            table = str(table[0])
            existed_tables.append(table)
        return existed_tables

    
    