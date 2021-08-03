Telegram bot: 
when user presses /start, the bot explains how it works - "the only thing you need is the URL of the YouTube video you want to extract the audio from. just text /getfile and follow instructions". the same works for /help 
principle of operation: 
the user presses /getfile, then bot asks to send him a link. and bot will respond by sending an mp3 file.

first, you need to develop a function that accepts a link from YouTube and downloads an mp3 file. I did it using the library youtube_dl. you can install it using "pip install youtube_dl"
then you need to create a bot. use this link https://python-telegram-bot.readthedocs.io/en/stable/ , there is detailed information about the bot in python. and after that you just need to attach your function here

for everything to work, you need to pass the token as a parameter to the start of the program. being in the right directive write in terminal 'python main.py token' where main.py is name of your program file and token is YOUR token 
