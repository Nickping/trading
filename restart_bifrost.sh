#!/bin/bash

APP_NAME="api/bifrost.js"
LOG_FILE="api/bifrost.log"

echo "🔍 실행 중인 $APP_NAME 프로세스 검색 중..."
pids=$(pgrep -f "node .*${APP_NAME}")

if [ -z "$pids" ]; then
  echo "🟢 실행 중인 $APP_NAME 프로세스가 없습니다."
else
  echo "🛑 다음 프로세스를 종료합니다:"
  for pid in $pids; do
    cmd=$(ps -p $pid -o cmd=)
    echo "  - PID: $pid | CMD: $cmd"
    kill "$pid"
  done
  echo "✅ 종료 완료"
fi

# Express 서버 재실행
echo "🚀 $APP_NAME 재실행 중..."
nohup node $APP_NAME > $LOG_FILE 2>&1 &
new_pid=$!
echo "✅ 실행됨 (PID: $new_pid)"