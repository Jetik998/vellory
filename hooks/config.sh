BACKUP_PASSWORD=123
#Имя директории для бекапа
BACKUP_DIR_NAME="Restic"

#Путь к этом файлу
CONFIG_FILE_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
#Директория hooks
HOOKS_DIR="$(dirname "$CONFIG_FILE_PATH")"
#Директория этого проекта
PROJECT_DIR=$(dirname "$HOOKS_DIR")
#Директория всех проектов
ALL_PROJECTS_DIR="$(dirname "$PROJECT_DIR")"
#Имя проекта
PROJECT_NAME="$(basename "$PROJECT_DIR")"
#Путь директории для бекапа этого проекта
BACKUP_DIR="$HOME/$BACKUP_DIR_NAME/$PROJECT_NAME"

#Имя файлов хука
FILE_NAME="post-commit"
#Директория хуков .git
GIT_HOOKS_DIR="$PROJECT_DIR/.git/hooks"
#Директория хуков .git/hooks
GIT_FILE_PATH="$GIT_HOOKS_DIR/$FILE_NAME"

RESTORE_DIR_NAME="PycharmBackups"
RESTORE_DIR="$HOME/$RESTORE_DIR_NAME"

#echo "Пароль к репозиторию бекапа: $BACKUP_PASSWORD"
#echo "Имя директории бекапа: $BACKUP_DIR_NAME"
#echo "Путь к этом файлу: $THIS_FILE_PATH"
#echo "Путь к директории этого файла: $HOOKS_DIR"
#echo "Путь к директории проекта: $PROJECT_DIR"
#echo "Путь к директории всех проектов: $ALL_PROJECTS_DIR"
#echo "Имя проекта: $PROJECT_NAME"
#echo "Путь к директории бекапа: $BACKUP_DIR"
#echo "Путь к директории hooks в .git: $FILE_NAME"
#echo "Путь к директории hooks в .git: $GIT_HOOKS_DIR"
#echo "Путь к директории hooks в .git: $GIT_FILE_PATH"

#echo "Путь к директории восстановленных файлов: $BACKUP_DIR"
#echo "Имя директории восстановленных файлов: $BACKUP_DIR"
