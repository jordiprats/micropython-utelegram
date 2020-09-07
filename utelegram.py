import time
import gc
import ujson
import urequests


class ubot:
    
    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot' + token

        self.commands = {}

        self.kbd = {
            'keyboard': [],
            'resize_keyboard': True,
            'one_time_keyboard': True}

        self.upd = {
            'offset': 0,
            'limit': 1,
            'timeout': 30,
            'allowed_updates': ['message']}

        self.last_read = 0

        messages = self.read_messages()
        if messages:
            for message in messages:
                if message['update_id'] > self.last_read:
                    self.last_read = message['update_id']


    def send(self, chat_id, text):
        data = {'chat_id': chat_id, 'text': text}
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = urequests.post(self.url + '/sendMessage', json=data, headers=headers)
            return True
        except:
            return False

    def read_messages(self):
        result = []
        try:
            update_messages = urequests.post(self.url + '/getUpdates', json=self.upd).json() 
            if 'result' in update_messages:
                for item in update_messages['result']:
                    if 'text' in item['message']:
                        result.append(item)
                
            return result
        except:
            return None

    def listen(self):
        while True:
            self.read_once()
            time.sleep(3)
            gc.collect()

    def read_once(self):
        messages = self.read_messages()
        if messages:
            for message in messages:
                if message['update_id'] > self.last_read:
                    self.message_handler(message)
                    self.last_read = message['update_id']
    
    def register(self, command, handler):
        self.commands[command] = handler

    def message_handler(self, message):
        parts = message['message']['text'].split(' ')
        if parts[0] in self.commands:
            self.commands[parts[0]](message)
