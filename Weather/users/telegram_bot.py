import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{self.token}/'

    def send_message(self, chat_id, message):
        url = f'{self.base_url}sendMessage'
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=data)
        return response.json()



TOKEN = 'your_bot_token'
bot = TelegramBot(TOKEN)