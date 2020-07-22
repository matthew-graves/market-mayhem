service redis-server start
python -u main.py &
python -u asyncchatbot.py &
python -u schedulemanager.py
