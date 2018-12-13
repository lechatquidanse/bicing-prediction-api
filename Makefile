.DEFAULT_GOAL := help
.SILENT:
.PHONY: vendor

## Colors
COLOR_RESET   = \033[0m
COLOR_INFO    = \033[32m
COLOR_COMMENT = \033[33m

## Help
help:
	printf "${COLOR_COMMENT}Usage:${COLOR_RESET}\n"
	printf " make [target]\n\n"
	printf "${COLOR_COMMENT}Available targets:${COLOR_RESET}\n"
	awk '/^[a-zA-Z\-\_0-9\.@]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf " ${COLOR_INFO}%-16s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

##################
# Useful targets #
##################

## Install all install_* requirements and launch project.
install: env_file env_run import_dev

## Run project, install vendors and run migrations.
run: env_run

## Stop project.
stop:
	docker-compose stop

## Down project and remove volumes (databases).
down:
	docker-compose down -v --remove-orphans

## Truncate database and import fixtures.
fixtures: down run import_dev

## Run all quality assurance tools (tests and code inspection).
qa: code_static_analysis test

########
# Code #
########

## Run pylint
code_static_analysis:
	docker-compose run --rm api pylint config src

###############
# Environment #
###############

## Set defaut environment variables by copying env.dist file as .env.
env_file:
	cp .env.dist .env

## Launch docker environment.
env_run:
	docker-compose up -d

###############
# Import Data #
###############

## Import fixtures.
import_dev:
	./docker/development/import-fixtures.sh

####################
# Machine Learning #
####################
create_models:
	docker-compose run --rm api python src/user_interface/cli/flask/command/generate_station_prediction_model.py

########
# Test#
########

## Run tests
test: test_unit

## Run unit tests.
test_unit:
	docker-compose run --rm api python -m unittest discover src "*Test.py"

