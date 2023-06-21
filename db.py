import sqlite3
import logging


class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name, timeout=10)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def edit(self, date, time, sender_id, tg_id, edit_message_sql, edit):
        query = """
        INSERT INTO Chat (date, time, sender_id, tg_id, message, is_edited) 
        VALUES (:date, :time, :sender_id, :tg_id, :message, :is_edited)
        """
        params = {
            'date': date,
            'time': time,
            'sender_id': sender_id,
            'tg_id': tg_id,
            'message': edit_message_sql,
            'is_edited': edit
        }
        self.__execute(query, params)

    def update_username(self, user_name, sender_id):
        query = """
        UPDATE Chat
        SET username = :user_name
        WHERE sender_id = :sender_id
        """
        params = {
            'user_name': user_name,
            'sender_id': sender_id
        }
        self.__execute(query, params)

    def delete(self, date, time, delete, tg_id):
        query = """
        UPDATE Chat 
        SET date = :date, time = :time, is_deleted = :delete 
        WHERE tg_id = :tg_id
        """
        params = {
            'date': date,
            'time': time,
            'is_deleted': delete,
            'tg_id': tg_id
        }
        self.__execute(query, params)

    def new_message(self, date, time, sender_id, tg_id, message_text, reply_mes_id):
        query = """
        INSERT INTO Chat (date, time, sender_id, tg_id, message, reply_tg_id)
        VALUES (:date, :time, :sender_id, :tg_id, :message, :reply_tg_id)
        """
        params = {
            'date': date,
            'time': time,
            'sender_id': sender_id,
            'tg_id': tg_id,
            'message': message_text,
            'reply_tg_id': reply_mes_id
        }
        self.__execute(query, params)

    def __execute(self, query, params):
        try:
            self.cursor.execute(query, params)
        except sqlite3.OperationalError as sql:
            logging.exception(sql)
        except Exception as e:
            logging.exception(e)
