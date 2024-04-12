import telebot
import logging
from database import create_table, insert_row, count_all_symbol
from speechkit import text_to_speech
from telebot.types import BotCommand, BotCommandScope, ReplyKeyboardMarkup
from system_config import admin_id, MAX_USER_TTS_SYMBOLS, MAX_TTS_SYMBOLS
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv("TOKEN")
admin_id = int(admin_id)
bot = telebot.TeleBot(token=TOKEN)

# Создание таблицы в БД
create_table()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H",
    filename="log_file.log",
    filemode="w",
    force=True)


# Команда /debug с доступом только для админов
@bot.message_handler(commands=['debug'])
def send_logs(message):
    user_id = message.chat.id

    if user_id == admin_id:
        try:

            with open("log_file.txt", "rb") as f:
                bot.send_document(message.chat.id, f)
                logging.info("логи отправлены")
        except telebot.apihelper.ApiTelegramException:

            bot.send_message(message.chat.id, "Логов пока нет.")

    else:
        bot.send_message(message.chat.id, "У Вас недостаточно прав для использования этой команды.")
        logging.info(f"{user_id} пытался получить доступ к логам, не являясь админом")


# клавиатура
main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("📊 Статистика", "🗣️ Озвучить")


# Команда /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    logging.info("Отправка приветственного сообщения")
    bot.reply_to(
        message,
        "Привет! Я бот озвучки текста с помощью SpeechKit. Нажми на кнопку '🗣️ Озвучить' и введи текст для озвучки.",
        reply_markup=main_menu_keyboard)
    commands = [  # Установка списка команд с областью видимости и описанием
        BotCommand('start', 'запуск бота'),
        BotCommand('help', 'основная информация о боте'),
        BotCommand('tts', 'озвучить текст')]
    bot.set_my_commands(commands)
    BotCommandScope('private', chat_id=message.chat.id)


# команда /help
@bot.message_handler(commands=["help"])
def about_bot(message):
    bot.send_message(message.chat.id, 'Так как я использую платные ресурсы для взаимодействия с нейросетью, то у вас '
                                      '<b>ограниченное количество</b> символов для озвучки.\n\n'
                                      '<b>Что такое SpeechKit?</b>\n'
                                      '<b>SpeechKit</b> - это набор инструментов для работы с естественным языком, '
                                      'разработанный компанией Яндекс. Он включает в себя распознавание речи, '
                                      'синтез речи, а также API для управления устройствами через голосовые '
                                      'команды.\n\n'
                                      'Информацию о том, сколько ресурсов вы уже потратили, вы сможете найти, нажав '
                                      'на кнопку <b>"📊 Статистика"</b>.\n'
                                      '<b>🗣️ Озвучить</b> - начните озвучивать текст.',
                     reply_markup=main_menu_keyboard, parse_mode="html")


@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "🗣️ озвучить")
@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправляйте текст строго на выбранном языке. Также, для большего очеловеченья аудио '
                              'можно использовать следующее:\n\n'
                              'Для ударения поставьте "+". Например:\nЯ хочу сделать удар+ение на букву е.\n\n'
                              'Для того, чтобы сделать акцент используйте "** **". Например: \nЯ хочу '
                              '**акцентировать**.\n\n'
                              'sil<[300]> - добавляет паузу длительностью в 300 миллисекунд. Например:\n А вот здесь '
                              'sil<[300]> сделаем паузу.\n\n'
                              '<[tiny]>, <[small]>, <[medium]>, <[large]>, <[huge]> также указывает на паузу '
                              'различной длительности.\n\n'
                              '⏸️ Паузы помогут сделать речь более разделенной и понятной.')
    bot.send_message(user_id, 'Отправь следующим сообщением текст, чтобы я его озвучил!')
    bot.register_next_step_handler(message, tts)


# вызов статистики
@bot.message_handler(content_types=["text"], func=lambda message: message.text.lower() == "📊 статистика")
def send_stats(message):
    user_id = message.from_user.id
    text_symbols = len(message.text)

    # Функция из БД для подсчёта всех потраченных пользователем символов
    all_symbols = count_all_symbol(user_id) + int(
        text_symbols) - 12  # каким-то образом начальное использование символов равняется 12, поэтому вычтем

    bot.send_message(message.chat.id, "Ваша статистика:\n\n"
                                      f"<b>Символов израсходовано:</b> {all_symbols}\n"
                                      f"<b>Максимальное количество символов:</b> {MAX_USER_TTS_SYMBOLS}\n\n",
                     parse_mode="html")


@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь следующим сообщеним текст, чтобы я его озвучил!')
    bot.register_next_step_handler(message, tts)


# функция, направляющая аудио от speechkit
def tts(message):
    user_id = message.from_user.id
    text = message.text

    # Проверка, что сообщение действительно текстовое
    if message.content_type != 'text':
        bot.send_message(user_id, 'Отправь текстовое сообщение')
        return

        # Считаем символы в тексте и проверяем сумму потраченных символов
    text_symbol = is_tts_symbol_limit(message, text)
    if text_symbol is None:
        return

    # Записываем сообщение и кол-во символов в БД
    insert_row(user_id, text, text_symbol)

    success, response = text_to_speech(message.text)

    if success:
        with open('output.ogg', 'wb') as audio_file:
            audio_file.write(response)
        voice = open('output.ogg', 'rb')
        bot.send_voice(chat_id=message.chat.id, voice=voice)
        voice.close()
        logging.info(f"{user_id} получил своё аудио")
    else:
        bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так!")


# функция контроля токенов
def is_tts_symbol_limit(message, text):
    user_id = message.from_user.id
    text_symbols = len(text)

    # Функция из БД для подсчёта всех потраченных пользователем символов
    all_symbols = count_all_symbol(user_id) + text_symbols

    # Сравниваем all_symbols с количеством доступных пользователю символов
    if all_symbols >= MAX_USER_TTS_SYMBOLS:
        msg = (f"Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols} символов. "
               f"Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols}")
        bot.send_message(user_id, msg)
        return None

    # Сравниваем количество символов в тексте с максимальным количеством символов в тексте
    if text_symbols >= MAX_TTS_SYMBOLS:
        msg = f"Превышен лимит SpeechKit TTS на запрос {MAX_TTS_SYMBOLS}, в сообщении {text_symbols} символов"
        bot.send_message(user_id, msg)
        return None
    return len(text)


CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice"]


@bot.message_handler(content_types=CONTENT_TYPES)
def any_msg(message):
    bot.send_message(message.chat.id, 'Если хотите озвучить текст, то сначала нажмите на кнопку "🗣️ Озвучить"',
                     reply_markup=main_menu_keyboard)


# запуск бота 🎉
if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.infinity_polling()
