source venv/bin/activate
export TWITCHUSERNAME="<TWITCH BOT USERNAME HERE>" TWITCHTOKEN="<TWITCH OAUTH TOKEN INCLUDING 'oath:' HERE>" TWITCHCHANNEL="<DESIRED TWITCH CHANNEL HERE>" IEXTOKEN="<IEX TOKEN HERE>" 
python3 main.py &
python3 schedulemanager.py &
python3 asyncchatbot.py &
