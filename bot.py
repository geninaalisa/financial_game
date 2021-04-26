from random import randint
# -*- encoding: utf-8 -*-
import vk_api
from random import randint
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from open_file import Bot
from datetime import datetime, timedelta


token = '1b35f05be43583ccf0fad81740e6fe69409c569515f9ae54680005501ded6cd33637fa2a7a05d957bf157'
group_id = '200909432'
session = vk_api.VkApi(token=token)
vk = session.get_api()
longpoll = VkBotLongPoll(session, group_id)

game_file = open('game_random.txt', 'r', encoding="utf-8")
rand_list = []
for line in game_file.readlines():
    rand_list.append(line.rstrip())

game_session = {}

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        if game_session.get(event.message.from_id) == None:
            game_session[event.message.from_id] = Bot()
        game = game_session[event.message.from_id]
        
        text = event.message.text
        
        if game.money < 0:
            game.move = 'break'
        if game.block == '0' and game.income != 0:
            game.move = 'end'

        if game.move == 'break':
            message = 'Вы обанкротились.' + 'Конец игры!' + '\n' + '\n' + 'Хотите начать игру заново?'
            
            vk.messages.send(
                    message = message,
                    peer_id=event.message.from_id,
                    random_id=get_random_id()
                ) 
            game_session[event.message.from_id] = Bot()

        if game.move == 'end':
            message = 'Хотите начать игру заново?'
            
            vk.messages.send(
                    message = message,
                    peer_id=event.message.from_id,
                    random_id=get_random_id()
                ) 
            game_session[event.message.from_id] = Bot()

        if game.move == 'start':
            message = 'Привет! Это бот с игрой про финансовую грамотность. Перед началом игры прочитайте правила: ' + '\n' + 'Ваша цель набрать как можно больше денег и не обанкротиться. '
            'Каждый ход вам будет прибавляться доход и будут происходить события на которые вы сможете совершать разные действия, которые повлияют на сюжет'
            '(вместо написания ответов вручную вы можете воспользоваться кнопками)'
            message = 'Вы перехали в новый город. С собой у вас 10000 монет.' + '\n' + 'Для начала игры напиши ок.'
            game.move = 'ask'
            keyboard3 = VkKeyboard()
            keyboard3.add_button('Ок', VkKeyboardColor.POSITIVE)
            vk.messages.send(
                    message = message,
                    peer_id=event.message.from_id,
                    random_id=get_random_id(),
                    keyboard=keyboard3.get_keyboard()
                )

        elif game.move == 'ask':
            if text.lower() == 'ок':
                line = game.open_('game.txt')
                message = game.text(line)
                message += '\n' + game.variants(line)
                game.move = 'choice'
                vk.messages.send(
                    message = message,
                    peer_id=event.message.from_id,
                    random_id=get_random_id(),
                    keyboard=game.button().get_keyboard()
                )
            else:
                message = 'Я не понимаю.' + '\n' + 'Напиши ок'
                vk.messages.send(
                    message = message,
                    peer_id=event.message.from_id,
                    random_id=get_random_id()
                )
                
        elif game.move == 'choice':
            choice = text
            d = game.next_block(line, choice)
            if d != None:
                message = 'Деньги: ' + d \
                + '\n' + 'Доход: ' + str(game.income) \
                + '\n' + 'Дата: ' + game.date.strftime('%d.%m.%Y') \
                + '\n' + 'Влияние: ' + str(game.influence) \
                + '\n' + 'Работа: ' + game.job
                game.move = 'rand'
                vk.messages.send(
                    message = message,
                    peer_id=event.message.from_id,
                    random_id=get_random_id(),
                    keyboard=VkKeyboard.get_empty_keyboard()
                )
                message = '(Для продолжения нажми ок)'
                keyboard2 = VkKeyboard()
                keyboard2.add_button('Ок', VkKeyboardColor.PRIMARY)
                vk.messages.send(
                    message = message,
                    peer_id=event.message.from_id,
                    random_id=get_random_id(),
                    keyboard=keyboard2.get_keyboard()
                )
            else:
                message = 'Попробуй ещё раз. Я не понимаю.'
                vk.messages.send(
                    message = message,
                    peer_id=event.message.from_id,
                    random_id=get_random_id()
                )

        
        if game.move == 'rand':
            rand = randint(-2, 14)
            if rand > -1:
                a = rand_list[rand].split(';')
                message = a[0]
                game.money += int(a[1])
                message += '\n' + 'Деньги: ' + str(game.money)
            
                vk.messages.send(
                    message = message,
                    peer_id=event.message.from_id,
                    random_id=get_random_id()
                ) 
            game.move = 'ask'
