import telebot
import youtube_dl
import os
import sys
import re

bot = telebot.TeleBot(sys.argv[1], parse_mode=None)

def replacefunction(somestr):
    result = ''
    for i in somestr:
        if i == '|' or i == '`':
            i = '#'
        result += i
    return result


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "the only thing you need is the URL of the YouTube video you want to extract the audio from. just text /getfile and follow instructions")


@bot.message_handler(commands=['getfile'])
def send_welcome(message):
    sent = bot.send_message(message.chat.id, "send me your link)")
    bot.register_next_step_handler(sent, task)

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def task(link):
    video_url = link.text
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url, download=False
    )
    filename_tmp = f"{get_valid_filename(video_info['title'])}.dat"
    filename =  f"{get_valid_filename(video_info['title'])}.mp3"

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename_tmp,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    audio = open(filename, 'rb')    
    # Grab known info from metadata
    duration = video_info["duration"]
    title = video_info.get("track", None)
    artist = video_info.get("artist", None)
    # Send the audio in response
    bot.send_audio(link.chat.id, audio, duration=duration, title=title, performer=artist)
    audio.close()
    os.remove(filename)



bot.polling(none_stop=False, interval=0, timeout=20)
