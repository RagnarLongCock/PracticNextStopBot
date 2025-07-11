@echo off
set PGPASSWORD=HatsuneGoyda
pg_dump -U rasa_user -d rasa_db -F c -b -v -f "C:\Backups\rasa_%date:~-4%%date:~3,2%%date:~0,2%.backup"
