import telebot

TOKEN = "2071766316:AAGxbQMuRVzi57pV3Ve8fyOabpcSvDWlYT8"
bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(content_types=["text"])
def send_message(message: telebot.types.Message):
    if message.from_user.id == 777000:
        bot.reply_to(message=message,
                     text="Привет! У этого чата есть правила посмотри их пожалуйста перед написанием текста! https://teletype.in/@hoprik/jTZJjXlAn9v")


bot.polling()