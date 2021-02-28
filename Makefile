SHELL := /bin/bash
.PHONY : all

build: ## build
	docker build -t storage .

run: ## run
	docker rm /storage; \
	docker run -it --rm \
	--env-file ${CURDIR}/env/staging_env/config.env \
	--env-file ${CURDIR}/env/staging_env/urls.env \
	--env-file ${CURDIR}/env/staging_env/secrets.env \
	-p 5000:80 \
	-p 80:80 \
	--name storage \
	storage


# General commands

clean: ##
	rm *.jpg; \
	rm *.png; \
	rm Flaskapi_invscan/logs/*; \
	docker rm /storage_test; \
	docker rm /storage_development; \
	docker stop $$(docker ps -aq); \
	docker rm $$(docker ps -aq); \
	docker -y system prune; \
	dropdb storage_db; \
	echo "Cleaned"

delete_containers: ## delete ALL active containers
	docker stop $$(docker ps -aq); \
	docker rm $$(docker ps -aq);

reshell: build shell ## rebuild and make (mounted) shell
rerun: build run ## rebuild and run


help: ##
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
