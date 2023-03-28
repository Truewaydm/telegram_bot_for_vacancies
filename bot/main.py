from flask import Flask
from flask.views import MethodView
from flask import request

app = Flask(__name__)


def parse_text(text_msg):
    '''
    /start
    /help
    /city
    /language
    @kiyv
    @python
    '''
    global message
    if '/' in text_msg:
        if '/start' in text_msg or '/help' in text_msg:
            message = '''To see which cities are available, send /city in a message.
             To learn about available languages - send /language
             To make a request for saved vacancies, send a space-separated message - @city @language.
             For example like this - @kyiv @python '''
        return message
    else:
        return None


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        response = request.get_json()
        print(response)
        return '<h1> Hi Telegram!!! </h1>'
    return '<h1> Hi BOT!!! </h1>'


class BotApi(MethodView):

    def get(self):
        return '<h1> Hi BOT_Class!!! </h1>'

    def post(self):
        response = request.get_json()
        text_msg = response['message']['text']
        chat_id = response['message']['chat']['id']
        temp = parse_text(text_msg)
        if temp:
            send_message(chat_id, temp)
        print(response)
        return '<h1> Hi Telegram_Class!!! </h1>'


app.add_url_rule('/TOKEN/', view_func=BotApi.as_view('bot'))

if __name__ == '__main__':
    app.run()
