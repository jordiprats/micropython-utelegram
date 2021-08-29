# micropython-utelegram

This library provides a **microPython** interface for for a subset of the **Telegram Bot API**. Have been tested on an **ESP32**.

Note that this module can't work on ESP8266 because axTLS version used currently by uPy doesn't support ciphersuites of telegram bot api 
<br />(see: https://docs.micropython.org/en/latest/esp8266/general.html?highlight=certificate#ssl-tls-limitations and https://forum.micropython.org/viewtopic.php?t=3246).

## Your first bot

You will find an example bot. 

First you'll need to edit the config dictionary on the main.py file, or create a new file config.json with the needed data about your wifi connection and the token of your bot.

```python
config = {
    'ssid': 'DEMO',
    'password': 'PASSW0RD',
    'token': 'TOKEN'
}
```
```config.json
{
    "ssid": "DEMO",
    "password": "PASSW0RD",
    "token": "TOKEN"
}
```
### Example bot code

#### Initialize bot

To create a new bot you just need to create a ubot object passing the token the **BotFather** have provided:

```python
bot = utelegram.ubot(utelegram_config['token'])
```

#### Register handlers

Handlers will receive the raw message as a parameter:

```python
def reply_ping(message):
    bot.send(message['message']['chat']['id'], 'pong')
```

Messages will be in the following format:

```python
{
   "update_id":302445393,
   "message":{
      "message_id":1492,
      "from":{
         "id":123456789,
         "is_bot":False,
         "language_code":"en",
         "first_name":"Jordi"
      },
      "text":"/ping",
      "date":1599563930,
      "entities":[
         {
            "offset":0,
            "length":5,
            "type":"bot_command"
         }
      ],
      "chat":{
         "id":123456789,
         "type":"private",
         "first_name":"Jordi"
      }
   }
}
```

You can register handlers using the **register** method:

```python
bot.register('/ping', reply_ping)
```

And optionally set a **default handler** for any other message:

```python
bot.set_default_handler(get_message)
```

### Reply to messages

Using the send function we can reply to messages, the parameters are:

* **chat ID**: chat ID is the same as the user ID except for group chats
* **message**: text to send

For example, we can use the incoming message to get the **chat_id** to reply to:

```python
bot.send(message['message']['chat']['id'], 'pong')
```

### Bot loop

We can either let the bot loop but itself to reply to messages:

```python
bot.listen_blocking()
```

Or we can loop manually using the **update()** function:

```python
bot.update()
```

Using this method you should add a sleep between each time we poll the Telegram API

## Other examples

* [Telegram integrated countdown timer](https://github.com/jordiprats/micropython-remainigdays)
