# micropython-utelegram

This library provides a **microPython** interface for for a subset of the **Telegram Bot API**. Have been tested on an **ESP32** but should work just fine on an **ESP8266**

## Your first bot

On the demo folder you will find an example bot. 

First you'll need to create a new bot using the **BotFather** to get a token for your bot. Once you have it rename the **config.py-demo** and set the variables (WiFI SID/password and your bot token):

```
wifi_config = {
    'ssid':'DEMO',
    'password':'PASSW0RD'
}

utelegram_config = {
    'token': 'TOKEN'
}
```

If you have your **ESP32** connected as **/dev/ttyUSB0** you can use the upload.sh script to upload the bot code to your **micropython enabled ESP32**:

```
./upload.sh
```

### Example bot code

#### Initialize bot

To create a new bot you just need to create a ubot object passing the token the **BotFather** have provided:

```
bot = utelegram.ubot(utelegram_config['token'])
```

#### Register handlers

Handlers will receive the raw message as a parameter:

```
def reply_ping(message):
    bot.send(message['message']['chat']['id'], 'pong')
```

Messages will be in the following format:

```
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

```
bot.register('/ping', reply_ping)
```

And optionally set a **default handler** for any other message:

```
bot.set_default_handler(get_message)
```

### Reply to messages

Using the send function we can reply to messages, the parameters are:

* **chat ID**: chat ID is the same as the user ID except for group chats
* **message**: text to send

For example, we can use the incoming message to get the **chat_id** to reply to:

```
bot.send(message['message']['chat']['id'], 'pong')
```

### Bot loop

We can either let the bot loop but itself to reply to messages:

```
bot.listen()
```

Or we can loop manually using the **read_once()** function:

```
bot.read_once()
```

Using this method you should add a sleep between each time we poll the Telegram API