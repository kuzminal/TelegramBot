import config, utils, weather_info
import telebot
import random
import apiai, json
from bot_test import BotTest

bot = telebot.TeleBot(config.token)
bot_test = BotTest(bot)

@bot.message_handler(commands=['test'])
def test_candidate(message):
    bot_test.send_question_from_db(message, 1)

@bot.message_handler(commands=['weather'])
def weathe_forecst(message):
    bot.send_message(message.chat.id, text=weather_info.get_weather())

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, text=config.help_text)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text=config.help_text)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    answer = utils.get_answer_for_user(message.chat.id)
    if not answer:
        responseJson = utils.get_answer_from_dialog_frlow(message)
        response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
        # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
        if response: 
            bot.send_message(message.chat.id, text=response)
        else:
            bot.send_message(message.chat.id, text='Я Вас не совсем понял!')
    else:
        bot_test.validate_user_answer(message, answer)

if __name__ == "__main__":
    random.seed()
    bot.polling(none_stop=True)