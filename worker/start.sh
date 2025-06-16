#!/bin/bash

# 🔍 1. 현재 실행 중인 app.py 프로세스 찾기
pids=$(pgrep -f "app.py")

if [ -z "$pids" ]; then
  echo "🟢 실행 중인 app.py 프로세스가 없습니다."
else
  echo "🛑 다음 app.py 프로세스를 종료합니다:"
  for pid in $pids; do
    cmd=$(ps -p $pid -o cmd=)
    echo "  - PID: $pid | CMD: $cmd"
    kill "$pid"
  done
  echo "✅ 종료 완료"
fi

# ▶️ 2. app.py 재실행
echo "🚀 app.py 재실행 중..."
# nohup python3 app.py > app.log 2>&1 &
new_pid=$!
echo "✅ 실행됨 (PID: $new_pid)"
