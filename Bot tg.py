import time
from sys import base_exec_prefix

from dotenv import  load_dotenv
import telebot
import os
import bd_tg
from telebot import types

load_dotenv()
BOT_TOKEN_2 = os.getenv("BOT_TOKEN_2")
bot = telebot.TeleBot(BOT_TOKEN_2)


@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(message.chat.id,"Привет! Это записная книжка!")

@bot.message_handler(commands=["add"])
def add_note(message):
    bot.send_message(message.chat.id, "Введите заметку: ")
    bot.register_next_step_handler(message,save_note)

def save_note(message):
    bd_tg.add_note(message.from_user.id,message.text)
    bot.send_message(message.chat.id,"Заметка сохранена!")


@bot.message_handler(commands=["notes"])
def show_notes(message):
    notes = bd_tg.get_note(message.from_user.id)
    # text = "\n".join([f"{n[0]} - {n[1]}" for n in notes])
    # bot.send_message(message.chat.id,text if text else "Пока нету заметок")
    if not notes:
        bot.send_message(message.chat.id,"Пока нету заметок")
        return
    for note_id,text in notes:
        markup = telebot.types.InlineKeyboardMarkup()
        delete_button = telebot.types.InlineKeyboardButton(
            "Удалить",callback_data=f"del_{note_id}"

        )
        markup.add(delete_button)
        bot.send_message(message.chat.id,text,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_"))
def del_note(call):
    note_id = call.data.split("_")[1]
    bd_tg.delete_note(note_id)
    bot.answer_callback_query(call.id,f"<b>{note_id}</b>")
    bot.edit_message_text("Удалено!",chat_id=call.message.chat.id, message_id=call.message.message_id)

# @bot.message_handler(commands=["delete"])
# def delete(message):
#     bot.send_message(message.chat.id, "Введите id:")
#     bot.register_next_step_handler(message, delete_note)
#
# def delete_note(message):
#     note_id = int(message.text)
#     bd_tg.delete_note(message.text)
#     bot.send_message(message.chat.id, "Заметка удалена!")

# @bot.message_handler(commands=["del"])
# def del_note(message):
#     note_id = message.text.split()[2]
#     bd_tg.delete_note(note_id)
#     bot.send_message(message.chat.id,"Удалено!")

@bot.message_handler(commands=['edit'])
def send_id(message):
    bot.send_message(message.chat.id, "Введите ID заметки:")
    bot.register_next_step_handler(message,send_text)

def send_text(message):
    id_note =  message.text
    bot.send_message(message.chat.id, "Введите новый текст:")
    bot.register_next_step_handler(message, send_update,id_note)

def send_update(message,id_note):
    bd_tg.edit_note(int(id_note), message.text)
    bot.send_message(message.chat.id,"Запись сделана успешна!")








while True:
    try:
        bot.polling(non_stop=True)
    except Exception as ex:
        print(ex)
        time.sleep(2)