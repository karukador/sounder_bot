URL = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
VOICE = "filipp"  # желаемый голос можно выбрать в списке - https://yandex.cloud/ru/docs/speechkit/tts/voices
LANGUAGE = "ru-RU"

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice"]
ADMIN_ID: int = 1234
MAX_USER_TTS_SYMBOLS = 500
MAX_TTS_SYMBOLS = 2000

DB_NAME = "speech_kit.db"
