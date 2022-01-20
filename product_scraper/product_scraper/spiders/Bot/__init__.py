import time

import flask
import telebot
import logging

from flask import request

import Config
from Drivers_bot import bot as driver
#from Clients_bot import bot as client

app = flask.Flask(__name__)

driver.remove_webhook()
driver.set_webhook(url=Config.URL_BASE+"/"+Config.token_drivers_bot)

time.sleep(5)

#client.remove_webhook()
#client.set_webhook(url=Config.URL_BASE+"/"+Config.token_clients_bot)

logger = logging.getLogger('YaTaxist')
logger.setLevel(logging.DEBUG)


@app.route("/"+Config.token_drivers_bot, methods=['POST'])
def drivers_webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        driver.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


'''@app.route("/"+Config.token_clients_bot, methods=['POST'])
def clients_webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        client.process_new_updates([update])
        return ''
    else:
        flask.abort(403)'''


@app.route('/api/save/')
def save():
    if request.values["apikey"] == Config.apikey:
        return str(driver.save())
    else:
        flask.abort(403)


@app.route('/')
def hello_world():
    return "Hello!"


@app.route('/test/')
def test():
    import json
    from flask import Response
    with open(driver.filename) as f:
        ret = json.dumps(json.load(f))
        resp = Response(response=ret,
                        status=200,
                        mimetype="application/json")
        return resp


if __name__ == '__main__':
    app.run()
