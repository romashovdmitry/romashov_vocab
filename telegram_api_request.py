import json
import requests
from time import sleep

class ButtonCreate():
    ''' 
    Class for making request to Telegram API and following sending message. 
    https://core.telegram.org/bots/api#sendmessage
    
    '''

    def __init__(self, texts_of_button: list, chat_id: int, message_text: str):
        
        self.texts_of_button = texts_of_button
        self.message_text = message_text
        self.chat_id = chat_id
    
    def return_button(self):
        
        texts_of_button = self.texts_of_button
        buttons = []
        api_url = 'https://api.telegram.org/bot<token>/sendMessage'        
        while len(texts_of_button) > 1:
            buttons.append(
                [
                {'text': str(texts_of_button[0])},
                {'text': str(texts_of_button[1])}
            ]
        )
            texts_of_button = texts_of_button[2:]
        if len(texts_of_button) == 1:
            buttons.append([{'text': str(texts_of_button[0])}])
        buttons = json.dumps({
                "keyboard": buttons,
                'resize_keyboard': True
            })
        button_params = {
            'chat_id': self.chat_id,
            'text': self.message_text,
            'reply_markup': buttons
        }
        requests.post(url=api_url, params=button_params)