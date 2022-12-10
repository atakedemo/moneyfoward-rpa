from dotenv import load_dotenv
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

load_dotenv()
LINE_CH_ACCESS_TOKEN= os.environ['LINE_CH_ACCESS_TOKEN']
ID01 = os.environ['TARGET_ID01']

line_bot_api = LineBotApi(LINE_CH_ACCESS_TOKEN)

def push_text(text):
    # Create text content to send to LINE
    messages = TextSendMessage(text=text)
    # Push massages to LINE
    try:
        line_bot_api.push_message(ID01, messages)
        #line_bot_api.multicast([ID01], messages=messages)
    except LineBotApiError as e:
        # error handle
        print(e)
        