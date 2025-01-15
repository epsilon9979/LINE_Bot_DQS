from linebot.models import *

def choice():
    template_message = TemplateSendMessage(
        altText = "this is a carousel template",
        template = {
            "type": "carousel",
            "columns":[
                {"title": "A", "text": " ", "actions": [{"type": "message", "label": "選擇", "text": "A"}] },
                {"title": "B", "text": " ", "actions": [{"type": "message", "label": "選擇", "text": "B"}] },
                {"title": "C", "text": " ", "actions": [{"type": "message", "label": "選擇", "text": "C"}] },
                {"title": "D", "text": " ", "actions": [{"type": "message", "label": "選擇", "text": "D"}] }
            ]
        }
    )
    
    return template_message