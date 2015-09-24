import unittest
import imp
import logging
import logging.config

telegram_module = imp.load_source('telegram_api', '../scripts/telegram_api.py')

user_id = 5464535

class TelegramApiMock(telegram_module.TelegramApi):
    def get_request(self, method='GET', command=None, params=None, headers={}):
        response_data = {'ok': False, 'result': [{'message': {'from': {'username': 'morhein', 'first_name': 'John',
                                                                        'last_name': 'Morhein', 'id': user_id},
                                                               'chat': {'username': 'morhein', 'first_name': 'John',
                                                                        'last_name': 'Morhein', 'id': user_id}}
                                                    }]}

        return response_data


class TestTelegramApi(unittest.TestCase):
    def setUp(self):
        logging.config.fileConfig('../scripts/logging.conf')

        self.api_key = "1234567"
        self.api = TelegramApiMock("api.telegram.org", self.api_key)

    def test_compile_url(self):
        self.assertEqual("/bot%s/getUpdates" % self.api_key, self.api.compile_url(self.api.api_key, "getUpdates"))

    def test_compile_invalid_params(self):
        self.assertRaises(ValueError, self.api.compile_url, None, "getUpdates")
        self.assertRaises(ValueError, self.api.compile_url, self.api_key, None)

    def test_get_updates(self):
        results = self.api.get_updates()

        self.assertTrue('morhein' in results)
        self.assertEqual(results['morhein'], user_id)

    def test_send_message(self):
        self.assertRaises(ValueError, self.api.send_message, None, None, None)


if __name__ == '__main__':
    unittest.main()
