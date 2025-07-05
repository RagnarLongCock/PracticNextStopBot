@echo off
set PGPASSWORD=HatsuneGoyda
"C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d rasa_db -f "cleanup.sql"

::Запусти "Планировщик заданий Windows"
::Добавь задание: запуск cleanup.bat раз в сутки