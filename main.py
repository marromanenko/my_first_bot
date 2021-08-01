import telebot
import youtube_dl
import os
import sys
#1814507400:AAEW-lEr3Wqls7HRdwkPDt0cKFoUCn0oxIU
bot = telebot.TeleBot("{}".format(sys.argv[1]), parse_mode=None)


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


def task(link):
    video_url = link.text
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url, download=False
    )
    filename_tmp = f"{video_info['title']}.dat"
    filename = f"{video_info['title']}.mp3"
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
    res = replacefunction(format(filename))
    audio = open('C:\\Users\\PC\\PycharmProjects\\myfirstbot\\' + res, 'rb')
    duration = video_info["duration"]
    title = video_info.get("track", None)
    artist = video_info.get("artist", None)
    bot.send_audio(link.chat.id, audio, duration=duration, title=title, performer=artist)
    audio.close()
    os.remove("C:\\Users\\PC\\PycharmProjects\\myfirstbot\\" + res)


bot.polling(none_stop=False, interval=0, timeout=20)
