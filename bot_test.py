import config
import telebot
from SQLLighter import SQLLighter
import random
import utils
from telebot import types

class BotTest:

    def __init__(self, bot):
        self.bot = bot

    def send_question_from_db(self, message, step):
        db_worker = SQLLighter(config.database_name)
        utils.count_rows_for_step(step)
        row = db_worker.select_single_for_step(random.randint(1, utils.get_rows_count()), step)
        markup = utils.generate_markup(row[2], row[3])
        utils.set_user_game(message.chat.id, row[0],row[2])
        q_id = utils.get_q_id_for_user(message.chat.id)
        check_chat = db_worker.count_rows_question_for_chat(message.chat.id, q_id)
        if check_chat == 0:
            self.bot.send_message(message.chat.id, row[1], reply_markup=markup)
            db_worker.save_question_result(message.chat.id, row[0])
        else:
            self.bot.send_message(message.chat.id, text='Вы уже отвечали на вопросы тестирования. Повторная попытка!')
            utils.finish_user_game(message.chat.id)
        db_worker.close()

    def validate_user_answer(self, message, answer):
        q_id = utils.get_q_id_for_user(message.chat.id)
        db_worker = SQLLighter(config.database_name)
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            self.bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
            db_worker.update_question_result(message.chat.id,q_id,1)
            self.bot.send_message(message.chat.id, 'Поздравляем, тестирование завершено!', reply_markup=keyboard_hider)
            utils.finish_user_game(message.chat.id)
        else:
            self.bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте еще раз!', reply_markup=keyboard_hider)
            db_worker.update_question_result(message.chat.id,q_id,0)
            utils.finish_user_game(message.chat.id)
        db_worker.close()