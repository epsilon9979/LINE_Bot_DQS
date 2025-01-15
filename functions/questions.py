from linebot.models import *

def question(data):
    return TextSendMessage(data[1])
