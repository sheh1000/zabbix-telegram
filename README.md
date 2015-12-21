Send [Zabbix](http://zabbix.com) notifications via [Telegram messenger](https://telegram.org)

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
Script name: telegram.sh  
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

**5. Deploy scripts**  
  
`cd /usr/lib/zabbix/alertscripts/`    
`git clone https://github.com/lebe-dev/zabbix-telegram.git`

Required files:  
- zabbix-telegram.py    
- zabbix-telegram.conf  
- logging.conf  
- telegram_api.py  

Create bash script:  
`/usr/lib/zabbix/alertscripts/telegram.sh`  

`#!/bin/bash`  
`/usr/bin/python /usr/lib/zabbix/alertscripts/telegram.py --config /usr/lib/zabbix/alertscripts/zabbix-telegram.conf $1 "$2" "$3"`

**6. Fix rights:**  
  
`touch /home/zabbix/zabbix-telegram.log`  
`chmod ug=rw /home/zabbix/zabbix-telegram.log`  
^ depends on zabbix user home directory (check `/etc/passwd`)  
`chown -R zabbix.zabbix /usr/lib/zabbix/alertscripts/`
`chmod +x /usr/lib/zabbix/alertscripts/telegram.sh`  
`chown -R zabbix.zabbix /usr/lib/zabbix/alertscripts/`   

**7. Create or modify action**

`Zabbix -> Configuration -> Actions -> Create`

"Operations" tab -> select media type `Telegram`


##F.A.Q.##

**1. Where can i get telegram user id?**  
- Write one message at least to your Telegram bot  
- Set debug level to `DEBUG` (`logging.conf`)  
- Send trigger notification (action) from zabbix  
- Check debug.log, you can see picture like this:  
  
>2015-09-26 15:41:32,720 DEBUG > active users:  
>2015-09-26 15:41:32,720 DEBUG > {u'good_fella': 43578235}

`43578235` - is your id

##Troubleshootings##

- Edit `logging.conf`, set all levels to `DEBUG`
- Activate some test triggers for zabbix
- Check `zabbix-telegram.log`
