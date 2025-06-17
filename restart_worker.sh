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
nohup python3 ./worker/app.py > ./worker/app.log 2>&1 &
new_pid=$!
echo "✅ 실행됨 (PID: $new_pid)"


PORT=5555

echo "🚀 streamlit 종료중"
echo "🔍 포트 $PORT 사용 중인 프로세스 검색 중..."
pids=$(lsof -ti tcp:$PORT)

if [ -z "$pids" ]; then
  echo "✅ 포트 $PORT 사용 중인 프로세스 없음."
else
  echo "🛑 포트 $PORT 사용 중인 프로세스 종료:"
  for pid in $pids; do
    echo "  - PID: $pid 종료"
    kill -9 $pid
  done
  echo "✅ 종료 완료"
fi

# ▶️ 4. dashboard 재실행
echo "🚀 streamlit 실행중"
streamlit run ./worker/page/page.py --server.address=0.0.0.0 --server.port=5555 --server.enableCORS false


Backtesting_PORT=5556

echo "🚀 backtest 종료중"
echo "🔍 포트 $Backtesting_PORT 사용 중인 프로세스 검색 중..."
pids=$(lsof -ti tcp:$Backtesting_PORT)

if [ -z "$pids" ]; then
  echo "✅ 포트 $Backtesting_PORT 사용 중인 프로세스 없음."
else
  echo "🛑 포트 $Backtesting_PORT 사용 중인 프로세스 종료:"
  for pid in $pids; do
    echo "  - PID: $pid 종료"
    kill -9 $pid
  done
  echo "✅ 종료 완료"
fi


# ▶️ 4. backtes 재실행
echo "🚀 backtest 실행중"
streamlit run ./worker/backtesting.py --server.address=0.0.0.0 --server.port=5556 --server.enableCORS false

