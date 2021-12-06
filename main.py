import random
import telebot
import config
import heroes
import requests
import os
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.token)
bogma = 426128881
admin = 406626012

@bot.message_handler(commands=['start', 'help'])
def main(message):
    # for i in heroes.miders:
    #     send_hero(message, i)
    hero = random.choice(heroes.miders)
    send_hero(message, hero)


def parse_stats(message, hero):
    url = 'https://dotabuff.com/heroes/lanes'
    response = requests.get(url, headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.findAll('td')
    x = {}
    for i in range(round(len(quotes)/7)):
        x.update({quotes[1].text: [quotes[i].text for i in range(7) if quotes[i].text]})
        quotes = quotes[7:]
    hero_name  = x[hero][0]
    picked = x[hero][1]
    winrate = x[hero][2]
    kda = x[hero][3]
    gpm = x[hero][4]
    text_for_message = ("Your hero is " + hero_name + 
                        "\nPickrate: " + picked + 
                        "\nWinrate: " + winrate +
                        "\nAverage KDA: " + kda +
                        "\nAverage GPM: " + gpm
    )
    bot.send_message(message.chat.id, text=text_for_message)


def send_hero(message, hero):
    """Send hero visual"""
    # media_url = os.getcwd() + hero['media']
    media_url = hero['media']
    print(media_url)
    if media_url != '':
        if (media_url[-4:] == '.mp4' or 
            media_url[-4:] == '.gif' or 
            media_url[-5:] == '.webm'):
            try:
                bot.send_video(message.chat.id, media_url)
            except:
                try: 
                    media_video = open(media_url, 'rb')
                    bot.send_video(message.chat.id, media_video)
                except:
                    fail = open('Bztt_L4jfX8.jpg', 'rb')
                    bot.send_photo(message.chat.id, fail)
        else:
            try:
                media_image = open(media_url, 'rb')
                bot.send_photo(message.chat.id, media_image)
            except:
                fail = open('Bztt_L4jfX8.jpg', 'rb')
                bot.send_photo(message.chat.id, fail)
    else:
        bot.send_message(message.chat.id, text='Ыконку спиздили хохлы')
    parse_stats(message, hero['hero'])
    # bot.send_message(message.chat.id, text=hero['hero'])
    if (message.chat.id != admin): 
        bot.send_message(admin, text='Мистер ' + message.from_user.first_name 
                                            + ' заранадомил:\n' + hero['hero']) 
        


bot.polling()