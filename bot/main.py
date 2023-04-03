import os
import re

import requests
from flask import Flask
from flask.views import MethodView
from flask import request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
API_URL = os.environ.get('API_URL')
TELEGRAM_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


def get_data_from_api(command):
    url = API_URL + command
    session = requests.Session()
    response = session.get(url).json()
    return response


def send_message(chat_id, message):
    session = requests.Session()
    response = session.get(TELEGRAM_URL, params=dict(chat_id=chat_id, text=message, parse_mode='Markdown'))
    return response.json()


def parse_text(text_msg):
    '''
    /start
    /help
    /city
    /language
    @kiyv
    @python
    '''
    addresses = {'city': '/cities', 'language': '/language'}
    command_pattern = r'/\w+'
    message = 'Bad Request'
    if '/' in text_msg:
        if '/start' in text_msg or '/help' in text_msg:
            message = '''
            To see which cities are available, send /city or /cities in a message.
To learn about available languages - send /language
To make a request for saved vacancies, send a space-separated message - @city @language.
For example like this - @kyiv @python
            '''
            return message
        else:
            command = re.search(command_pattern, text_msg).group().replace('/', '')
            command = addresses.get(command, None)
            return [command] if command else message
    else:
        return message


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
            if len(temp) > 10:
                send_message(chat_id, temp)
            elif len(temp) == 1:
                response = get_data_from_api(temp[0])
                if response:
                    message = ''
                    for dictionary in response:
                        message += '#' + dictionary['slug'] + '\n'
                        if temp[0] == '/language':
                            msg = 'Available languages: \n'
                        else:
                            msg = 'Available cities: \n'
                send_message(chat_id, msg + message)
        print(response)
        return '<h1> Hi Telegram_Class!!! </h1>'


app.add_url_rule('/TOKEN/', view_func=BotApi.as_view('bot'))

if __name__ == '__main__':
    app.run()
