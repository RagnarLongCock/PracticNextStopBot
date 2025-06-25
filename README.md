# stepBOT — Информационный чат-бот на Rasa
ЗДЕСЬ МОЖЕТ БЫТЬ ВАША РЕКЛАМА
## 🧠 Используемые технологии

- `Rasa 3.6.21`
- `Python 3.9`
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

## ⚙️ Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/RagnarLongCock/PracticNextStopBot.git
cd NextStepBot
```

### 2. Виртуальное окружение

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# или
source .venv/bin/activate  # Linux/macOS
```

### 3. Установка зависимостей

```bash
pip install rasa==3.6.21
pip install rasa-sdk
```

### 4. Обучение модели

```bash
rasa train
```

### 5. Запуск серверов

```bash
# В первом терминале
rasa run actions

# Во втором терминале
rasa run --enable-api
```

### 6. Открытие интерфейса

Открой файл `index.html` в браузере.

## 🔈 Озвучка

---

Разработчики: **Максим Бутаков, Орлов Роман, Чурбаков Данила**.  
Платформа: **Rasa + HTML-интерфейс + Python SDK**.
