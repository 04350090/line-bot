
# write server package: flask(for app), django(for website)

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('H+PBv1oRz5IGW1lSXYd1j+Q9TVebCOPgOrf388xD+taSYLCDnt3Hblt6Djmrz6+eXKscZdLByG9qGKxmAkp+FZadSpaIt/I9T4pCmZ+Doal5WCUDcKnBRjnr6+mL5ieSJbdKylW+5QoJ37epvEXGYgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7a2f582011c69a2da75db8aabd8663a0')


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
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if "睡覺" in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)

    if msg in ['hi', 'hello', '妳好', '你好', 'HI', 'Hi', 'Hello']:
        r = '嗨'
    elif msg == '你是誰':
        r = '我是機器人'
    elif ['估價', '報價', '價格', '多少錢'] in msg:
        r = '您是想獲得產品報價，是嗎？'
    elif msg in ['是的', '是', '對的']:
        r = '請稍等，會有專人為您服務'
    else:
        r = '很抱歉，您說什麼'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()