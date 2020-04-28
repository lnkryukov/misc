#!/usr/bin/env bash

RECREATE_TABLES_FLAG=":crtbls"

cd $APP_ROOT

git fetch origin $APP_BRANCH > /dev/null 2>&1

LATEST_REMOTE=$(git rev-parse origin/$APP_BRANCH)
LATEST_LOCAL=$(git rev-parse HEAD)

#echo "$(date) Latest local is $LATEST_LOCAL"
#echo "$(date) Latest remote on branch dev is $LATEST_REMOTE"

(

  flock -x -w 10 200 || exit 1

  if [ "$LATEST_REMOTE" != "$LATEST_LOCAL" ]
  then

    echo "$(date) Updating"

    echo "$(date) Stopping service..."
    sudo systemctl stop $APP_SERVICE@" "

    echo "$(date) Checking out..."
    git checkout -f FETCH_HEAD > /dev/null 2>&1

    MESSAGE=$(git log -1 --pretty=%B)
    #echo "Commit message is: $MESSAGE"
    for i in $MESSAGE; do
      if [ "$i" = "$RECREATE_TABLES_FLAG" ]; then
        echo "$(date) Recreating tables..."   
        
        echo "$(date) Starting instance..."
        sudo systemctl start $APP_SERVICE@"--create-tables"
        sleep 5
        echo "$(date) Stopping instance..."
        sudo systemctl stop $APP_SERVICE@"--create-tables"
        systemctl status $APP_SERVICE@"--create-tables"
      fi
    done

    echo "$(date) Starting service"
    sudo systemctl start $APP_SERVICE@" "
    systemctl status $APP_SERVICE@" "
  fi
) 200>~/.autodeploy.exclusivelock
