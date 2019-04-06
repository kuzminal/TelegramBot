import sqlite3

class SQLLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """Получаем все строки"""
        with self.connection:
            return self.cursor.execute('select * from question_list').fetchall()

    def select_single(self, rownum):
        """Получаем одну строку с номером rownum"""
        with self.connection:
            return self.cursor.execute('select * from question_list where id = ?', (rownum,)).fetchall()[0]

    def select_single_for_step(self, rownum, step):
        """Получаем одну строку с номером rownum"""
        with self.connection:
            return self.cursor.execute('select * from question_list where question_step = ?', (step,)).fetchall()[rownum-1]
    
    def count_rows(self):
        """Считаем записи"""
        with self.connection:
            result = self.cursor.execute('select * from question_list').fetchall()
            return len(result)

    def count_rows_for_step(self, step):
        """Считаем записи"""
        with self.connection:
            result = self.cursor.execute('select * from question_list where question_step = ?', (step,)).fetchall()
            return len(result)

    def save_question_result(self, chat_id, question_id):
        """Записываем вопрос и чат"""
        with self.connection:
            if self.count_rows_question_for_chat(chat_id, question_id) == 0:
                self.cursor.execute('insert into test_results(chat_id, question_id) values(?,?)', (chat_id,question_id,))
            else: pass
    
    def count_rows_question_for_chat(self, chat_id, question_id):
        """Считаем записи"""
        with self.connection:
            result = self.cursor.execute('select * from test_results where chat_id = ? and question_id = ?', (chat_id,question_id,)).fetchall()
            return len(result)

    def count_rows_question_without_result(self, chat_id, question_id):
        """Считаем записи"""
        with self.connection:
            result = self.cursor.execute('select * from test_results where chat_id = ? and question_id = ? and result is NULL', (chat_id,question_id,)).fetchall()
            return len(result)

    def update_question_result(self, chat_id, question_id, result):
        """Записываем результат ответа на вопрос"""
        with self.connection:
            if self.count_rows_question_without_result(chat_id, question_id) == 1:
                self.cursor.execute('update test_results set result =? where chat_id=? and question_id =?', (result,chat_id,question_id,))
            else: pass

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()