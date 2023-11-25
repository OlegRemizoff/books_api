<p align="center">
<img src="logo.jpg">
</p>
<!-- <h2 align="center">......</h2> -->

## Описание
Простое API на Django Rest Framework. Присутствует возможность авторизации по профилю github


## Установка

### 1) Перейти в папку с проектом

### 2) Выполнить команду: 
    docker-compose up --build

### 3) Перейти по адресу
     http://127.0.0.1:8000/
---

### Создать администратора
    docker-compose exec django python manage.py createsuperuser


###  Тесты
     docker-compose exec django python manage.py test
### Документация доступна по адресу: 
    http://127.0.0.1:8000/swagger/