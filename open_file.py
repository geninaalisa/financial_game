# -*- encoding: utf-8 -*-
from random import randint
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime, timedelta

class Bot:
    def __init__(self):
        self.block = '1'
        self.money = 10000
        self.income = 0
        self.variant = []
        self.move = 'start'
        self.date = datetime.today()
        self.influence = 0
        self.job = 'У вас её нет'
        

    def open_(self, file_):
        game_file = open(file_, 'r', encoding="utf-8")
        for line in game_file.readlines():
            line = line.split(';')
            if line[0] == self.block:
                return line

    def text(self, line):
        return line[1]
    
    def variants(self, line):
        st = 'Варианты: '
        self.variant = []
        count = 1
        for i in line:
            if count != 1 and count != 2:
                self.variant.append(i)
            count += 1
        titles = [v.split('@')[0] for v in self.variant]
        st += ', '.join(titles)
        return st

    def next_block(self, line, choice):
        for i in range(len(self.variant)):
            x = self.variant[i].split('@')
            if choice.lower() == x[0].lower():
                weeeks = randint(2, 5)
                self.date += timedelta(weeks=weeeks)
                self.money += self.income
                self.money += int(x[1])
                self.income += int(x[2])
                self.block = x[3].rstrip()
                self.money += self.income
                if self.income > 2000:
                    self.influence += self.income/2000
                    self.influence = round(self.influence, -3)
                if self.influence > 100:
                    self.income += self.influence/100
                if self.block == '4':
                    self.job = choice
                if self.block == '10' and choice == 'Я очень хочу эту работу!!!':
                    self.job = 'Заместитель директора крупного банка'
                return str(self.money)
        return None 

    def button(self):
        keyboard = VkKeyboard()
        c = 0
        for i in self.variant:
            lst = i.split('@')
            keyboard.add_button(lst[0], VkKeyboardColor.SECONDARY)
            c += 1
            if c % 3 == 0 and c < len(self.variant):
                keyboard.add_line()
        return keyboard
