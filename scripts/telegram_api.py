import urllib
import httplib
import json
import logging


class TelegramApi:
    def __init__(self, api_host, api_key):
        self.api_host = api_host
        self.api_key = api_key

        self.logger = logging.getLogger("logfile")

    def get_request(self, method='GET', command=None, params=None, headers={}):
        data = None

        try:
            cnn = httplib.HTTPSConnection(self.api_host)
            cnn.request(method, self.compile_url(self.api_key, command), params, headers)
            resp = cnn.getresponse()
            data = resp.read()
            cnn.close()
        except Exception as e:
            raise IOError(e.message)

        return json.loads(data)

    @staticmethod
    def compile_url(api_key, command):
        if not api_key:
            raise ValueError("Invalid api_key value")

        if not command:
            raise ValueError("Invalid command value")

        return "/bot%s/%s" % (api_key, command)

    def get_updates(self):
        results = {}

        users = {}

        response = self.get_request("GET", "getUpdates")

        if response:

            try:
                if 'result' in response:
                    for responseObject in response['result']:
                        message_from = responseObject['message']['from']
                        users[message_from['username']] = message_from['id']
            except:
                raise ValueError("Invalid response: %s" % response)

        results = users
        self.logger.debug('active users:')
        self.logger.debug(results)

        return results

    def send_message(self, target_id, subject, message):
        params = urllib.urlencode(
            {'chat_id': target_id,
             'text': '*subject:* %s\n*message:* %s' % (subject, message),
             'parse_mode': 'Markdown',
             'disable_web_page_preview': 'true'})

        headers = {"Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}

        response = self.get_request("POST", "sendMessage", params, headers)

        if not response['ok'] is True:
            raise ValueError("Invalid response from server: %s" % response)