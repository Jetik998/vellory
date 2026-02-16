#!/bin/bash

# Скрипт для автоматического создания и управления бэкапами проекта с помощью Restic.

# Функционал:
# 1. Создает Restic-репозиторий для текущего проекта в папке ~/Restic/{имя_проекта}, если репозиторий ещё не существует.
# 2. После каждого git-коммита автоматически делает бэкап всего проекта.
# 3. Логи отображают успешное создание snapshot'а и количество добавленных/измененных файлов.

#Начало работы:
# chmod +x hooks/*.sh
# ./hooks/backup.sh

#Путь к этом файлу
BACKUP_FILE_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
#Директория hooks
HOOKS_DIR="$(dirname "$BACKUP_FILE_PATH")"

source "$HOOKS_DIR/config.sh"
source "$HOOKS_DIR/log.sh"


#Экспортируем пароль и репозиторий
export RESTIC_PASSWORD=$BACKUP_PASSWORD
export RESTIC_REPOSITORY=$BACKUP_DIR

check_repo() {
  log $LOG_LEVEL_DEBUG "[check_repo](start) Поиск репозитория бекапа"

  if [ ! -d "$BACKUP_DIR" ]; then
    log $LOG_LEVEL_DEBUG "Репозиторий не найден"
    return 1
  else
    log $LOG_LEVEL_DEBUG "Репозиторий найден $BACKUP_DIR"
    return 0
  fi
}

create_backup() {
  log $LOG_LEVEL_DEBUG "[init_post_commit](start)"
  log $LOG_LEVEL_INFO "Создание бекапа"

  if ! check_repo; then
    restic init || { log $LOG_LEVEL_ERROR "Ошибка создания репозитория" >&2; exit 1; }
    log $LOG_LEVEL_DEBUG "Создан репозиторий"
  fi

  (
    cd "$ALL_PROJECTS_DIR" || { log $LOG_LEVEL_ERROR "Директория не найдена"; exit 1; }
    restic -r "$BACKUP_DIR" --verbose backup "$PROJECT_NAME" || { log $LOG_LEVEL_ERROR "Неизвестная ошибка" >&2; exit 1; }
    log $LOG_LEVEL_INFO "Бекап создан. Дата: $(date '+%Y-%m-%d %H:%M:%S')"
  )
}


#Создаем файл post-commit и отправляем в папку .git/hooks
cat <<EOF > "$GIT_FILE_PATH"
#!/bin/bash

#Импортируем скрипт
source "$BACKUP_FILE_PATH" || { echo "Ошибка импорта BACKUP_FILE_PATH" >&2; exit 1; }
source "$HOOKS_DIR/log.sh" || { echo "Ошибка импорта HOOKS_DIR/log.sh" >&2; exit 1; }

log $LOG_LEVEL_DEBUG "Скрипт $BACKUP_FILE_PATH успешно импортирован!"

#Функция из скрипта backup.sh
create_backup || { log $LOG_LEVEL_ERROR "[create_backup](in .git/hooks) Ошибка при создании бекапа" >&2; exit 1; }

log $LOG_LEVEL_INFO "[create_backup](.git/hooks) Успешно"

EOF
#Делаем исполняемым
chmod +x "$GIT_FILE_PATH"