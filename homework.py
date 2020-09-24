import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client


def get_status(user_id):
    load_dotenv()
    vk_token = os.getenv('vk_token')
    vk_fields = os.getenv('vk_fields')
    vk_v = os.getenv('vk_v')

    params = {
        'user_ids': user_id,
        'access_token': vk_token,
        'fields': 'online',
        'v': '5.92',
    }
    user_info = requests.post('https://api.vk.com/method/users.get',
                              params=params)
    online_status = user_info.json()['response'][0]['online']
    return online_status  # Верните статус пользователя в ВК


def sms_sender(sms_text):
    load_dotenv()
    twilio_token = os.getenv('twilio_token')
    twilio_sid = os.getenv('twilio_sid')
    NUMBER_FROM = os.getenv('NUMBER_FROM')
    NUMBER_TO = os.getenv('NUMBER_TO')

    client = Client(twilio_sid, twilio_token)

    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )
    return message.sid  # Верните sid отправленного сообщения из Twilio


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
