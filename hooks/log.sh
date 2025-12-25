#!/bin/bash

#Путь к этом файлу
LOG_FILE_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
#Директория hooks
HOOKS_DIR="$(dirname "$LOG_FILE_PATH")"


LOG_LEVEL_DEBUG=0
LOG_LEVEL_INFO=1
LOG_LEVEL_WARNING=2
LOG_LEVEL_ERROR=3

# Текущий уровень логирования (минимальный уровень, который будет выводиться)
CURRENT_LOG_LEVEL=$LOG_LEVEL_DEBUG

# Функция логирования
log() {
    local level=$1
    shift
    local message="$*"

    if [ "$level" -ge "$CURRENT_LOG_LEVEL" ]; then
        case $level in
            $LOG_LEVEL_DEBUG) echo "$(date '+%F %T') [DEBUG] $message" ;;
            $LOG_LEVEL_INFO) echo "$(date '+%F %T') [INFO] $message" ;;
            $LOG_LEVEL_WARNING) echo "$(date '+%F %T') [WARNING] $message" ;;
            $LOG_LEVEL_ERROR) echo "$(date '+%F %T') [ERROR] $message" >&2 ;;
        esac
    fi
}