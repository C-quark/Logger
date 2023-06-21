import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

database = 'logger.db'

def clicked():
  res = inscription_txt.get()
  inscription_txt.delete(0, END)
  connection = sqlite3.connect(database)
  cursor = connection.cursor()
  id = res
  cursor.execute('select id, id_sender, message from Chat where id > ' + str(id))
  #chat = cursor.fetchall()
  chat = []
  row = 0
  while True:
    message = cursor.fetchone()
    row += 1
    if message == None:
        break
    chat_window = Label(window, text=message)
    chat_window.grid(column=0, row=row)
    print(message)
    chat.append(message)
  #chat_window = Label(window, text=message)
  #chat_window.grid(column=0, row=1)
  window.mainloop()
  file = open('chat.txt', 'w')
  file.write(str(chat))
  file.close()


window = Tk()
window.title("Чат")
window.geometry('500x900')
inscription = Label(window, text="С какого сообщения начать читать?")
inscription.grid(column=0, row=0)
inscription_txt = Entry(window,width=10)
inscription_txt.grid(column=1, row=0)
btn = Button(window, text="Ok", command=clicked)
btn.grid(column=2, row=0)
window.mainloop()
