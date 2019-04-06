import shelve
from SQLLighter import SQLLighter
from config import database_name, shelve_name, dialog_id
from telebot import types
from random import shuffle
import apiai, json

"""def count_rows():
    db = SQLLighter(database_name)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rowsnum"""

def count_rows_for_step(step):
    db = SQLLighter(database_name)
    rowsnum = db.count_rows_for_step(step)
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rowsnum

def get_rows_count():
     with shelve.open(shelve_name) as storage:
         rowsnum = storage['rows_count']
         return rowsnum

def set_user_game(chat_id, question_id, estimated_answer):
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = [question_id, estimated_answer]

def finish_user_game(chat_id):
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]

def get_answer_for_user(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)][1]
            return answer
        except KeyError:
            return None

def get_q_id_for_user(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            q = storage[str(chat_id)][0]
            return q
        except KeyError:
            return None

def generate_markup(right_answer, wrong_answer):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    all_answers = '{},{}'.format(right_answer, wrong_answer)
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    shuffle(list_items)
    for item in list_items:
        markup.add(item)
    return markup

def get_answer_from_dialog_frlow(message):
    request = apiai.ApiAI(dialog_id).text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = message.text # Посылаем запрос к ИИ с сообщением от юзера
    return json.loads(request.getresponse().read().decode('utf-8'))
        