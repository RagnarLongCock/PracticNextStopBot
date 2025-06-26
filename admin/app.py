from flask import Flask, jsonify, request, render_template
import yaml
import os
import subprocess

# Абсолютные пути
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
NLU_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "nlu.yml"))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),  # admin/templates
    static_folder=os.path.join(BASE_DIR, "static")        # на будущее
)

# Загрузка интентов из nlu.yml
def load_nlu():
    with open(NLU_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    intents = {}
    for item in data.get("nlu", []):
        intent_name = item.get("intent")
        examples = item.get("examples", "")
        lines = [line.strip("- ").strip() for line in examples.strip().split("\n") if line.strip()]
        intents[intent_name] = lines
    return intents

# Сохранение интентов в nlu.yml
def save_nlu(intents):
    data = {"version": "3.1", "nlu": []}
    for name, examples in intents.items():
        examples_text = "\n".join([f"- {e}" for e in examples])
        data["nlu"].append({"intent": name, "examples": examples_text})
    with open(NLU_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

# Главная страница
@app.route("/")
def index():
    return render_template("admin.html")

# Получить список интентов
@app.route("/api/intents", methods=["GET"])
def get_intents():
    intents = load_nlu()
    return jsonify(list(intents.keys()))

# Получить примеры для интента
@app.route("/api/intents/<intent>", methods=["GET"])
def get_examples(intent):
    intents = load_nlu()
    return jsonify(intents.get(intent, []))

# Добавить новый интент
@app.route("/api/intents", methods=["POST"])
def add_intent():
    name = request.json.get("name")
    intents = load_nlu()
    if name not in intents:
        intents[name] = []
        save_nlu(intents)
        return jsonify({"message": "Интент добавлен"}), 201
    return jsonify({"message": "Интент уже существует"}), 409

# Добавить пример к интенту
@app.route("/api/intents/<intent>", methods=["POST"])
def add_example(intent):
    text = request.json.get("text")
    intents = load_nlu()
    if intent not in intents:
        return jsonify({"error": "Интент не найден"}), 404
    if text not in intents[intent]:
        intents[intent].append(text)
        save_nlu(intents)
    return jsonify({"message": "Фраза добавлена"})

# Переобучение модели
@app.route("/api/train", methods=["POST"])
def train():
    try:
        result = subprocess.run(["rasa", "train"], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "Переобучение завершено успешно"})
        else:
            return jsonify({"message": f"Ошибка: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
