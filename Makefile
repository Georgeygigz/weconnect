shell:
	pipenv shell
install:
	pipenv install
migrations:
	python manage.py makemigrations
migrate:
	python3 manage.py migrate
collectstatic:
	python manage.py collectstatic
server:
	python3 manage.py runserver
