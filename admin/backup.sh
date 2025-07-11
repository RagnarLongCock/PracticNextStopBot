#!/bin/bash
mkdir -p ./backup_bd
docker exec practic_db pg_dump -U postgres rasa_db > ./backup_bd/rasa_db_backup_$(date +"%Y-%m-%d_%H-%M-%S").sql
