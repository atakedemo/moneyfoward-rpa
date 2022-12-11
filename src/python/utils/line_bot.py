from dotenv import load_dotenv
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

load_dotenv()
LINE_CH_ACCESS_TOKEN= os.environ['LINE_CH_ACCESS_TOKEN']
ID01 = os.environ['TARGET_ID01']
ID02 = os.environ['TARGET_ID02']

line_bot_api = LineBotApi(LINE_CH_ACCESS_TOKEN)

def push_text(text):
    # Create text content to send to LINE
    text_sum = text["summary"]
    text_at = text["at"]
    messages_sum = TextSendMessage(text=text_sum)
    #messages_at = TextSendMessage(text=text_at)

    # Push massages to LINE
    try:
        line_bot_api.push_message(ID01, messages_sum)
        #line_bot_api.push_message(ID02, messages_at)
        #line_bot_api.multicast([ID01], messages=messages)
    except LineBotApiError as e:
        # error handle
        print(e)
        