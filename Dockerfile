# Используем официальный образ Python в качестве базового образа
FROM python:3

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Копируем файл requirements.txt внутрь контейнера
COPY requirements.txt ./
# Устанавливаем зависимости, описанные в файле requirements.txt
RUN python -m pip install -r requirements.txt

# Устанавливаем рабочую директорию внутри контейнера
ENV APP_HOME=/usr/src/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles

WORKDIR $APP_HOME
#WORKDIR /usr/src/app
COPY . /usr/src/app


RUN python manage.py collectstatic --noinput
#COPY . /app--settings=mysite.settings.prod


#WORKDIR $APP_HOME



