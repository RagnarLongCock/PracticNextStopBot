from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import os

# Путь к responses.json
RESPONSES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "responses.json")

# Загрузка ответов
def load_responses():
    with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

RESPONSES = load_responses()

# Универсальная функция получения default-ответа
def get_default_response(action_name: str) -> str:
    return RESPONSES.get(action_name, {}).get("default", "Бот пока не знает, что ответить.")

# Функция получения ответа по смене
def get_program_response(action_name: str, program: str) -> str:
    if not RESPONSES.get(action_name):
        return "Нет данных для этого действия."
    return RESPONSES[action_name].get(program, RESPONSES[action_name].get("default", "Пожалуйста, уточните смену."))


# Классы кастомных действий:

class ActionAskAboutDates(Action):
    def name(self) -> Text:
        return "action_ask_about_dates"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        dispatcher.utter_message(text=get_program_response("action_ask_about_dates", program))
        return []


class ActionAskAboutTheme(Action):
    def name(self) -> Text:
        return "action_ask_about_theme"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        dispatcher.utter_message(text=get_program_response("action_ask_about_theme", program))
        return []


class ActionAskAboutFood(Action):
    def name(self) -> Text:
        return "action_ask_about_food"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_default_response("action_ask_about_food"))
        return []


class ActionAskAboutPreferences(Action):
    def name(self) -> Text:
        return "action_ask_about_preferences"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_default_response("action_ask_about_preferences"))
        return []


class ActionAskAboutEvents(Action):
    def name(self) -> Text:
        return "action_ask_about_events"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_default_response("action_ask_about_events"))
        return []


class ActionAskAboutScienceContent(Action):
    def name(self) -> Text:
        return "action_ask_about_science_content"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_default_response("action_ask_about_science_content"))
        return []


class ActionAskAboutRobloxContent(Action):
    def name(self) -> Text:
        return "action_ask_about_roblox_content"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_default_response("action_ask_about_roblox_content"))
        return []


class ActionAskAboutPartTime(Action):
    def name(self) -> Text:
        return "action_ask_about_part_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_default_response("action_ask_about_part_time"))
        return []


class ActionAskAboutPrice(Action):
    def name(self) -> Text:
        return "action_ask_about_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_default_response("action_ask_about_price"))
        return []


class ActionAskAboutDiscounts(Action):
    def name(self) -> Text:
        return "action_ask_about_discounts"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_default_response("action_ask_about_discounts"))
        return []


class ActionAskAboutHours(Action):
    def name(self) -> Text:
        return "action_ask_about_hours"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=get_default_response("action_ask_about_hours"))
        return []





class ActionHatsune(Action):
    def name(self) -> Text:
        return "action_hatsune"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if RESPONSES.get("action_hatsune", {}).get(program):
            text = RESPONSES["action_hatsune"][program]
        else:
            text = RESPONSES.get("action_hatsune", {}).get("default", "Бот пока не знает, что ответить.")
        dispatcher.utter_message(text=text)
        return []


class ActionDude(Action):
    def name(self) -> Text:
        return "action_dude"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if RESPONSES.get("action_dude", {}).get(program):
            text = RESPONSES["action_dude"][program]
        else:
            text = RESPONSES.get("action_dude", {}).get("default", "Бот пока не знает, что ответить.")
        dispatcher.utter_message(text=text)
        return []
