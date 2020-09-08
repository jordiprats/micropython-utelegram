import time
import gc
import ujson
import urequests


class ubot:
    
    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot' + token

        self.commands = {}

        self.default_handler = None

        self.message_offset = 0

        messages = self.read_messages()
        if messages:
            for message in messages:
                if message['update_id'] > self.message_offset:
                    self.message_offset = message['update_id']


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
        self.query_updates = {
            'offset': self.message_offset,
            'limit': 1,
            'timeout': 30,
            'allowed_updates': ['message']}

        try:
            update_messages = urequests.post(self.url + '/getUpdates', json=self.query_updates).json() 
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
                if message['update_id'] > self.message_offset:
                    self.message_handler(message)
                    self.message_offset = message['update_id']
    
    def register(self, command, handler):
        self.commands[command] = handler

    def set_default_handler(self, handler):
        self.default_handler = handler

    def message_handler(self, message):
        parts = message['message']['text'].split(' ')
        if parts[0] in self.commands:
            self.commands[parts[0]](message)
        else:
            if self.default_handler:
                self.default_handler(message)
