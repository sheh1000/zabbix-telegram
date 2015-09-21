import argparse
import httplib
import json
import os
import sys
import logging
import logging.config
import logging.handlers

from ConfigParser import ConfigParser
import urllib

__author__ = 'Evgeny Lebedev'

CONFIG_FILE = "zabbix-telegram.conf"


class UserNotFound(Exception):
    def __init__(self, msg):
        self.message = msg


class ServerErrorException(Exception):
    def __init__(self, msg):
        self.message = msg


class TelegramBot:
    def __init__(self, api_key):
        self.api_key = api_key

    def getUpdates(self):
        results = {}
        #{"ok":true,"result":[{"update_id":349851603,
        #"message":{"message_id":2,"from":{"id":1448214,"first_name":"Bob","last_name":"Global","username":"bob_global"},
        # "chat":{"id":1448214,"first_name":"Bob","last_name":"Global","username":"bob_global"},
        # "date":1442864448,"text":"tettt"}}]}

        users = {}

        try:
            cnn = httplib.HTTPSConnection("api.telegram.org")
            cnn.request("GET", "/bot%s/getUpdates" % self.api_key)
            resp = cnn.getresponse()
            data = resp.read()

            jsonResponse = json.loads(data)
            if 'result' in jsonResponse:
                for responseObject in jsonResponse['result']:
                    if 'message' in responseObject:
                        if 'from' in responseObject['message']:
                            if 'id' in responseObject['message']['from'] and 'username' in responseObject['message']['from']:
                                users[responseObject['message']['from']['username']] = responseObject['message']['from']['id']

            results = users
            log.debug('active users:')
            log.debug(results)
        except Exception as e:
            log.error(e.message)

        return results

    def sendMessage(self, target_id, subject, message):
        try:
            cnn = httplib.HTTPSConnection("api.telegram.org")
            params = urllib.urlencode({'chat_id': target_id, 'text': '*subject:* %s\n*message:* %s' % (subject, message), 'parse_mode':'Markdown'})
            headers = {"Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}
            cnn.request("POST", "/bot%s/sendMessage" % self.api_key, params, headers)

            response = cnn.getresponse()

            try:
                server_response = response.read()

                json_data = json.loads(server_response)

                if 'ok' in json_data:
                    if not json_data['ok'] is True:
                        raise ServerErrorException("Error response from server: %s" % server_response)
            except:
                raise ServerErrorException("Error response from server: %s" % server_response)

        except Exception as e:
            # TODO: handle exception
            log.error("Unable to send message: %s" % e.message)


def compile_config(args):
    parser = argparse.ArgumentParser(usage='use: -h for full help',
                                     description='zabbix script for telegram notifications',
                                     epilog='site: github.com/lebe-dev/zabbix-telegram')

    parser.add_argument('to', help="telegram username")
    parser.add_argument('subject', help="subject of message")
    parser.add_argument('message', help="text of message")

    options = parser.parse_args(args[1:])

    api_key = None
    target_id = None

    if os.path.isfile(CONFIG_FILE):
        config = ConfigParser()
        config.read(CONFIG_FILE)

        if config.has_section('telegram-bot'):
            api_key = config.get('telegram-bot', 'api-key')

            if config.has_section('allowed-users'):
                if config.has_option('allowed-users', options.to):
                    target_id = config.get('allowed-users', options.to)
                else:
                    raise UserNotFound('user "%s" not found, check config' % options.to)

    return api_key, target_id, options


if __name__ == '__main__':
    logging_handler = logging.handlers.RotatingFileHandler(filename='zabbix-telegram.log', mode='a', maxBytes=1024,
                                                           backupCount=1)

    fmt = logging.Formatter('%(asctime)s (%(levelname)s) > %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging_handler.setFormatter(fmt)

    logging.Formatter(fmt='%(asctime)s %(message)s')

    log = logging.getLogger(__name__)

    log.addHandler(logging_handler)
    log.setLevel(logging.DEBUG)

    try:
        api_key, target_id, options = compile_config(sys.argv)

        bot = TelegramBot(api_key)
        bot.getUpdates()

        bot.sendMessage(target_id, options.subject, options.message)
    except UserNotFound as e:
        log.error(e.message)

    except ServerErrorException as e:
        log.error(e.message)




