#! /usr/bin/env sh
docker compose --env-file .env -f docker-compose.traefik.yml up --build