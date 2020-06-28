import json
import os
import random

class ChatClient():

    SPECIAL_CHATS_FILE = 'assets/special_searches.json'

    def __init__(self):
        with open(f"{os.path.dirname(__file__)}/{self.SPECIAL_CHATS_FILE}", 'r') as f:
            self.special_chats = json.load(f)

    def check_for_special_chats(self, message):
        for _, item in self.special_chats.items():
            # If the special case tells us to ignore case, then set it to lower
            msg = message.content if not item['ignoreCase'] else message.content.lower()

            # Check if the message contains any of the keys
            if bool([x for x in item['keys'] if(x in msg)]):
                res = item['responses'][random.randint(0,len(item['responses']) - 1)]
                if item['tagUser']:
                    res = f"{message.author.mention}\n{res}"
                return res

        # If no matches, return None to signal this
        return None
