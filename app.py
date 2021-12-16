import datetime
import errno
import json
import os
import sys
import tempfile
from dotenv import load_dotenv
from argparse import ArgumentParser

from flask import Flask, request, abort, send_from_directory
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

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

# get channel_secret and channel_access_token from your environment variable
load_dotenv()
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

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
START = 0

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global QUESTION
    global START
    text = event.message.text
    # button template
    # Q1
    if text.lower() == "start1":
        QUESTION = 1
        START = 1
        message = TemplateSendMessage(
            alt_text = "是否指定基酒?",
            template = ButtonsTemplate(
                thumbnail_image_url="https://i2.kknews.cc/SIG=3j4a194/qqo00048rs927p7qp3p.jpg",
                text="是否指定基酒?",
                actions=[
                    MessageTemplateAction(label="是", text="是"),
                    MessageTemplateAction(label="否", text="否")
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    # quick reply
    # P1
    elif text.lower() == "start2":
        QUESTION = 1
        START = 2
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="是否指定基酒?",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="是", text="是")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="否", text="否")
                        ),
                    ]
                )
            )
        )
    elif text.lower() == "否":
        if QUESTION == 1:
            QUESTION = 2
            # Q2 P2
            message = TemplateSendMessage(
                alt_text = "是否指定口味?",
                template = ConfirmTemplate(
                    text="是否指定口味?",
                    actions=[
                        MessageAction(label="是", text="是"),
                        MessageAction(label="否", text="否")
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        elif QUESTION == 2:
            QUESTION = 3
            # Q3 P3
            message = TemplateSendMessage(
                alt_text = "是否指定材料?",
                template = ConfirmTemplate(
                    text="是否指定材料?",
                    actions=[
                        MessageAction(label="是", text="是"),
                        MessageAction(label="否", text="否")
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        elif QUESTION == 3:
            QUESTION = 4
            # Q4 P4
            message = TemplateSendMessage(
                alt_text = "是否偏好氣泡感?",
                template = ConfirmTemplate(
                    text="是否偏好氣泡感?",
                    actions=[
                        MessageAction(label="是", text="是"),
                        MessageAction(label="否", text="否")
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        elif QUESTION == 4:
            QUESTION = 0
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text="推薦中，請稍候 ..."),
                    TextSendMessage(text="推薦您Mojito!")
                ]
            )
    elif text.lower() == "是":
        QUESTION = 0
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="還沒做啦 ..."),
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)