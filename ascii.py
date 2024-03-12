from telebot import *
from telebot import types
from telebot.handler_backends import State, StatesGroup
from scripts import *
import os

API_TOKEN = '6662827447:AAG5GmjwROgKgZglJTJ5CXfrPSOBQwoD0Qc'
add_chars = '*xх'
bot = telebot.TeleBot(API_TOKEN)
photo_file_ids = {}
# path = C:\Users\obser\PycharmProjects\ascii


class AddStats(StatesGroup):
    photo = State()
    add_size = State()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.delete_state(message.from_user.id)
    welcome_message_text = """
    Welcome👋!
    """
    bot.send_message(message.chat.id, welcome_message_text, parse_mode='html')


@bot.message_handler(content_types=['photo'])
def photo_download(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = 'photo.jpg'
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    message_text = """
    Please enter the new width and height (in pixels) separated by a space, e.g., 300 200
    """
    bot.send_message(message.chat.id, message_text, parse_mode='html')


@bot.message_handler(func=lambda message: message.text.isdigit())
def process_dimensions(message):
    chat_id = message.chat.id
    dimensions = message.text.split()
    if len(dimensions) == 2 and all(dim.isdigit() for dim in dimensions):
        width, height = map(int, dimensions)
        if chat_id in photo_file_ids:
            photo_file_id = photo_file_ids[chat_id]
            del photo_file_ids[chat_id]
            photo = bot.get_file(photo_file_id)
            photo_path = os.path.join(os.getcwd(), photo.file_path)
            photo.download(photo_path)

            resized_image = resize_photo(photo_path,width, height)

            png_2_ascii(resized_image)

        else:
            bot.send_message(message.chat.id, "No photo found for these dimensions. Please send a photo first.")
    else:
        bot.send_message(message.chat.id, "Invalid input. Please enter the new width and height separated by a space, e.g., 300 200")


bot.infinity_polling()