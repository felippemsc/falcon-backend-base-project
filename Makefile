all:
	python setup.py build

check:
	docker-compose up -d
	sleep .5
	coverage run --source base_project setup.py test --verbose
	docker-compose stop
	sleep .5
	coverage report -m

lint: all
	python lint.py