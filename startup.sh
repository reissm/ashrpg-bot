#!/bin/bash

PID_FILE=".pid"

DATE=$(date)

function startup() {
  echo "$DATE - $(git pull origin master && echo 'Successfully updated git')\n"
  echo "$DATE - $(pip install --upgrade -r requirements.txt && echo 'Successfully updated pip')\n"
  echo "$DATE - $(nohup python bot.py > ./output.txt 2>&1 & && echo 'Successfully started the nohup')\n"
  echo $! > $PID_FILE
  echo "$DATE - Started new Discord Bot process"
}

if [ -f "$PID_FILE" ]; then
  PROCESS=$(echo "$PID_FILE")

  if pgrep -F $PID_FILE; then
      echo "$DATE - Process already running"
  else
      echo "$DATE - Process not running, starting up..."
      startup
  fi
else
  startup
fi
