import logging
import logging.config
import unittest
import imp

from ConfigParser import ConfigParser


class Options:
    to = 'z@s.com'
    subject = 'subject'
    message = 'message'
    config_file_path = 'zabbix-telegram.conf'


class TestApplication(unittest.TestCase):
    def setUp(self):
        logging.config.fileConfig('../scripts/logging.conf')
        self.application_module = imp.load_source('zabbix-telegram', '../scripts/zabbix-telegram.py')

        self.config = ConfigParser()

        telegram_section = "telegram-bot"
        allowed_users_section = "allowed-users"

        self.config.add_section(telegram_section)
        self.config.add_section(allowed_users_section)

        self.config.set(telegram_section, 'api-key', '1111111111X')
        self.config.set(allowed_users_section, 'z@s.com', '1448214')

        self.opts = Options()

    def test_compile_config2(self):
        app = self.application_module.Application(self.config, self.opts)

        self.assertEqual(app.api_key, '1111111111X')

    def test_unavailable_user(self):
        self.opts.to = 'bbb@a.com'

        self.assertRaises(self.application_module.InvalidConfigurationException,
                          self.application_module.Application, self.config, self.opts)

    def test_compile_config(self):
        self.assertRaises(IOError, self.application_module.compile_config, 'zzzasdasd4545234534.conf')

        config = self.application_module.compile_config('')

        # self.assertEqual()

    def test_invalid_config_file(self):
        config = ConfigParser()
        config.add_section("telegram-bot")
        config.add_section("allowed-users")

        app = self.application_module.Application(self.config, self.opts)

        app.config = config

        self.assertRaises(self.application_module.InvalidConfigurationException, app.load_configuration, self.opts.to)
