# Пример API-сервиса для магазина

[Документация по запросам в PostMan](https://documenter.getpostman.com/view/5037826/SVfJUrSc) 



## **Запустить приложение**

     docker-compose -f docker-compose.yml up -d --build

     docker-compose run web python manage.py migrate    


## **Запустить админ панель**
    docker-compose run web python manage.py createsuperuser
   
