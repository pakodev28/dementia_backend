# demencia-backend

## Работа с git
1. При создании новой ветки наследоваться от dev
2. Наименования веток:
    - **feature/название-функционала**
    - **fix/название-бага**

## Требования к стилю
    - используем black, flake8
    - длина строки 119 символов
    - .....

## После того, как вы сделали PR, необходимо:
Написать в Slack'е сообщение со ссылкой на PR, в сообщении отметить @Константин и @Иванов Михаил
В Notion-тикете необходимо добавить ссылку на PR.

## Подготовка окружения для работы:
1. Склонировать проект, перейти в папку demencia-backend, настроить .env файл(устанавливаются значения для DEBUG и SECRET KEY):
    ```shell
    git clone git@github.com:Studio-Yandex-Practicum/demencia-backend.git
    cd demencia-backend
    copy .env.dist .env
    ```
2. Создать виртуальное окружение(на примере venv).
    Linux:
	```shell
    python -m venv venv
    ```
3. Активировать виртуальное окружение. Установить зависимости
    Linux:
	```shell
    source venv/bin/activate
    pip install -r ./requirements/dev.txt
    ```
	Windows:
	```shell
    venv\Scripts\activate.bat
    pip install -r .\requirements\dev.txt
    ```
4. Создать новую ветку и переключиться в нее для работы
	```shell
    git checkout -b feature/название_ветки
    ```
5. Перед выполнением push проверить код flake8, при необходимости откорректировать с помощью black
#### Настройка pre-commit хуков
```
pip install pre-commit
```
```
pre-commit install
```

## Built With

* [Django](https://www.djangoproject.com/) - web framework written in Python.
* [Django-environ](https://django-environ.readthedocs.io/en/latest/) - package that allows you to use Twelve-factor methodology to configure Django application with environment variables.
* [Django-solo](https://pypi.org/project/django-solo/) - Django Solo helps working with singletons.
* [Django-tinymce](https://pypi.org/project/django-tinymce/) - A Django application that contains a widget to render a form field as a TinyMCE editor.
* [Psycopg2](https://pypi.org/project/psycopg2-binary/) - PostgreSQL database adapter for the Python programming language.

## Make команды

[Описание установки make для windows](https://gist.github.com/evanwill/0207876c3243bbb6863e65ec5dc3f058)

* **run** - запуск сервера разработки.
* **migrate** - синхронизация состояние базы данных с текущим состоянием моделей и миграций.
* **lint** - проверка правильности кода.
* **packages** - установка dev-зависимостей.