fuser -k 10099/tcp

nohup python app/main.py > logs/app.log 2>&1 &