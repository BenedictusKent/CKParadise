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

from linebot.models import (
    RichMenu,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    URIAction
)
from linebot.models.actions import RichMenuSwitchAction
from linebot.models.rich_menu import RichMenuAlias

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
PREFERENCE = None

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global QUESTION
    global PREFERENCE
    text = event.message.text
    # Q1
    if text.lower() == "start":
        QUESTION = 1
        message = TemplateSendMessage(
            alt_text = "?????????????",
            template = ButtonsTemplate(
                # thumbnail_image_url="https://i2.kknews.cc/SIG=3j4a194/qqo00048rs927p7qp3p.jpg",
                text="?????????????",
                actions=[
                    MessageTemplateAction(label="???(???????????????)", text="???"),
                    MessageTemplateAction(label="???(???????????????)", text="???"),
                    MessageTemplateAction(label="???(???????????????)", text="???"),
                    MessageTemplateAction(label="??????(???????????????)", text="??????"),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    # Q2
    elif ((text.lower()=="???") or (text.lower()=="???") or (text.lower()=="???") or (text.lower()=="??????")) and QUESTION == 1:
        QUESTION = 2
        message = TemplateSendMessage(
            alt_text = "3???1",
            template = ButtonsTemplate(
                # thumbnail_image_url="https://i2.kknews.cc/SIG=3j4a194/qqo00048rs927p7qp3p.jpg",
                text="3???1",
                actions=[
                    MessageTemplateAction(label="??????", text="??????"),
                    MessageTemplateAction(label="?????????", text="?????????"),
                    MessageTemplateAction(label="?????????", text="?????????")
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    # Q2a
    elif (text.lower()=="??????") and QUESTION == 2:
        QUESTION = 3
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="?????????",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="????????????", text="????????????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="?????????", text="?????????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="????????????", text="????????????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                    ]
                )
            )
        )
    # Q2b
    elif (text.lower()=="?????????") and QUESTION == 2:
        QUESTION = 3
        message = TemplateSendMessage(
            alt_text = "????????????",
            template = ButtonsTemplate(
                # thumbnail_image_url="https://i2.kknews.cc/SIG=3j4a194/qqo00048rs927p7qp3p.jpg",
                text="????????????",
                actions=[
                    MessageTemplateAction(label="??????", text="??????"),
                    MessageTemplateAction(label="??????", text="??????"),
                    MessageTemplateAction(label="?????????", text="?????????"),
                    MessageTemplateAction(label="??????", text="??????")
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    # Q2c
    elif (text.lower()=="?????????") and QUESTION == 2:
        QUESTION = 3
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="????????????",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="??????", text="??????")
                        ),
                    ]
                )
            )
        )
    # Answer
    elif QUESTION == 3:
        QUESTION = 0
        PREFERENCE = text
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text="?????????????????????..."),
                TextSendMessage(text="????????????Mojito!"),
            ]
        )
    # Anything else
    else:
        QUESTION = 0
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="??????????????????"),
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)