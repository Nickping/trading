
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

