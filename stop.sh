#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="${APP_DIR}/streamlit.pid"

cd "${APP_DIR}"

if [ ! -f "${PID_FILE}" ]; then
  echo "실행 중인 PID 파일이 없습니다."
  exit 0
fi

pid="$(cat "${PID_FILE}")"

if [ -z "${pid}" ]; then
  echo "PID 파일이 비어 있습니다."
  rm -f "${PID_FILE}"
  exit 0
fi

if kill -0 "${pid}" 2>/dev/null; then
  kill "${pid}"
  echo "앱을 종료했습니다. PID=${pid}"
else
  echo "프로세스가 이미 종료되어 있습니다. PID=${pid}"
fi

rm -f "${PID_FILE}"
