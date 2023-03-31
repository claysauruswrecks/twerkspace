
.PHONY: build
build:
	docker-compose build


.PHONY: runserver
runserver:
	flask --app app.server run

.PHONY: shell
shell:
	docker-compose \
	 -f ./docker-compose.yaml \
	 run \
	 --rm \
	 -v ${PWD}:/opt/twerkspace/ \
	 flask \
	 bash -c "/bin/bash --login"

.PHONY: stop
stop:
	docker-compose stop
