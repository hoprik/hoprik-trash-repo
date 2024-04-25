import telebot, os

import api, db

API = api.API_YANDEX(api.get_token(), os.environ.get("FOLDER_ID"))
DB = db.SQL()
bot = telebot.TeleBot(os.environ.get('TOKEN'))


def bot_message(message: telebot.types.Message, text: str):
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message) -> None:
    bot_message(message, "Привет, я бот, который может преоброзовать текст в речь для этого пропиши /tts")
    DB.create_user(message.from_user.id)


@bot.message_handler(commands=['/tts'])
def send_tts(message: telebot.types.Message) -> None:
    bot_message(message, "Отправьте текст")
    bot.register_next_step_handler(message, tts_handle)


@bot.message_handler(func=lambda message: False)
def tts_handle(message: telebot.types.Message) -> None:
    if message.content_type != "text":
        bot_message(message, "Ошибка! Вы отправили не текст.")
        bot.register_next_step_handler(message, tts_handle)
        return

    if len(message.text) < DB.get_tokens(message.from_user.id):
        bot_message(message, "Ошибка! У вас закончились токены")
        return

    if len(message.text) < 200:
        bot_message(message, "Ошибка! Вы отправили текст больше 200 символов!")
        bot.register_next_step_handler(message, tts_handle)
        return

    answer, data = API.text_to_speech(message.text)

    if answer:
        bot.send_voice(message.from_user.id, data)
    else:
        bot_message(message, text="Непредвиденная ошибка")

    DB.take_away_symbols(message.from_user.id, len(message.text))
