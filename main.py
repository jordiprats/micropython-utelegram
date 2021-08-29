import utelegram
import network
import utime
import json

def demo():
    config = {
        'ssid': 'DEMO',
        'password': 'PASSW0RD',
        'token': 'TOKEN',
    }
    try:
        with open('config.json', 'r') as f:
            config = json.loads(f.read())
    except:
        pass
    print('Config: {}'.format(config))
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.scan()
    sta_if.connect(config['ssid'], config['password'])

    print('WAITING FOR NETWORK')
    while not sta_if.isconnected():
        utime.sleep(1)

    def get_message(message):
        bot.send(message['message']['chat']['id'], message['message']['text'].upper())

    def reply_ping(message):
        print(message)
        bot.send(message['message']['chat']['id'], 'pong')

    if sta_if.isconnected():
        bot = utelegram.ubot(config['token'])
        bot.register('/ping', reply_ping)
        bot.set_default_handler(get_message)

        print('BOT LISTENING')
        while True:
            bot.update()
            utime.sleep(3)
    else:
        print('NOT CONNECTED - aborting')

if __name__ == "__main__":
    demo()