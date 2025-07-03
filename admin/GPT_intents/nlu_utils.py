import shutil
import os

NUL_FILE_PATH = 'data/nlu.yml'
BACKUP_DIR = 'admin/backups/'

def loads_nlu():
    with open(NUL_FILE_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


import yaml


# 👇 Создаём обёртку, чтобы YAML писал блоки как литералы (|-) без экранирования
class LiteralString(str): pass


def literal_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(LiteralString, literal_representer, Dumper=yaml.SafeDumper)


def saves_nlu(data):
    # 👇 Преобразуем поле examples для всех интентов
    for intent in data.get("nlu", []):
        examples = intent.get("examples")
        if examples and not isinstance(examples, LiteralString):
            intent["examples"] = LiteralString(examples)

    with open(NUL_FILE_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, Dumper=yaml.SafeDumper)


def validate_nlu(data):
    if 'nlu' not in data or not isinstance(data['nlu'], list):
        raise ValueError("Invalid NLU structure")

def backup_nlu():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    shutil.copy(NUL_FILE_PATH, os.path.join(BACKUP_DIR, 'nlu_backup.yml'))

def rollback_nlu():
    backup_path = os.path.join(BACKUP_DIR, 'nlu_backup.yml')
    if not os.path.exists(backup_path):
        raise FileNotFoundError("No backup found")
    shutil.copy(backup_path, NUL_FILE_PATH)


def update_nlu(intent, examples):
    data = loads_nlu()
    validate_nlu(data)

    # Удалим старый интент, если он уже есть
    data['nlu'] = [i for i in data['nlu'] if i.get('intent') != intent]

    # Форматируем примеры в нужный блок
    formatted_examples = "\n".join([f"- {ex}" for ex in examples])
    indented = formatted_examples.replace('\n', '\n  ')
    examples_block = f"|\n  {indented}"

    # Добавим интент
    data['nlu'].append({
        "intent": intent,
        "examples": examples_block
    })

    backup_nlu()
    saves_nlu(data)





