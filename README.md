script for [Zabbix](http://zabbix.com) notifications via [Telegram messenger](https://telegram.org)

##Requirements##

- Python 2.6+  
Note for 2.6:   
`pip install argparse`  

- TelegramBot account  
- Zabbix Administrator account

***


##Usage##

**1. Create your Telegram Bot**

How to create: https://core.telegram.org/bots

**2. Configuration:**  
Example of `zabbix-telegram.conf`:

>[telegram-bot]  
>api-key=your_telegram_bot_api_key
>
>[allowed-users]  
>zabbix-user-name=telegram user id or chat id

**2. Send message:**  
`zabbix-telegram.py username "subject" "body of message"`
  
***
  
###Zabbix configuration guide###

**1. Create new media type**

Go to `Zabbix -> Administration -> Media type`

example:

Name: Telegram  
Type: Script  
Script name: zabbix-telegram.sh  
Enabled: yes  

**2. Configurate zabbix user**

Open zabbix `user profile -> "Media" tab -> Add`

example:

Type: Telegram  
Send to: username  
Enabled: yes  

**3. Configure Zabbix-server**  
Look /etc/zabbix/zabbix_server.conf for `AlertScriptsPath`  
Default path: `/usr/lib/zabbix/alertscripts/`

**5.Deploy scripts**  
>cd /usr/lib/zabbix/alertscripts/  
>git clone https://github.com/lebe-dev/zabbix-telegram.git

Required files:
- zabbix-telegram.py  
- zabbix-telegram.conf  
- logging.conf  
- telegram_api.py  

Create bash script:  
`/usr/lib/zabbix/alertscripts/telegram.sh`  

`#!/bin/bash`  
`/usr/bin/python /usr/lib/zabbix/alertscripts/telegram.py --config /usr/lib/zabbix/alertscripts/zabbix-telegram.conf $1 "$2" "$3"`

Fix rights:

`chmod +x /usr/lib/zabbix/alertscripts/telegram.sh`  
`chown -R zabbix.zabbix /usr/lib/zabbix/alertscripts/`   

**6. Create or modify action**

`Zabbix -> Configuration -> Actions -> Create`

"Operations" tab -> select media type `Telegram`


##Troubleshootings##

- Edit `logging.conf`, set all levels to `DEBUG`
- Activate some test triggers for zabbix
- Check `zabbix-telegram.log`
