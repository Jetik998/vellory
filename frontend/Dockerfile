FROM nginx:1.29.4

WORKDIR /etc/nginx/frontend/

COPY ./avatars/ ./avatars
COPY ./static/ ./static
COPY ./templates/ ./templates
# Установить владельца и права одной командой
RUN chown -R nginx:nginx /etc/nginx/frontend && \
    chmod -R 755 /etc/nginx/frontend

COPY ./nginx /etc/nginx

# Открываем 80-й порт
EXPOSE 80 223

# Запускаем Nginx (эта команда уже есть в базовом образе,
# но ее часто пишут для наглядности)
CMD ["nginx", "-g", "daemon off;"]