from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
database = 'logger.db'


@app.route('/')
def chat():
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT date, time, username, message, tg_id, reply_tg_id, is_deleted from Chat')
    #messages = cursor.fetchall()
    chat = []
    for i in cursor:
        message = {}
        messages = cursor.fetchone()
        if messages == None:
            break
        date = messages[0]
        time = messages[1]
        username = messages[2]
        text = messages[3]
        tg_id = messages[4]
        reply_tg_id = messages[5]
        is_deleted = messages[6]
        date_time = ' | '.join([str(date), str(time)])
        message['date_time'] = date_time
        username_message = ': '.join([str(username), str(text)])
        message['username_message'] = username_message
        status = ' | '.join([str(tg_id), str(reply_tg_id), str(is_deleted)])
        message['status'] = status
        chat.append(message)
    connection.close()
    return render_template('index.html', chat=chat)

if __name__ == '__main__':
    app.run()