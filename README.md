# stepBOT — Информационный чат-бот на Rasa

[//]: # (ЗДЕСЬ МОЖЕТ БЫТЬ ВАША РЕКЛАМА)
## 🧠 Используемые технологии

- `Rasa 3.6.21`
- `Python 3.9`
- `Redis 5.0.14.1`
- `PosgreSQL 17`
- `HTML/CSS/JavaScript` (для фронтенда)
- `SpeechSynthesis API` (озвучка)
- `Rasa SDK` для кастомных действий (`actions.py`)

## 📁 Структура проекта

```
stepBOTagain/
│
├── actions/                  # Кастомные действия (ответы на вопросы)
│   └── actions.py
├── data/                     # Интенты, правила, истории
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
├── admin/
|    ├── backups/ # Резервные копии
|    │   └── nlu_backup.yml   # YAML-файл с резервной копией NLU
|    │
|    ├── GPT_intents/         # Логика и утилиты для работы с GPT-интентами
|    │   ├── config.py        # Конфигурации
|    │   ├── giga.py          # Основной модуль логики
|    │   ├── nlu_utils.py     # Вспомогательные функции для NLU
|    │   └── redis_cache.py   # Работа с кэшем Redis
|    │
|    ├── static/ # Статические файлы
|    │   ├── image/           # Изображения
|    │   ├── admin.css        # Стили для админки
|    │   ├── app.js           # JavaScript логика
|    │   ├── GPT.css
|    │   └── style.css        # Общие стили
|    │
|    ├── templates/ # HTML-шаблоны
|    │   ├── admin.html       # Шаблон админки
|    │   ├── GPT.html 
|    │   └── index.html       # Главная страница
│
├── app.py # Основной входной скрипт приложения
├── nlu_for_admin.py # NLU логика, адаптированная для админки
|
├── models/                   # Обученные модели
├── image/                    # Графика для интерфейса
├── .rasa/                    # Служебные файлы Rasa
├── .venv/                    # Виртуальное окружение
├── config.yml                # Конфигурация пайплайна и политики
├── credentials.yml           # Настройки каналов (например, REST)
├── domain.yml                # Домейн: интенты, ответы, сущности, слоты
├── endpoints.yml             # Настройки action-сервера
├── index.html                # HTML-интерфейс чат-бота
├── style.css                 # Стилизация интерфейса
└── README.md                 # Документация по проекту (этот файл)
```


так же в корне проекта создать файл .env с такой структурой:

```
AUTHORISATION=ваш токен авторизации giga chat
POSTGRES_USER=postgres
POSTGRES_PASSWORD=HatsuneGoyda
PGHOST=localhost
PGPORT=5432
```


## ⚙️ Установка и запуск

### 1. Клонирование репозитория

```bash
# в терминале
git clone https://github.com/RagnarLongCock/PracticNextStopBot.git
cd NextStepBot
```

### 2. Виртуальное окружение

```bash
# в терминале
python -m venv .venv
.venv\Scripts\activate  # Windows
# или
source .venv/bin/activate  # Linux/macOS
```

### 3. Установка зависимостей

```bash
# в терминале
pip install -r requirenment.txt
```

### 4. Обучение модели

```bash
# в терминале
rasa train
```

### 5. Запуск redis

в терминале переходим в папку с установленным redis

```bash
# В терминале
redis-server.exe
```

### 6. Запуск БД

переходим по данному пути ```C:\Program Files\PostgreSQL\17\pgAdmin 4\runtime```

запускаем файл ```pgAdmin4.exe```

чтобы база данных автоматически очищалась от данных старше 30 дней, добавте файл cleanup.bat в планировщик задач windows


### 7. Запуск приложения

```bash
# В терминале
python admin/app.py
```

### 8. Открытие интерфейса

Напишите в поисковой строке браузера http://127.0.0.1:5000/.

[//]: # (## 🔈 Озвучка)

[//]: # ()
[//]: # (---)

Разработчики: **Максим Бутаков, Орлов Роман, Чурбаков Данила**.  
Платформа: **Rasa + HTML-интерфейс + Python SDK**.
