
::set PGPASSWORD=HatsuneGoyda
docker exec -i practic_db psql -U postgres -d rasa_db < cleanup.sql


::Запусти "Планировщик заданий Windows"
::Добавь задание: запуск cleanup.bat раз в сутки