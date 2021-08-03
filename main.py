import telebot
import youtube_dl
import os
import sys

try:
    bot = telebot.TeleBot("{}".format(sys.argv[1]), parse_mode=None)
except IndexError:
    print("for everything to work, you need to pass the token as a parameter to the start of the program. write in terminal 'python main.py token' where main.py is name of your program file and token is YOUR token ")
    sys.exit()

def replacefunction(somestr):  #Python does not read some characters and replaces them with a #, we do it right away, so that later we can find the correct file name
    result = ''
    for i in somestr:
        if i == '|' or i == '`':
            i = '#'
        result += i
    return result


@bot.message_handler(commands=['start', 'help'])  #bot reaction to /start and /help
def send_welcome(message):
    bot.send_message(message.chat.id, "the only thing you need is the URL of the YouTube video you want to extract the audio from. just text /getfile and follow instructions")


@bot.message_handler(commands=['getfile'])  #bot reaction to /getfile
def send_welcome(message):
    sent = bot.send_message(message.chat.id, "send me your link)")
    bot.register_next_step_handler(sent, filecreation)


def filecreation(link):
    bot.send_message(link.chat.id, "it takes a little time to create the file...")
    video_url = link.text
    try:
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
        mypath = os.getcwd()
        try:
            audio = open(mypath + '\\' + res, 'rb')
            duration = video_info["duration"]
            title = video_info.get("track", None)
            artist = video_info.get("artist", None)
            bot.send_audio(link.chat.id, audio, duration=duration, title=title, performer=artist)
            audio.close()
            os.remove(mypath + '\\' + res)
        except OSError:
            bot.send_message(link.chat.id, "there are some problems with the file name. try to find this video with a different title or write to the bot developer")
    except:
        bot.send_message(link.chat.id, "check if everything is good with the link, if the video is not private and if everything is ok, write to the bot developer")

bot.polling(none_stop=False, interval=0, timeout=20)
