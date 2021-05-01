from config import token
import emoji
import telebot
from telebot import types
from photo_generator import photo_generator


bot = telebot.TeleBot(token)

@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_geo = types.KeyboardButton(text=f'{emoji.GLOBE_SHOWING_AMERICAS}{emoji.ROUND_PUSHPIN}',
                                      request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)
    user_profile_photo = bot.get_user_profile_photos(message.chat.id)
    print(user_profile_photo, '<-----')

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        '''
        photo_generator(user_id=message.from_user.id,
                        x=message.location.longitude,
                        y=message.location.latitude)'''
        bot.get_user_profile_photos(message.chat.id)
        print("широта(y): %s; долгота(x): %s" % (message.location.latitude, message.location.longitude))

bot.polling()