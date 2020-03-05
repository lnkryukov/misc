# Разное полезное

## Сервис в systemd 

```
[Unit]
Description=Congress Events Flask server
After=network.target

[Service]
User=app
EnvironmentFile=/home/app/envars
WorkingDirectory=/var/www/backend_19288
ExecStartPre=/usr/bin/python3 -m pip install -r requirements.txt
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Содержимое кронтаба 
```
# Рабочая директория приложение, должна быть гит репозиторием
APP_ROOT=/var/www/backend_19288
# Ветка, которую мы разворачиваем
APP_BRANCH=dev
# Сервис systemd, который отвечает за работу приложения
APP_SERVICE=congress-events
*/5 * * * * $HOME/autodeploy.sh >> $HOME/logs/autodeploy.log 2>&1
```

Что редактировать набираем
```bash
crontab -e
```

## Скрипт для автодеплоя
```bash
#!/usr/bin/env bash

cd $APP_ROOT

git fetch origin $APP_BRANCH > /dev/null

LATEST_REMOTE=$(git rev-parse origin/$APP_BRANCH)
LATEST_LOCAL=$(git rev-parse HEAD)

echo "$(date) Latest local is $LATEST_LOCAL"
echo "$(date) Latest remote on branch dev is $LATEST_REMOTE"

if [ "$LATEST_REMOTE" != "$LATEST_LOCAL" ]
then

  echo "$(date) Updating"

  echo "$(date) Stopping service..."
  sudo systemctl stop $APP_SERVICE

  echo "$(date) Checking out..."
  git checkout -f FETCH_HEAD
  #make install

  echo "$(date) Starting service"
  sudo systemctl start $APP_SERVICE
fi
```
