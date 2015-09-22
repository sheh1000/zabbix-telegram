import argparse

import os
import sys
import logging
import logging.config
import logging.handlers

from telegram_api import TelegramApi, ServerErrorException

from ConfigParser import ConfigParser

VERSION = '1.0.0'

__author__ = 'Evgeny Lebedev'

TELEGRAM_API_HOST = 'api.telegram.org'


class Application:
    def __init__(self, opts):
        self.options = opts

        self.logger = logging.getLogger("logfile")

        self.api_key = None
        self.target_id = None

        self.configFilePath = 'zabbix-telegram.conf'

        self.compile_config()

    def compile_config(self):
        # TODO: refactoring required
        if self.options.configFilePath:
            self.logger.debug("Configuration file path: %s" % options.configFilePath)
            if os.path.isfile(self.options.configFilePath):
                self.configFilePath = self.options.configFilePath
            else:
                self.logger.error("Not found")
                sys.exit(1)

        if os.path.isfile(self.configFilePath):
            config = ConfigParser()
            config.read(self.configFilePath)

            telegram_section = 'telegram-bot'
            allowed_users_section = 'allowed-users'

            if config.has_section(telegram_section):
                self.api_key = config.get(telegram_section, 'api-key')

                if config.has_section(allowed_users_section):
                    if config.has_option(allowed_users_section, options.to):
                        self.target_id = config.get(allowed_users_section, options.to)
                    else:
                        raise ValueError('user "%s" not found, check config' % options.to)

        else:
            self.logger.error("Configuration file not found")
            sys.exit(1)


if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    log = logging.getLogger('logfile')

    parser = argparse.ArgumentParser(usage='<to> "<subject>" "<message>"',
                                     description='Zabbix script for notifications via Telegram Messenger',
                                     epilog='site: github.com/lebe-dev/zabbix-telegram', version=VERSION)

    parser.add_argument('to', help="user alias from configuration file")
    parser.add_argument('subject', help="subject of message")
    parser.add_argument('message', help="text of message")

    parser.add_argument("-c", "--config", dest="configFilePath", help="path to configuration file")

    options = parser.parse_args(sys.argv[1:])

    try:
        app = Application(options)

        api = TelegramApi(TELEGRAM_API_HOST, app.api_key)

        api.get_updates()

        api.send_message(app.target_id, options.subject, options.message)

    except ValueError as e:
        log.error(e.message)

    except ServerErrorException as e:
        log.error(e.message)




