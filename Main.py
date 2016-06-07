# -*- coding: utf-8 -*-

import random
import telebot

import Constaints
import RaspParse
import Database

types = telebot.types
bot = telebot.TeleBot(Constaints.token)
print(bot.get_me())


def log(message, answer):
    print("\n ::::::::::")
    from datetime import datetime
    print((datetime.now()))
    print('Сообщение от {0} {1}. (id = {2})\nТекст - {3}'.format(message.from_user.first_name,
                                                                 message.from_user.last_name,
                                                                 str(message.from_user.id),
                                                                 message.text))
    print(answer)


Database.DeleteAllRecords()


def GetUserKeyboard():
    UserKeyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    UserKeyboard.row('Сегодня', 'Завтра', 'Неделя')
    UserKeyboard.row('Чётность недели', 'Выход')

    return UserKeyboard


def GetDefaultKeyboard():
    return telebot.types.ReplyKeyboardHide()


@bot.message_handler(commands=['reg'])
def handle_reg(message):
    try:

        if Database.GetStudent(message.from_user.id):
            answer = 'Вы уже зарегистрированы'
            return
        else:
            answer = bot.reply_to(message, 'В какой Вы группе?')
            bot.register_next_step_handler(answer, enterGroupName)

    except Exception as e:
        bot.reply_to(message, 'oooops')

        # group = message.text.split('/reg')[-1].strip()

        # if not RaspParse.GetGroupID(group):
        #    answer = 'Такой группы нет!'
        #    keyboard = DefaultKeyboard
        # else:
        #    Database.InsertStudent(message.from_user.id, message.from_user.last_name, group)
        #    answer = 'Вы зарегистрированы в системе!'
        #    keyboard = UserKeyboard

        # log(message, answer)
        #
        # bot.send_chat_action(message.from_user.id, 'typing')
        # bot.send_message(message.from_user.id, answer, reply_markup=keyboard)


def enterGroupName(message):
    try:

        group = message
        if not RaspParse.GetGroupID(group.text):
            answer = bot.reply_to(message, 'Что-то тут не то! Так из какой Вы группы?')
            bot.register_next_step_handler(answer, enterGroupName)
            return
        else:
            Database.InsertStudent(message.from_user.id, message.from_user.last_name, group.text)
            answer = 'Вы зарегистрированы в системе!'

            bot.send_chat_action(message.from_user.id, 'typing')
            bot.send_message(message.from_user.id, answer, reply_markup=GetUserKeyboard())

    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    answer = []
    user = Database.GetStudent(message.from_user.id)

    if message.text == 'Сегодня':
        answer = RaspParse.GetTodayRasp(user['group'])
    elif message.text == 'Завтра':
        answer = RaspParse.GetTomorrowRasp(user['group'])
    elif message.text == 'Неделя':
        answer = RaspParse.GetWeekRasp(user['group'])
    elif message.text == 'Чётность недели':
        answer = RaspParse.GetParity()
    elif message.text == 'Выход':
        Database.DeleteById(message.from_user.id)
        log(message, answer)
        bot.send_message(message.from_user.id, 'Вы успешно вышли из системы', reply_markup=GetDefaultKeyboard())
        return

    # else:
    #     random.seed()
    #     rndFact = Constaints.Facts[random.randint(0, len(Constaints.Facts) - 1)]
    #     rndCat = Constaints.Cats[random.randint(0, Constaints.CatsSize - 1)]
    #     img = open(Constaints.ProjectPath + '/TelegramBot/Cats/' + rndCat, 'rb')
    #
    #     bot.send_chat_action(message.from_user.id, 'upload_photo')
    #     bot.send_photo(message.from_user.id, img, rndFact)
    #     img.close()
    #
    #     log(message, rndFact)
    #     return

    log(message, answer)
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, answer)


bot.polling(none_stop=True)
