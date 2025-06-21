import os
import json
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

class record:   
    
    def __init__(self):
        pass

    def setting(self):
        try:
            service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
            # creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
            client = gspread.authorize(creds)
            sheet_id = "1TIV5rHSUcdhBnR2mdUHWgbA-UGW76Nx7mvWPOaPptnw"
            cursor = client.open_by_key(sheet_id)
        except Exception as e:
            print("發生錯誤,因為:", e)
            return None, None
        else:
            print("successfully connect to database")
            cnx = 0  #純粹配合格式，本身無意義
            return cursor, cnx
    
    
    def create_table(self, cursor, name):
        try:
            sheet = cursor.add_worksheet(title=name, rows=1000, cols=20)
            sheet.update("A1:K1", [["id", "questions", "optionA", "optionB", "optionC", "optionD", "answer", "explaintion", "date", "time", "url"]])
        except Exception as e:
            print(f"{name} already exists",e)
        else:
            print(f"Successfully creating table {name}")
        
            
    def append(self, cursor, cnx, content, which_table):
        sheet = cursor.worksheet(which_table)
        values = list(content)
        # values[8] = values[8].strftime("%Y-%m-%d %H:%M:%S")
        values[9] = values[9].strftime("%Y-%m-%d %H:%M:%S")
        id = int(values[0])
        print("id:", id)
        sheet.update(f"A{id+1}:k{id+1}", [values], value_input_option="USER_ENTERED")
        print(f"successfully append {id} to {which_table}.")
              
              
    def fetch(self, cursor, cnx, which_table, which_item, criteria):
        #items:(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url)
        try:
            sheet = cursor.worksheet(which_table)
            if criteria is not None and "id=" in criteria:
                id = int(criteria.split("=")[1])
                box = sheet.row_values(id+1)
            elif criteria is None:
                cell = sheet.find(which_item)
                box = sheet.col_values(cell.col)[1:]
                box = [i for i in box if i.strip()]
            return [box]
        except Exception as e:
            print("something wrong:", e)
            return []


    def delete(self, cursor, cnx, which_table, criteria):
        try:
            sheet = cursor.worksheet(which_table)
            if "time<" in criteria:
                expire_date = criteria.split("<")[1].strip("'")
                expire_date = datetime.strptime(expire_date, "%Y-%m-%d %H:%M:%S.%f")
                box_date = (sheet.col_values(sheet.find("time").col))[1:]
                box_date = [i for i in box_date if i.strip()]
                box_date = [datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in box_date]
                box_id = (sheet.col_values(sheet.find("id").col))[1:]
                box_id = [i for i in box_id if i.strip()]
                for item in box_date:
                    if item < expire_date:
                        idx = box_date.index(item)
                        row = sheet.find(box_id[idx]).row
                        # print(f"successfully deleting data: \n { tuple(sheet.row_values(row)) }")
                        sheet.batch_clear([f"A{row}:K{row}"])
                        
            if "id=" in criteria:
                id = criteria.split("=")[1].strip("'")  
                row = sheet.find(id).row 
                sheet.batch_clear([f"A{row}:K{row}"])         
                
        except Exception as e:
            print("something wrong", e)
        
        
    def show_tables(self, cursor):
        if cursor is None:
            print("cursor 無效，無法讀取表單")
            return []
        sheets = cursor.worksheets()
        return [sheet.title for sheet in sheets]

    
    