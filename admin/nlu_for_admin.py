import os
import json

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

yaml_ruamel = YAML()
yaml_ruamel.default_flow_style = False
yaml_ruamel.allow_unicode = True
yaml_ruamel.width = 1000


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