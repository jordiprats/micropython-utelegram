import time
import gc
import ujson
import urequests

class ubot:
    class DEBUG_LEVELS:
        DISABLED = 0
        INFO = 1
        VERBOSE = 2
        DEBUG = 3
    def __init__(self, token, offset=-1, debuglevel=DEBUG_LEVELS.DEBUG):
        self.DEBUG_LEVEL = debuglevel
        self.url = 'https://api.telegram.org/bot' + token
        self.commands = {}
        self.default_handler = None
        self.message_offset = offset-1
        self.sleep_btw_updates = 3

    def myprint(self, level, txt):
        if level <= self.DEBUG_LEVEL:
            print(txt)

    def send(self, chat_id, text):
        data = {'chat_id': chat_id, 'text': text}
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = urequests.post(self.url + '/sendMessage', json=data, headers=headers)
            response.close()
            self.myprint(self.DEBUG_LEVELS.INFO, 'Send: {}'.format(data))
            return True
        except:
            self.myprint(self.DEBUG_LEVELS.INFO, 'Send failed! Data: {}'.format(data))
            return False

    def read_messages(self):
        result = []
        query_updates = {
            'offset': self.message_offset + 1,
            'limit': 1,
            'timeout': 5,
            'allowed_updates': ['message']}
        header = {'Content-Type': 'application/json'}
        try:
            self.myprint(self.DEBUG_LEVELS.DEBUG, 'Request new messages: {}'.format(query_updates))
            update_messages = urequests.post(self.url + '/getUpdates', json=query_updates, headers=header).json()
            if 'result' in update_messages:
                for item in update_messages['result']:
                    self.myprint(self.DEBUG_LEVELS.INFO, 'Received message: {}'.format(item))
                    result.append(item)
            return result
        except (ValueError):
            self.myprint(self.DEBUG_LEVELS.INFO, 'Received message ValueError.')
            return None
        except (OSError):
            self.myprint(self.DEBUG_LEVELS.INFO, 'Received message OSError')
            print("OSError: request timed out")
            return None

    def listen_blocking(self):
        while True:
            self.myprint(self.DEBUG_LEVELS.VERBOSE, 'Check for updates.')
            self.read_once()
            time.sleep(self.sleep_btw_updates)
            gc.collect()

    def update(self):
        self.myprint(self.DEBUG_LEVELS.VERBOSE, 'Check for updates.')
        self.read_once()
        gc.collect()

    def read_once(self):
        messages = self.read_messages()
        if messages:
            if self.message_offset == 0:
                self.message_offset = messages[-1]['update_id']
                self.myprint(self.DEBUG_LEVELS.DEBUG, 'New message_offset: {}'.format(self.message_offset))
                self.message_handler(messages[-1])
            else:
                for message in messages:
                    if message['update_id'] > self.message_offset:
                        self.message_offset = message['update_id']
                        self.myprint(self.DEBUG_LEVELS.DEBUG, 'New message_offset: {}'.format(self.message_offset))
                        self.message_handler(message)
                        #break

    def register(self, command, handler):
        self.commands[command] = handler

    def set_default_handler(self, handler):
        self.default_handler = handler

    def set_sleep_btw_updates(self, sleep_time):
        self.sleep_btw_updates = sleep_time

    def message_handler(self, message):
        self.myprint(self.DEBUG_LEVELS.DEBUG, 'Handle message: {}'.format(message))
        if 'text' in message['message']:
            parts = message['message']['text'].split(' ')
            if parts[0] in self.commands:
                self.commands[parts[0]](message)
            else:
                if self.default_handler:
                    self.default_handler(message)
