import requests
from system_config import URL, VOICE, LANGUAGE
from config import FOLDER_ID, IAM_TOKEN
import logging


def text_to_speech(text):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}'}
    data = {
        'text': text,
        'lang': LANGUAGE,
        'voice': VOICE,
        'folderId': FOLDER_ID}
    response = requests.post(URL, headers=headers, data=data)

    if response.status_code == 200:
        return True, response.content  # Возвращаем голосовое сообщение
    else:
        return False, logging.debug("При запросе в SpeechKit возникла ошибка")
