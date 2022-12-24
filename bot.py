import config  # импорт файла *config.py*
import random
from telebot import TeleBot, types
from time import sleep

    # Переменные игровой статистики
victories = 0
defeats = 0
draws = 0
    
bot = TeleBot(config.BOT_TOKEN, parse_mode='html') # Авторизация токена

    # Меню start
@bot.message_handler(commands=['start'])

def Hello(message):
    bot.send_message(message.chat.id, f'👋 Привет, <b>{message.from_user.first_name}</b> 👋\n\n'
                                      f'Надеюсь, вам понравится работать со мной 😊\n\n'
                                      f'Взаимодействие со мной происходит при помощи кнопки <b>"меню"</b> ниже 👇'
                                      )    
    # Дополнительная информация
@bot.message_handler(commands=['credits'])

def Credits(message):
    bot.send_message(message.chat.id, '<Напишите о себе, боте или чём-нибудь ещё>')

    # Генератор паролей
@bot.message_handler(commands=['generate'])

def GenerateRequest(message):
    sent_msg = bot.send_message(message.chat.id, 
                                '😁 Cупер😁 \nТеперь введите количество символов\n❗️<b>от 2 до 64</b>❗️')
    bot.register_next_step_handler(sent_msg, Generate)

def Generate(message):
    _characters = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*'
    _length = int(message.text)
                                                        
    if _length < 2 or _length > 64:
        bot.send_message(message.chat.id, 
                        '⛔️ Неправильное количество символов ⛔️ \nПопробуйте ещё раз! Используйте /generate')
    else:
        bot.send_message(message.chat.id, '💬 Генерирую пароль... 💬')
        _password = "".join(random.sample(_characters, _length))
        sleep(0.5)
        bot.send_message(message.chat.id, _password)
        sleep(0.3)
        bot.send_message(message.chat.id, '✅ Генерация прошла успешно ✅')
    
    # Игра
@bot.message_handler(content_types=['text'])

def Game(message):
    if message.chat.type == 'private':
        
        win_msg = 'Вы победили 😃\nНе хотите ещё сыграть?' # сообщение о победе
        lose_msg = 'Вы проиграли 😔\nВозьмите же реванш!'  # сообщение о поражении
        draw_msg = 'Ничья 🤨\nПопробуйте ещё раз'          # сообщение о ничье
        items = ['Камень', 'Ножницы', 'Бумага']             # область выбора бота
        bot_choose = random.choice(items)                   # рандомный выбор бота из списка выше
        bot_msg = f'Бот выбрал <b>{bot_choose}</b>'         # сообщение о выборе бота
        global draws, victories, defeats

        if message.text == '/game':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            btn_1 = types.KeyboardButton('Камень')
            btn_2 = types.KeyboardButton('Ножницы')
            btn_3 = types.KeyboardButton('Бумага')
            end_btn = types.KeyboardButton('Статистика')
            markup.add(btn_1, btn_2, btn_3, end_btn)

            bot.send_message(message.chat.id, 
                            'Камень, ножницы, бумага, а может статистика?🤔', 
                            reply_markup = markup)
        
        elif message.text == bot_choose:
            sleep(0.5)
            bot.send_message(message.chat.id, bot_msg)
            draws += 1
            bot.send_message(message.chat.id, draw_msg)
        
        elif message.text == 'Ножницы':
            sleep(0.5)
            bot.send_message(message.chat.id, bot_msg)
            if bot_choose == items[2]:
                victories +=1
                bot.send_message(message.chat.id, win_msg)
            else:
                defeats += 1
                bot.send_message(message.chat.id, lose_msg)

        elif message.text == 'Камень':
            sleep(0.5)
            bot.send_message(message.chat.id, bot_msg)
            if bot_choose == items[1]:
                victories +=1
                bot.send_message(message.chat.id, win_msg)
            else:
                defeats += 1
                bot.send_message(message.chat.id, lose_msg)

        elif message.text == 'Бумага':
            sleep(0.5)
            bot.send_message(message.chat.id, bot_msg)
            if bot_choose == items[0]:
                victories +=1
                bot.send_message(message.chat.id, win_msg)
            else:
                defeats += 1
                bot.send_message(message.chat.id, lose_msg)

        elif message.text == 'Статистика':
            sleep(0.5)
            bot.send_message(message.chat.id, f'Общая статистика:\n\n'
                                              f'<b>Победы:</b> {victories}\n'
                                              f'<b>Поражения:</b> {defeats}\n'
                                              f'<b>Ничьи:</b> {draws}')
        else:
            sleep(0.5)
            bot.send_message(message.chat.id, 'Не понимаю, чего вы желаете😔')
    
    # RUN
while True:
    try:
        if __name__ == '__main__':
            bot.polling(none_stop=True, interval=0)
    except:
        continue
    
