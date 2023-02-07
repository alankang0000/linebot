from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os, openai

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key =os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def echo(event):
    if (event.message.text[:6] == "@小小秘豬:"):
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt="How do I combine arrays?\n",
            temperature=0,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0,
            stop=["@小小秘豬:"]
            )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="I couldn’t catch what you said.")
            )
    return



if __name__ == "__main__":
    app.run()
