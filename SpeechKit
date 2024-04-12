import requests
from dotenv import load_dotenv
from os import getenv
from system_config import URL, voice
import logging

load_dotenv()
folder_id = getenv("folder_id")
iam_token = getenv("iam_token")


def text_to_speech(text):
    headers = {
        'Authorization': f'Bearer {iam_token}'}
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': voice,
        'folderId': folder_id}
    response = requests.post(URL, headers=headers, data=data)

    if response.status_code == 200:
        return True, response.content  # Возвращаем голосовое сообщение
    else:
        return False, logging.debug("При запросе в SpeechKit возникла ошибка")
