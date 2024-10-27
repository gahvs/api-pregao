IMAGE_NAME=pregao-api-dev

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -p 8000:8000 \
		-e POSTGRES_HOST=$(POSTGRES_HOST) \
		-e POSTGRES_PORT=$(POSTGRES_PORT) \
		-e POSTGRES_PASS=$(POSTGRES_PASS) \
		-e POSTGRES_USER=$(POSTGRES_USER) \
		-e POSTGRES_DATABASE=$(POSTGRES_DATABASE) \
		-e POSTGRES_SCHEMA=$(POSTGRES_SCHEMA) \
		$(IMAGE_NAME)

run-env:
	docker run -p 8000:8000 $(IMAGE_NAME)

stop:
	docker stop $$(docker ps -q --filter ancestor=$(IMAGE_NAME))
	docker rm $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME))

remove:
	docker rmi $(IMAGE_NAME)
