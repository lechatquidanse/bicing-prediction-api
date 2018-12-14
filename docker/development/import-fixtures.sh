#!/usr/bin/env bash

docker-compose exec bicing_api_db unzip /var/data/fixtures.zip -d /var/data
docker-compose exec bicing_api_db psql -d symfony -U symfony -f /var/data/symfony_public_station.sql > /dev/null
docker-compose exec bicing_api_db psql -d symfony -U symfony -f /var/data/symfony_public_station_state.sql > /dev/null
docker-compose exec bicing_api_db rm /var/data/symfony_public_station.sql
docker-compose exec bicing_api_db rm /var/data/symfony_public_station_state.sql
