import telebot
from telebot import types
import config_hahabot

bot = telebot.TeleBot(config_hahabot.hahabot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.full_name}, на связи клуб Ха-Хатон! \n\n'
                                            'Здесь ты можешь предложить пост или мем для нашего тг канала.')

    # Создаем клавиатуру
    show_main_menu(message.chat.id)


def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Отправить мем")
    item2 = types.KeyboardButton("Предложить пост")
    markup.add(item1, item2)

    bot.send_message(chat_id, "Выбери, что ты хочешь предложить:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Отправить мем")
def propose_mem(message):
    msg = bot.send_message(message.chat.id, "Отправь свой мем (только одно фото):")
    bot.register_next_step_handler(msg, forward_mem)


def forward_mem(message):
    if message.photo:
        photo_id = message.photo[-1].file_id  # Берем самое большое фото
        caption = "Предложенный мем от @" + message.from_user.username
        bot.send_photo(config_hahabot.predlozhka_chat_id, photo_id, caption=caption)
        bot.send_message(message.chat.id, "Спасибо за предложенный мем! \n\n"
                                          "Если хочешь, можешь отправить еще)")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправь только мем (фото).")

    show_main_menu(message.chat.id)  # Показываем меню выбора после отправки


@bot.message_handler(func=lambda message: message.text == "Предложить пост")
def propose_post(message):
    msg = bot.send_message(message.chat.id, "Отправь свой пост:")
    bot.register_next_step_handler(msg, forward_post)


def forward_post(message):
    if message.text:
        caption = "Предложенный пост от @" + message.from_user.username
        bot.send_message(config_hahabot.predlozhka_chat_id, caption + "\n\n" + message.text)
    elif message.photo:
        photo_id = message.photo[-1].file_id  # Берем самое большое фото
        caption = "Предложенный пост с изображением от @" + message.from_user.username
        bot.send_photo(config_hahabot.predlozhka_chat_id, photo_id, caption=caption)
    elif message.video:
        caption = "Предложенное видео от @" + message.from_user.username
        bot.send_video(config_hahabot.predlozhka_chat_id, message.video.file_id, caption=caption)
    elif message.document:
        caption = "Предложенный документ от @" + message.from_user.username
        bot.send_document(config_hahabot.predlozhka_chat_id, message.document.file_id, caption=caption)
    else:
        bot.send_message(config_hahabot.predlozhka_chat_id, "Получено сообщение другого типа.")

    bot.send_message(message.chat.id, "Спасибо за предложенный пост! \n\n"
                                      "Если хочешь, можешь отправить еще)")

    show_main_menu(message.chat.id)  # Показываем меню выбора после отправки


bot.polling()
