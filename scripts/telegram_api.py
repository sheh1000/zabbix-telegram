import urllib
import httplib
import json
import logging


class ServerErrorException(Exception):
    pass


class TelegramApi:
    def __init__(self, api_host, api_key):
        self.api_host = api_host
        self.api_key = api_key

        self.logger = logging.getLogger("logfile")

    def __get_request(self, method='GET', command=None, params=None, headers={}):
        data = None

        try:
            cnn = httplib.HTTPSConnection(self.api_host)
            cnn.request(method, "/bot%s/%s" % (self.api_key, command), params, headers)
            resp = cnn.getresponse()
            data = resp.read()
            cnn.close()
        except Exception as e:
            self.logger.error(e.message)

        # TODO: add checks

        return data

    def get_updates(self):
        results = {}

        users = {}

        try:
            data = self.__get_request("GET", "getUpdates")

            if data:
                # todo: refactoring required
                json_response = json.loads(data)
                if 'result' in json_response:
                    for responseObject in json_response['result']:
                        if 'message' in responseObject:
                            if 'from' in responseObject['message']:
                                if 'id' in responseObject['message']['from'] and 'username' in responseObject['message'][
                                    'from']:
                                    users[responseObject['message']['from']['username']] = \
                                        responseObject['message']['from']['id']

            results = users
            self.logger.debug('active users:')
            self.logger.debug(results)

        except Exception as e:
            self.logger.error(e.message)

        return results

    def send_message(self, target_id, subject, message):
        try:
            params = urllib.urlencode(
                {'chat_id': target_id, 'text': '*subject:* %s\n*message:* %s' % (subject, message),
                 'parse_mode': 'Markdown'})

            headers = {"Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}

            data = self.__get_request("POST", "sendMessage", params, headers)

            try:
                json_data = json.loads(data)

                if 'ok' in json_data:
                    if not json_data['ok'] is True:
                        raise ServerErrorException("Error response from server: %s" % data)
            except:
                raise ServerErrorException("Error response from server: %s" % data)

        except Exception as e:
            # TODO: handle exception
            self.logger.error("Unable to send message: %s" % e.message)