# 跑程式前，記得先設定 ngrok_url，並將 ngrok_url 複製貼上到 webhook

import datetime
import errno
import json
import os
import sys
import tempfile
from dotenv import load_dotenv
from argparse import ArgumentParser

from flask import Flask, request, abort, send_from_directory, make_response
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage, MessageTemplateAction)

from linebot.models import (
    RichMenu,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    URIAction
)
from linebot.models.actions import RichMenuSwitchAction
from linebot.models.rich_menu import RichMenuAlias

from menu_pic import pic_design
from demo_new import choice

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

# get channel_secret and channel_access_token from your environment variable
load_dotenv()
channel_secret = os.getenv('LINE_CHANNEL_SECRET', '4b3c9cb362994c4921b1680d2e8d8caf')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '31HK94ip0qFh9/7LuR/abBgWcCRzw/2ZFFOCAspXsYol+PJqXb6/pkoz4LOR5aNVGriy46o5S7nClMXiVo7WdyNE/mNFnqSvePdtxG0Gx6LpkjqB0T1DEIFio5prE/GZWF8shbV7LvlsLTE+KxMMGQdB04t89/1O/w1cDnyilFU=')
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# set ngrok url
ngrok_url = None
if ngrok_url is None:
    print('Please specify ngrok_url')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# global variables
QUESTION = 0
PREFERENCE = []


# menu.png不會一開始就存在
@app.route('/ck_paradise', methods=['GET'])
def ck_paradise_image():
    image_data = open('./menu.png', 'rb').read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'menu/png'
    return response


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global QUESTION
    global PREFERENCE
    text = event.message.text
    user_id = event.source.user_id
    demand = []
    # Q1
    if text.lower() == 'start':
        QUESTION = 1
        message = TemplateSendMessage(
            alt_text = "什麼口味?",
            template = ButtonsTemplate(
                # thumbnail_image_url="https://i2.kknews.cc/SIG=3j4a194/qqo00048rs927p7qp3p.jpg",
                text="什麼口味?",
                actions=[
                    MessageTemplateAction(label="酸(酸爽的青春)", text="酸"),
                    MessageTemplateAction(label="甜(甜蜜的依戀)", text="甜"),
                    MessageTemplateAction(label="苦(苦澀的成長)", text="苦"),
                    MessageTemplateAction(label="特殊(夠大的心臟)", text="特殊"),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    # Q2
    elif ((text.lower()=="酸") or (text.lower()=="甜") or (text.lower()=="苦") or (text.lower()=="特殊")) and QUESTION == 1:
        QUESTION = 2
        PREFERENCE.append(text)
        message = TemplateSendMessage(
            alt_text = "3選1",
            template = ButtonsTemplate(
                # thumbnail_image_url="https://i2.kknews.cc/SIG=3j4a194/qqo00048rs927p7qp3p.jpg",
                text="3選1",
                actions=[
                    MessageTemplateAction(label="果香", text="果香"),
                    MessageTemplateAction(label="濃醇香", text="濃醇香"),
                    MessageTemplateAction(label="自然香", text="自然香")
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)


    # Q2a
    elif (text.lower()=="果香") and QUESTION == 2:
        QUESTION = 3
        PREFERENCE.append(text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="選果香",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="莓果", text="莓果")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="葡萄", text="葡萄")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="熱帶水果", text="熱帶水果")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="蘋果", text="蘋果")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="柑橘", text="柑橘")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="台灣味", text="台灣味")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="瓜類", text="瓜類")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="檸檬萊姆", text="檸檬萊姆")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="綜合", text="綜合")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="桃類", text="桃類")
                        ),
                    ]
                )
            )
        )


    # Q2b
    elif (text.lower()=="濃醇香") and QUESTION == 2:
        QUESTION = 3
        PREFERENCE.append(text)
        message = TemplateSendMessage(
            alt_text = "選濃醇香",
            template = ButtonsTemplate(
                # thumbnail_image_url="https://i2.kknews.cc/SIG=3j4a194/qqo00048rs927p7qp3p.jpg",
                text="選濃醇香",
                actions=[
                    MessageTemplateAction(label="奶香", text="奶香"),
                    MessageTemplateAction(label="咖啡", text="咖啡"),
                    MessageTemplateAction(label="巧克力", text="巧克力"),
                    MessageTemplateAction(label="堅果", text="堅果")
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)



    # Q2c
    elif (text.lower()=="自然香") and QUESTION == 2:
        QUESTION = 3
        PREFERENCE.append(text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="選自然香",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="薑味", text="薑味")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="藥草", text="藥草")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="香料", text="香料")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="薄荷", text="薄荷")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="茶香", text="茶香")
                        ),
                    ]
                )
            )
        )


    # Answer
    elif QUESTION == 3:
        PREFERENCE.append(text)
        print('PREFERENCE = ', PREFERENCE)
        QUESTION = 0

        demand = choice(PREFERENCE[0], PREFERENCE[1], PREFERENCE[2])
        png_filename = pic_design(demand)
        PREFERENCE = []

        line_bot_api.push_message(user_id,
                                  TextSendMessage(
                                      text='推薦中，請稍候...'))
        line_bot_api.push_message(user_id,
                                  ImageSendMessage(
                                      original_content_url=ngrok_url + '/ck_paradise',
                                      preview_image_url=ngrok_url + '/ck_paradise'
                                  )
                                  )

    # Anything else
    else:
        QUESTION = 0
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入「Start」 \n讓我為您推薦好喝的調酒 (๑´ㅂ`๑)"),
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)