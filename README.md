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
1. Склонировать проект, перейти в папку demencia-backend
    ```shell
    git clone git@github.com:Studio-Yandex-Practicum/demencia-backend.git
    cd demencia-backend
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
    pip -r /requirements/dev.txt
    ```
	Windows:
	```shell
    venv\Scripts\activate.bat
    pip -r /requirements/dev.txt
    ```
3. Создать новую ветку и переключиться в нее для работы
	```shell
    git checkout -b feature/название_ветки
    ```
	Windows:
	```shell
    venv\Scripts\activate.bat
    pip -r /requirements/dev.txt
    ```
