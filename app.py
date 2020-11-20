
# write server package: flask(for app), django(for website)

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()