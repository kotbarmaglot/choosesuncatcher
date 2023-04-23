from .config import API_KEY
from .vkchoosesun import *
import telebot
import json
from telebot import types
from telebot.types import InputMediaPhoto
from random import randint
import time


bot = telebot.TeleBot(API_KEY)

media_gr_id = {}
url_list = {}
del_post = {}


def create_file_info_prod_json():
    with open("info_product.json", "w") as write_file:
        json.dump(update_info_product(), write_file)
        print('Файл с товарами из вк создан или обновлен.')


def create_upd_file_url_list_json(data={}, is_create=1):
    if is_create == 1:
        with open("url_list.json", "w") as write_file:
            json.dump(data, write_file)
            print('Файл url_list создан')
    else:
        with open("info_product.json", "r") as read_file:
            data = json.load(read_file)

        x = 0
        url_list_u = []

        while x < len(data):
            url_list_u.append(data[str(x)]['url_photo'])
            x +=1

        url_list['url_list'] = url_list_u

        with open("url_list.json", "w") as write_file:
            json.dump(url_list, write_file)
            print('Файл url_list обновлен')


def upd_media_group_id(data):
    with open("media_group_id.json", "w") as write_file:
        json.dump(data, write_file)
        print('Файл media_group_id cздан или обновлен.')


def delete_media_group(message, choose_left=0, choose_right=0):
    with open("media_group_id.json", "r") as read_file:
        data = json.load(read_file)

    bot.delete_message(message.chat.id, data[str(message.chat.id)][0][0])
    bot.delete_message(message.chat.id, data[str(message.chat.id)][0][1])

    with open("url_list.json", "r") as read_file:
        data1 = json.load(read_file)

    if choose_left == 1:
        data1['url_list'].pop(data[str(message.chat.id)][2])

    if choose_right == 1:
        data1['url_list'].pop(data[str(message.chat.id)][1])
    
    create_upd_file_url_list_json(data1)


def send_media_group(message):
    m_id = []
    ch_id = 0
    fin_media_id = []

    with open("url_list.json", "r") as read_file:
        data = json.load(read_file)

    if len(data['url_list']) > 1:

        left = randint(0, len(data['url_list']) // 2 - 1)
        right = randint(len(data['url_list']) // 2, len(data['url_list']) - 1)

        pic1 = data['url_list'][left]
        pic2 = data['url_list'][right]

        media = [InputMediaPhoto(pic1), InputMediaPhoto(pic2)]
        msg = bot.send_media_group(message.chat.id, media)

        for elem in msg:
            m_id.append(elem.message_id)
            ch_id = elem.chat.id
        
        media_gr_id[ch_id] = m_id, left, right

        upd_media_group_id(media_gr_id)
    
    else:

        with open("first_id.json", "r") as read_file:
            first_id = json.load(read_file)

        bot.delete_message(message.chat.id, first_id)

        with open("info_product.json", "r") as read_file:
            info_prod = json.load(read_file)

        x = 0

        while x < len(info_prod):
            if info_prod[str(x)]['url_photo'] == data['url_list'][0]:
                title = info_prod[str(x)]['title']
                description = info_prod[str(x)]['description']
                price = info_prod[str(x)]['price']
            x+=1

        text = 'Ваш выбор: ' + f'{title}'
        
        pic1 = data['url_list'][0]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton('Сыграть заново')
        markup.add(item)

        markup_inline = types.InlineKeyboardMarkup()
        item = types.InlineKeyboardButton(text='Написать в личку', url='https://t.me/Lunar_room')
        markup_inline.add(item)

        choose_text = bot.send_message(message.chat.id, text=text, reply_markup=markup)
        choose_photo = bot.send_photo(message.chat.id, pic1, caption=description, reply_markup=markup_inline)

        del_post[choose_text.chat.id] = choose_text.message_id, choose_photo.message_id

        with open("fin_text.json", "w") as write_file:
            json.dump(del_post, write_file)


@bot.message_handler(commands=['start'])
def start(message):
    
    print(message)
    create_file_info_prod_json()
    create_upd_file_url_list_json(is_create=0)

    user_name = message.from_user.first_name
    text_message = 'Привет, давай сыграем в игру! Будут меняться ловцы.\n\nВыбери какой тебе нравится больше - Левый или Правый'
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Выбрать левый')
    item2 = types.KeyboardButton('Выбрать правый')
    markup.add(item, item2)

    first = bot.send_message(message.chat.id, text=text_message, reply_markup=markup)

    with open("first_id.json", "w") as write_file:
        json.dump(first.id, write_file)

    send_media_group(message)


@bot.message_handler(func=lambda m: True)
def main(message):
    t = message.text

    if t == 'Выбрать левый':
        bot.delete_message(message.chat.id, message.message_id)
        delete_media_group(message, choose_left=1)
        send_media_group(message)

    if t == 'Выбрать правый':
        bot.delete_message(message.chat.id, message.message_id)
        delete_media_group(message, choose_right=1)
        send_media_group(message)

    if t == 'Сыграть заново':

        with open("fin_text.json", "r") as read_file:
            fin_text = json.load(read_file)

        bot.delete_message(message.chat.id, fin_text[str(message.chat.id)][0])
        bot.delete_message(message.chat.id, fin_text[str(message.chat.id)][1])

        bot.delete_message(message.chat.id, message.message_id)

        start(message)


bot.infinity_polling() 


def main():
    pass


if __name__ == '__main__':
    main()