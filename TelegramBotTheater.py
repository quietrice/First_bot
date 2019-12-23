# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 16:28:59 2019

@author: andre
"""

import requests
import json

def get_data():
    response = requests.get('https://bol-theater.com/afisha/')
    a = response.content.decode('utf-8')
    
    s_start = '<script type="application/ld+json">'
    s_end = '</script>'
    
    j_start = a.find(s_start) + 36
    j_end = a.find(s_end, j_start) - 1
    
    future_json = a[j_start : j_end]
    
    
    d = json.loads(future_json)["events"]
    dates = list()
    for elem in d:
        name = elem['name']
        dates.append([name, elem['startDate']])
        
    left = '</a><div class="date__scene"><span>'
    right = '</span></div></div></div><div class="ev_date__time">'
    prev_start = 0
    prev_end = 0
    
    for i in range(len(dates)):
        
        start = a.find(left, prev_start)
        end = a.find(right, prev_end)
        dates[i].append(a[start + 35 : end])
        
        prev_start = start + 1
        prev_end = end + 1
    
    return dates # список со списками в формате name, date, place

data = get_data()

import time
t=str(time.strftime("%x", time.localtime()))
k1=t.find('/')
k2=t.rfind('/')
a=t[:k1]
b=t[k1+1:k2]
c=t[k2+1:]
Today_date='20'+c+'-'+a+'-'+b 

def coup(l):
    l2=''
    for i in range(len(l)-1,-1,-1):
        l2+=l[i]+'-'
    return l2

import telebot

bot = telebot.TeleBot('966394153:AAE70jhwkEHKIcYCSc-W0kB4k6UlCEUUOjY')


@bot.message_handler(commands=['start'])
def send_Day(message): 

    text='Выбери день\nНапишите "Сегодня"\n"Завтра"\nЛибо напишите точную дату:\n xx.xx.20xx (01.01.2019)'
    bot.send_message(message.chat.id,text)#reply_markup=markup) 

@bot.message_handler(func= lambda message:  message.text=='Сегодня' or message.text=='Today' )
def send_Table_today(message):
    text='Сегодня:\n------------\n'
    for i in range(len(data)):
        if data[i][1].find(Today_date)!=-1:
            text+='Время: '+data[i][1][data[i][1].find('T')+1:]+'\nДата:'+data[i][1][:data[i][1].find('T')]
            text+='\nСпектакль: '+data[i][0]+'\nМесто: '+data[i][2]
            text+='\n------------\n'
        else:
            break
    if text=='Сегодня:\n------------\n':
        text='Сегодня спектаклей не будет!\n'
    bot.send_message(message.chat.id, text)
    

        
@bot.message_handler(func= lambda message:  message.text=='Завтра' )
def send_Table_tomorrow(message):
    text='Завтра\n------------\n'
    Tomorrow_date=Today_date[:len(Today_date)-1]+str(int(Today_date[len(Today_date)-1])+1)
    for i in range(len(data)):
        if data[i][1].find(Tomorrow_date)!=-1:
            text+='Время: '+data[i][1][data[i][1].find('T')+1:]+'\nДата:'+data[i][1][:data[i][1].find('T')]
            text+='\nСпектакль: '+data[i][0]+'\nМесто: '+data[i][2]
            text+='\n------------\n'
        elif text=='Завтра\n------------\n' and data[i][1]!=Tomorrow_date and data[i][1]!=Today_date:
            text='Спектаклей в этот день не будет!'
        elif text!='Завтра\n------------\n':
            break
    bot.send_message(message.chat.id, text)

@bot.message_handler(func= lambda message:  message.text.find('20') != -1)
def send_Table_ThisDate(message):

    date=message.text
    date=date.split('.')
    date.reverse()
    date = '-'.join(date)

    text = str()

    for elem in data:
        if date in elem[1]:
            if not text:
                text='В этот день будет\n------------\n'
            text += 'Время: ' + elem[1][-5:] +'\nДата: ' + elem[1][:-6]
            text+='\nСпектакль: ' + elem[0] +'\nМесто: ' + elem[2]
            text+='\n------------\n'
        
        
    if not text:
        text ='В этот день спектаклей не будет!\n'
    bot.send_message(message.chat.id, text)
        
bot.polling()

