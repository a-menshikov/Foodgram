FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY foodgram/ .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]

# WORKDIR /app

# COPY requirements.txt /app

# RUN python -m pip install --upgrade pip

# RUN pip3 install -r /app/requirements.txt --no-cache-dir

# COPY . .

# CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]


# FROM python:3.10-slim

# # Создать директорию вашего приложения.
# RUN mkdir /app

# # Скопировать с локального компьютера файл зависимостей
# # в директорию /app.
# COPY requirements.txt /app

# RUN python -m pip install --upgrade pip
# # Выполнить установку зависимостей внутри контейнера.
# RUN pip3 install -r /app/requirements.txt --no-cache-dir

# # Скопировать содержимое директории /api_yamdb c локального компьютера
# # в директорию /app.
# COPY foodgram/ /app

# # Сделать директорию /app рабочей директорией. 
# WORKDIR /app

# # Выполнить запуск сервера разработки при старте контейнера.
# CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ] 