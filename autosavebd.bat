@echo off
::set PGPASSWORD=HatsuneGoyda
pg_dump -U rasa_user -d rasa_db -F c -b -v -f "/backups/rasa_$(date +%Y%m%d).backup"

