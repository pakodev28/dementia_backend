run:
	python manage.py runserver
migrate:
	python manage.py makemigrations
	python manage.py migrate
lint:
	isort ./ && flake8 ./