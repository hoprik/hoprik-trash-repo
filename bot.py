import telebot
from telebot import types as tgp
import config
import gpt

bot = telebot.TeleBot(config.TOKEN)

user_history = {}

ai_modes = [
    "математик",
    "шефповр",
    "программист",
    "поэт"
]

ai_desc = {
    "математик": "Ты дружулюбный помошник по математике",
    "шефповр": "Ты повор, ты помогаешь всем рецептом",
    "программист": "Ты программист, ты помогаешь всем с ошибками",
    "поэт": "Ты поэт, ты придумаваешь стихи, рассказы и сказки"
}


def keyboard_gen(buttons: list) -> tgp.ReplyKeyboardMarkup:
    markup = tgp.ReplyKeyboardMarkup(one_time_keyboard=True)
    for button in buttons: markup.add(tgp.KeyboardButton(button))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message: tgp.Message):
    bot.send_message(chat_id=message.chat.id, text="Привет, я помошник на искувстевенном интелекте! Выбери режим ии",
                     reply_markup=keyboard_gen(ai_modes))
    bot.register_next_step_handler(message, send_ai_answer)


@bot.message_handler(content_types=["text"], func=lambda message: False)
def send_ai_answer(message: tgp.Message):
    user_history[message.from_user.id] = [message.text, []]
    user_history[message.from_user.id][1].append(
        gpt.make_message("system", "Answer in Russian and do not translate the text into another language"))
    user_history[message.from_user.id][1].append(gpt.make_message("system", ai_desc[message.text]))
    user_history[message.from_user.id][1].append(gpt.make_message("assistant", "Решим задачу по шагам: "))
    bot.send_message(chat_id=message.chat.id, text="Напишите задачу: ")
    bot.register_next_step_handler(message, send_ai_request_answer)


@bot.message_handler(content_types=["text"], func=lambda message: False)
def send_ai_request_answer(message: tgp.Message):
    user_history[message.from_user.id][1].append(gpt.make_message("user", message.text))
    ai_answer = bot.send_message(chat_id=message.chat.id, text="Нейросеть думает")
    payload = gpt.make_prompt(user_history[message.from_user.id][1])
    rep = gpt.send_request(payload)
    text = gpt.get_request(rep)
    user_history[message.from_user.id][1].append(gpt.make_message("assistant", text))
    bot.edit_message_text(chat_id=message.chat.id, message_id=ai_answer.message_id, text=text)
    bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id, text="Сообщение доставлено",
                     reply_markup=keyboard_gen(["Продолжить", "Закончить"]))
    bot.register_next_step_handler(message, send_ai_question)


@bot.message_handler(content_types=["text"], func=lambda message: False)
def send_ai_question(message: tgp.Message):
    if message.text == "Закончить":
        bot.register_next_step_handler(message, send_welcome)
    elif message.text == "Продолжить":
        bot.register_next_step_handler(message, send_ai_request_answer)
    else:
        bot.register_next_step_handler(message, send_ai_request_answer)


if __name__ == "__main__":
    print("Бот запускается....")
    bot.polling()