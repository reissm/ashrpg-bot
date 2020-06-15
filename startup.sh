#!/bin/bash

PID_FILE=".pid"

function startup() {
  nohup my_command > ./output.txt 2>&1 &
  echo $! > $PID_FILE
  echo "Started new Discord Bot process"
}

if [ -f "$PID_FILE" ]; then
  PROCESS=$(echo "$PID_FILE")

  if pgrep -F $PID_FILE; then
      echo "Process already running"
  else
      echo "Process not running, starting up..."
      startup
  fi
else
  startup
fi
