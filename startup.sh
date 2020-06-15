#!/bin/bash

PID_FILE="${PWD}/.pid"

DATE=$(date)

function startup() {
  echo -e "$DATE - $(git pull origin master)\n"
  echo -e "$DATE - $(pip install --upgrade -r requirements.txt)\n"
  echo -e "$DATE - $(nohup python bot.py > ./output.txt 2>&1 &)\n"
  echo $! > $PID_FILE
  echo -e "$DATE - Started new Discord Bot process\n"
}

echo -e "$DATE - Using pidfile ${PID_FILE}"
if [ -f "$PID_FILE" ]; then
  if pgrep -F $PID_FILE; then
      echo -e "$DATE - Process already running\n"
  else
      echo -e "$DATE - Process not running, starting up...\n"
      startup
  fi
else
  startup
fi
