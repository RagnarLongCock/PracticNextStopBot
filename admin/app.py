from flask import Flask, jsonify, request, render_template
import os
import subprocess
import json
import sys
import psutil
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
ACTIONS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "actions"))

NLU_FILE = os.path.join(DATA_DIR, "nlu.yml")
DOMAIN_FILE = os.path.join(BASE_DIR, "..", "domain.yml")
RESPONSES_FILE = os.path.join(DATA_DIR, "responses.json")
RULES_FILE = os.path.join(DATA_DIR, "rules.yml")
ACTIONS_FILE = os.path.join(ACTIONS_DIR, "actions.py")

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"), static_folder=os.path.join(BASE_DIR, "static"))

yaml_ruamel = YAML()
yaml_ruamel.default_flow_style = False
yaml_ruamel.allow_unicode = True
yaml_ruamel.width = 1000

# === NLU ===
def load_nlu():
    with open(NLU_FILE, encoding="utf-8") as f:
        data = yaml_ruamel.load(f)
    intents = {}
    for item in data.get("nlu", []):
        name = item.get("intent")
        examples = item.get("examples", "")
        lines = [line.strip("- ").strip() for line in str(examples).split("\n") if line.strip()]
        intents[name] = lines
    return intents

def save_nlu(intents):
    data = {"version": "3.1", "nlu": []}
    for name, examples in intents.items():
        clean_examples = [e.strip() for e in examples if isinstance(e, str) and e.strip()]
        examples_block = "\n".join([f"- {ex}" for ex in clean_examples]) if clean_examples else "- пример"
        data["nlu"].append({
            "intent": name.strip(),
            "examples": LiteralScalarString(examples_block)
        })
    with open(NLU_FILE, "w", encoding="utf-8") as f:
        yaml_ruamel.dump(data, f)

# === DOMAIN ===
def update_domain_with_intent(intent_name):
    with open(DOMAIN_FILE, encoding="utf-8") as f:
        domain = yaml_ruamel.load(f)

    domain.setdefault("intents", [])
    if intent_name not in domain["intents"]:
        domain["intents"].append(intent_name)

    domain.setdefault("actions", [])
    action_name = f"action_{intent_name}"
    if action_name not in domain["actions"]:
        domain["actions"].append(action_name)

    with open(DOMAIN_FILE, "w", encoding="utf-8") as f:
        yaml_ruamel.dump(domain, f)

# === RESPONSES ===
def load_responses():
    if os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_responses(data):
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# === RULES ===
def add_rule_for_custom_action(intent_name):
    if not os.path.exists(RULES_FILE):
        rules_data = {"version": "3.1", "rules": []}
    else:
        with open(RULES_FILE, encoding="utf-8") as f:
            rules_data = yaml_ruamel.load(f)

    rule_title = f"Ответ на вопрос {intent_name}"
    new_rule = {
        "rule": rule_title,
        "steps": [
            {"intent": intent_name},
            {"action": f"action_{intent_name}"}
        ]
    }

    if "rules" not in rules_data:
        rules_data["rules"] = []

    exists = any(r.get("rule") == rule_title for r in rules_data["rules"])
    if not exists:
        rules_data["rules"].append(new_rule)

    with open(RULES_FILE, "w", encoding="utf-8") as f:
        yaml_ruamel.dump(rules_data, f)

# === ACTION ===
def append_action_to_file(intent_name):
    class_name = "Action" + "".join(word.capitalize() for word in intent_name.split("_"))
    action_name = f"action_{intent_name}"
    code = f"""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class {class_name}(Action):
    def name(self) -> Text:
        return "{action_name}"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if RESPONSES.get("{action_name}", {{}}).get(program):
            text = RESPONSES["{action_name}"][program]
        else:
            text = RESPONSES.get("{action_name}", {{}}).get("default", "Бот пока не знает, что ответить.")
        dispatcher.utter_message(text=text)
        return []
"""
    with open(ACTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(code)

# === ROUTES ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/api/intents", methods=["GET"])
def get_intents():
    return jsonify(list(load_nlu().keys()))

@app.route("/api/intents/<intent>", methods=["GET"])
def get_examples(intent):
    return jsonify(load_nlu().get(intent, []))

@app.route("/api/intents", methods=["POST"])
def add_intent():
    name = request.json.get("name")
    intents = load_nlu()
    if name in intents:
        return jsonify({"message": "Интент уже существует"}), 409

    intents[name] = []
    save_nlu(intents)
    update_domain_with_intent(name)
    add_rule_for_custom_action(name)

    responses = load_responses()
    responses[f"action_{name}"] = {"default": ""}
    save_responses(responses)

    append_action_to_file(name)

    return jsonify({"message": f"Интент '{name}' добавлен"}), 201

@app.route("/api/intents/<intent>", methods=["POST"])
def add_example(intent):
    text = request.json.get("text")
    intents = load_nlu()
    if intent not in intents:
        return jsonify({"error": "Интент не найден"}), 404
    if text and text not in intents[intent]:
        intents[intent].append(text)
        save_nlu(intents)
    return jsonify({"message": "Фраза добавлена"})

@app.route("/api/intents/<intent>/<int:index>", methods=["DELETE"])
def delete_example(intent, index):
    intents = load_nlu()
    if intent not in intents or index >= len(intents[intent]):
        return jsonify({"error": "Неверный интент или индекс"}), 404
    intents[intent].pop(index)
    save_nlu(intents)
    return jsonify({"message": "Фраза удалена"})

@app.route("/api/responses", methods=["GET"])
def get_responses():
    return jsonify(load_responses())

@app.route("/api/responses/<action>", methods=["POST"])
def update_response(action):
    text = request.json.get("text", "")
    responses = load_responses()
    if isinstance(responses.get(action), dict):
        responses[action]["default"] = text
    else:
        responses[action] = {"default": text}
    save_responses(responses)
    return jsonify({"message": f"Ответ для '{action}' обновлён"})

@app.route("/api/train", methods=["POST"])
def train_model():
    try:
        result = subprocess.run([sys.executable, "-m", "rasa", "train"], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "✅ Модель успешно переобучена"})
        else:
            return jsonify({"message": f"❌ Ошибка при обучении:\n{result.stderr}"}), 500
    except Exception as e:
        return jsonify({"message": f"❌ {str(e)}"}), 500

# === BOT CONTROL ===
bot_process = None
actions_process = None

def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        return True
    except Exception:
        return False

@app.route("/api/start-bot", methods=["POST"])
def start_bot():
    global bot_process, actions_process

    try:
        if bot_process is None:
            bot_process = subprocess.Popen([
                "rasa", "run", "--enable-api", "-p", "5010", "--cors", "*"
            ])
        if actions_process is None:
            actions_process = subprocess.Popen([
                "rasa", "run", "actions", "-p", "5055"
            ])
        return jsonify({"message": "✅ Бот и actions запущены"})
    except Exception as e:
        return jsonify({"message": f"❌ Ошибка запуска: {str(e)}"}), 500

@app.route("/api/stop-bot", methods=["POST"])
def stop_bot():
    global bot_process, actions_process
    try:
        stopped = []
        if bot_process:
            if kill_process_tree(bot_process.pid):
                stopped.append("бот")
            bot_process = None
        if actions_process:
            if kill_process_tree(actions_process.pid):
                stopped.append("actions")
            actions_process = None
        if not stopped:
            return jsonify({"message": "⚠️ Бот и actions уже остановлены"})
        return jsonify({"message": f"🛑 Остановлено: {', '.join(stopped)}"})
    except Exception as e:
        return jsonify({"message": f"❌ Ошибка остановки: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
