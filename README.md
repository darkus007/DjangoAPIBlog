# DjangoAPIBlog v.1.0
Блог на Django и Django REST framework. Работа с приложением только через RESTFull API. 

Реализована регистрация и авторизация пользователей с помощью токенов по средствам dj-rest-auth в сочетании с django-allauth. \
Читать посты могут все без регистрации. 
Создавать могут только зарегистрированные пользователи, редактировать и удалять - только авторы постов. 
Читать список пользователей могут все, редактировать доступно только администраторам сайта.

Документация сформирована автоматически с использованием Swagger и ReDoc. Доступна по адресам `swagger/` и `redoc/` соответственно.

Приложение написано на [Python v.3.11](https://www.python.org). \
При разработке использованы следующие основные пакеты, фреймворки и технологии: \
[Django](https://pypi.org/project/Django/); \
[Django REST framework](https://www.django-rest-framework.org); \
[dj-rest-auth](https://pypi.org/project/dj-rest-auth/); \
[django-allauth](https://pypi.org/project/django-allauth/); \
[Swagger](https://django-rest-swagger.readthedocs.io/en/latest/); \
[ReDoc](https://github.com/Redocly/redoc); \
[Docker](https://www.docker.com/).

Полный список в фале `requirements.txt`.

База данных [SQLite](https://sqlite.org/index.html).

### Описание Models
> Post - Посты.
>> id - уникальный идентификатор, присваивается автоматически.\
>> title - заголовок поста.\
>> body - текст поста. \
>> created_at - дата создания поста, присваивается автоматически. \
>> updated_at - дата обновления поста, присваивается автоматически. \
>> author - автор поста, связь один со многими с моделью django.contrib.auth.models.User.

## Установка и запуск

#### Локально на Вашем устройстве (используя отладочный сервер)
1. Скачайте DjangoAPIBlog на Ваше устройство любым удобным способом (например Code -> Download ZIP, распакуйте архив).
2. Установите [Python](https://www.python.org), если он у Вас еще не установлен.
3. Установите необходимые для работы приложения модули. Для этого откройте терминал, перейдите в каталог с приложением (cd <путь к приложению>/DjangoAPIBlog), выполните команду `pip3 install -r requirements.txt`. Если Вы пользователь Microsoft Windows, то вместо `pip3 install ...` следует использовать  `pip install -r requirements.txt`
4. Установите [переменную окружения](https://wiki.archlinux.org/title/Environment_variables_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)) `SECRET_KEY`, например выполнив в терминале `export SECRET_KEY="ваш_сложный_секретный_ключ_djang"`.
5. Перейдите в папку `website` (`cd website` или `dir website` для Windows) выполните команду `python3 manage.py runserver` (Для Microsoft Windows `python manage.py runserver`).
6. Откройте любимый Веб-браузер и перейдите по адресу http://127.0.0.1:8000/redoc/ или http://127.0.0.1:8000/swagger/ для просмотра документации RESTFull API данного приложения.
#### В контейнере Docker (используя отладочный сервер)
1. Скачайте DjangoAPIBlog на Ваше устройство любым удобным способом (например Code -> Download ZIP, распакуйте архив).
2. Установите [Docker](https://www.docker.com/), если он у Вас еще не установлен.
3. Откройте терминал, перейдите в каталог с приложением (cd <путь к приложению>/DjangoAPIBlog).
4. В Dockerfile установите Ваши значения переменных окружения `SECRET_KEY`, `DJANGO_SUPERUSER_PASSWORD`, `DJANGO_SUPERUSER_EMAIL` и `DJANGO_SUPERUSER_USERNAME`.
5. Выполните сборку Docker образа (image) `docker build -t django_api_blog .`.
6. Запустите контейнер `docker run -p 8000:8000 -d django_api_blog`.
7. Откройте любимый Веб-браузер и перейдите по адресу http://127.0.0.1:8000/redoc/ или http://127.0.0.1:8000/swagger/ для просмотра документации RESTFull API данного приложения.