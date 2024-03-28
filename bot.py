import json
from typing import Optional
import config
import telebot
import db
import pyYandexGpt
from pyYandexGpt import Role as rl

bot = telebot.TeleBot(config.TOKEN)
sql = db.SQL()
gpt = pyYandexGpt.PyYandexGpt(pyYandexGpt.get_token(), config.YANDEX_FOLDER_ID, )


def create_markup(buttons: list) -> telebot.types.ReplyKeyboardMarkup:
    replay = telebot.types.ReplyKeyboardMarkup()
    for button in buttons: replay.add(button)
    return replay


def sendMessage(message: telebot.types.Message, text: str,
                keyboard: Optional[telebot.REPLY_MARKUP_TYPES] = None) -> telebot.types.Message:
    return bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id,
                     'Привет, добро пожаловать в бота сценариста. Подробности проекта можно узнать /help, а что бы начать генерировать задачу /new_story')


@bot.message_handler(commands=['help'])
def help_info(message: telebot.types.Message) -> None:
    sendMessage("Привет это телеграм бот, написанный за 3.2 часа. Ты в нем сможешь сгенерировать историю")

@bot.message_handler(commands=["new_story"])
def new_story(message: telebot.types.Message) -> None:
    if not sql.has_user(message.chat.id):
        if sql.count_users() < 2:
            sql.create_user(message.chat.id)
        else:
            sendMessage(message, "Ошибка системы, бот времено не работает =/")

    sendMessage(message, "Выбирете жанр", config.GENRE)
    bot.register_next_step_handler(message, set_character)


@bot.message_handler(func=lambda message: False)
def set_character(message: telebot.types.Message) -> None:
    if message.text not in config.CHARACTER:
        sendMessage(message, text="Ошибка! Такого выбора нет!")
        bot.register_next_step_handler(message, new_story)
    sql.set_genre(message.chat.id, message.text)
    sendMessage(message, "Выбирете персонажа", config.CHARACTER)
    bot.register_next_step_handler(message, set_env)


@bot.message_handler(func=lambda message: False)
def set_env(message: telebot.types.Message) -> None:
    if message.text not in config.CHARACTER:
        sendMessage(message, text="Ошибка! Такого выбора нет!")
        bot.register_next_step_handler(message, new_story)
    sql.set_character(message.chat.id, message.text)
    sendMessage(message, "Выбирете вселеную", config.ENV)


@bot.message_handler(func=lambda message: False)
def create_request(message: telebot.types.Message) -> None:
    if message.text not in config.CHARACTER:
        sendMessage(message, text="Ошибка! Такого выбора нет!")
        bot.register_next_step_handler(message, new_story)
    sql.set_environment(message.chat.id, message.text)
    account = sql.get_account(message.chat.id)
    genre = account[4]
    character = account[5]
    env = account[6]
    gpt_story = json.loads(account[3])
    user_message = gpt_story["user"]
    assistant_message = gpt_story["assistant"]

    if (gpt.count_tokens("Ты сценарист придумывающий историю для людей, помогай им, но делай интригу в конце,чтобы человек смог её продолжить" + f"Привет сделай историю в жанре {genre}, в которой персонаж {character}, а сам находится в {env} всленной. Сделай интригу чтобы я смог продолжить")
            + 100 > account[2]):
        sendMessage(message, "Ваш лимит на сезон токенов исчерпан")
    gpt.add_history(rl.system, "Ты сценарист придумывающий историю для людей, помогай им, но делай интригу в конце, "
                               "чтобы человек смог её продолжить", message.chat.id)
    gpt.add_history(rl.user,
                    f"Привет сделай историю в жанре {genre}, в которой персонаж {character}, а сам находится в {env} всленной. Сделай интригу чтобы я смог продолжить",
                    message.chat.id)
    gpt.add_history(rl.user, user_message, message.chat.id)
    gpt.add_history(rl.assistant, assistant_message, message.chat.id)
    created_message = sendMessage(message, "Нейросеть думает", keyboard=telebot.types.ReplyKeyboardRemove())
    response = gpt.create_request(message.chat.id)
    try:
        data = gpt.response(response, message.chat.id)
        bot.edit_message_text(message_id=created_message.message_id, chat_id=message.chat.id, text=data[0])
        sql.set_tokens(message.chat.id, account[2] - data)
        assistant_message += " " + data[0]
        story = {
            "user": "",
            "assistant": assistant_message
        }
        sql.set_gpt_history(message.chat.id, json.dumps(story))
        sendMessage(message, "Напишите продолжение истории или выберите дейстивин на клавиатуре",
                    keyboard=create_markup(["Закончить"]))
    except pyYandexGpt.YandexGptError as e:
        sendMessage(message, "Не предвиденная ошибка, " + str(e) + "нам придется начать с начало, но ваш сезон не "
                                                                   "закроется, а токены вернутся на баланс аккаунта")
        story = {
            "user": "",
            "assistant": ""
        }
        sql.set_season(message.chat.id, account[2] - 1)
        sql.set_tokens(message.chat.id, 1000)
        gpt.clear_history(message.chat.id)
        sql.set_gpt_history(message.chat.id, json.dumps(story))

        new_story(message)


@bot.message_handler(func=lambda message: False)
def action_request(message: telebot.types.Message):
    if message.text == "Закончить":
        sendMessage(message, "Вы уверены?", keyboard=telebot.types.ReplyKeyboardRemove())
    else:
        account = sql.get_account(message.chat.id)
        history = account[3]
        assistant_message = history["user"]
        user_message = history["user"] + " " + message.text
        story = {
            "user": user_message,
            "assistant": assistant_message
        }
        sql.set_gpt_history(message.chat.id, json.dumps(story))
        create_request(message)


@bot.message_handler(func=lambda message: False)
def sure(message: telebot.types.Message):
    if message.text.lower() == "да":
        story = {
            "user": "",
            "assistant": ""
        }
        sendMessage(message, "Вы закончили сезон")
        sql.set_tokens(message.chat.id, 1000)
        gpt.clear_history(message.chat.id)
        sql.set_gpt_history(message.chat.id, json.dumps(story))
        new_story(message)
    if message.text.lower() == "нет":
        sendMessage(message, "Напишите продолжение истории")
        bot.register_next_step_handler(message, action_request)


bot.polling()
