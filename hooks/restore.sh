#!/bin/bash


#Начало работы:
# chmod +x ./hooks/restore.sh
# ./hooks/restore.sh


#Путь к этом файлу
RESTORE_FILE_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
#Директория hooks
HOOKS_DIR="$(dirname "$RESTORE_FILE_PATH")"

source "$HOOKS_DIR/config.sh"
source "$HOOKS_DIR/log.sh"
source "$HOOKS_DIR/backup.sh"

restoring() {
  log $LOG_LEVEL_INFO "[restoring](start) Восстановление файлов"
  if check_repo; then
    log $LOG_LEVEL_DEBUG "Запуск восстановления"
    restic -r "$BACKUP_DIR" restore latest --target "$RESTORE_DIR" || { log $LOG_LEVEL_ERROR "Ошибка при восстановлении" >&2; exit 1; }
    log $LOG_LEVEL_INFO "[restoring](done) Восстановление файлов завершено успешно"
  else
    log $LOG_LEVEL_WARNING "[restoring](check_repo) Восстановление прервано, репозиторий не найден!"
  fi
}

restoring