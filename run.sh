#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="${APP_DIR}/streamlit.pid"
LOG_FILE="${APP_DIR}/streamlit.log"
PORT="${PORT:-8501}"
HOST="${HOST:-0.0.0.0}"

cd "${APP_DIR}"

if [ ! -f ".env" ]; then
  echo ".env 파일이 없습니다. .env.example을 참고해서 생성하세요."
  exit 1
fi

if [ ! -x ".venv/bin/streamlit" ]; then
  echo ".venv 또는 streamlit 실행 파일이 없습니다. 먼저 가상환경과 의존성을 설치하세요."
  exit 1
fi

if [ -f "${PID_FILE}" ]; then
  pid="$(cat "${PID_FILE}")"
  if [ -n "${pid}" ] && kill -0 "${pid}" 2>/dev/null; then
    echo "이미 실행 중입니다. PID=${pid}"
    exit 0
  fi
fi

setsid ./.venv/bin/streamlit run app.py \
  --server.headless true \
  --server.port "${PORT}" \
  --server.address "${HOST}" \
  > "${LOG_FILE}" 2>&1 < /dev/null &

pid=$!
echo "${pid}" > "${PID_FILE}"

sleep 2

if kill -0 "${pid}" 2>/dev/null; then
  echo "앱이 실행되었습니다. PID=${pid}"
  echo "로그: ${LOG_FILE}"
else
  echo "앱 기동에 실패했습니다. 로그를 확인하세요: ${LOG_FILE}"
  exit 1
fi
