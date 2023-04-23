def edit_media_group(message):
    with open("media_group_id.json", "r") as read_file:
        data = json.load(read_file)

    pic1 = 'https://sun6-23.userapi.com/impg/pRg4gqwTFhHSqBb5Do8_CbAh6gDl3gz86DC_Qw/UmSErGTB0f8.jpg?size=1080x1079&quality=95&sign=12ff1fd6996900453e878b3db40cf1b8&type=album'

    pic2 = 'https://sun9-78.userapi.com/impg/_Y9m20t7FWYNtloSaiJi1yb0X8_Tcn47rljT9Q/80WHFlMFpdk.jpg?size=2560x2560&quality=95&sign=3f8255c76872459ae10bce313d0abddc&type=album'

    media = InputMediaPhoto(pic1)
    media2 = InputMediaPhoto(pic2)

    bot.edit_message_media(message.from_user.id, data[str(message.from_user.id)][0], media=media)
    bot.edit_message_media(message.from_user.id, data[str(message.from_user.id)][1], media=media2)

# реализация через инлайн кнопки. Callback's:

    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text = 'Выбрать левый', callback_data = 'left')
    item2 = types.InlineKeyboardButton(text = 'Выбрать правый', callback_data = 'right')
    markup.add(item1, item2)

@bot.callback_query_handler(func=lambda m: True)
def callback_choice(message):
    t = message.data
    # print(message.data)

    if t == 'left':

        # print(url_list[randint(0, 5)])

        # for elem in data:
        #     print(elem['url_photo'])
        # pic1 = 'https://sun9-69.userapi.com/LP0G-hyTmjrJpSMWzzFYiPUCSqRdt-hf_A0xig/Yf_xeZa4pa4.jpg'
        pic1 = url_list[randint(0, 5)]
        print(pic1)
        media1 = InputMediaPhoto(pic1)
        bot.edit_message_media(chat_id=ch_id, message_id=m_id[0], media=media1)

    if t == 'right':
        pic2 = 'https://sun9-41.userapi.com/2RVJNxojelzK6g_WvCCqmw7wf0owFmorla1Vvg/Otp9ld3GNKk.jpg'
        media2 = InputMediaPhoto(pic2)
        bot.edit_message_media(chat_id=ch_id, message_id=m_id[1], media=url_list[randint(0, 5)])