
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
import os
import re
import neologdn


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # text
    text = event.message.text
    text_norm = neologdn.normalize(text).lower()
    # response
    response = ''
    # 返答作成
    pattern_01 = "!!+|ー!"
    pattern_02 = "頑張|応援"
    pattern_03 = "おめでと|うれし|嬉し"
    pattern_04 = "愛子|あいこ|アイコ|愛|アイ|aiko"
    pattern_05 = "健吾|けんご|ケンゴ|kengo|シェフ|しぇふ"
    pattern_06 = "江城"    

    if re.match(pattern_01, text_norm):
        response = "ナイス!"
    elif re.match(pattern_02, text_norm):
        response = "ファイト!"
    elif re.match(pattern_03, text_norm):
        response = "グッド!"
    elif re.match(pattern_04, text_norm):
        response = "それは俺の嫁だ!"
    elif re.match(pattern_05, text_norm):
        response = "呼んだ？こんにちは健吾botです"
    elif re.match(pattern_06, text_norm):
        response = "Yes K&A"

    if response != '':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response))
    


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)