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


class ActionTestmessage(Action):
    def name(self) -> Text:
        return "action_testmessage"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if RESPONSES.get("action_testmessage", {}).get(program):
            text = RESPONSES["action_testmessage"][program]
        else:
            text = RESPONSES.get("action_testmessage", {}).get("default", "Бот пока не знает, что ответить.")
        dispatcher.utter_message(text=text)
        return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionBankai(Action):
    def name(self) -> Text:
        return "action_bankai"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if RESPONSES.get("action_bankai", {}).get(program):
            text = RESPONSES["action_bankai"][program]
        else:
            text = RESPONSES.get("action_bankai", {}).get("default", "Бот пока не знает, что ответить.")
        dispatcher.utter_message(text=text)
        return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionA(Action):
    def name(self) -> Text:
        return "action_a"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if RESPONSES.get("action_a", {}).get(program):
            text = RESPONSES["action_a"][program]
        else:
            text = RESPONSES.get("action_a", {}).get("default", "Бот пока не знает, что ответить.")
        dispatcher.utter_message(text=text)
        return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionPedagogi1(Action):
    def name(self) -> Text:
        return "action_Pedagogi_1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if RESPONSES.get("action_Pedagogi_1", {}).get(program):
            text = RESPONSES["action_Pedagogi_1"][program]
        else:
            text = RESPONSES.get("action_Pedagogi_1", {}).get("default", "Бот пока не знает, что ответить.")
        dispatcher.utter_message(text=text)
        return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionTestGpt(Action):
    def name(self) -> Text:
        return "action_test_gpt"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if RESPONSES.get("action_test_gpt", {}).get(program):
            text = RESPONSES["action_test_gpt"][program]
        else:
            text = RESPONSES.get("action_test_gpt", {}).get("default", "Бот пока не знает, что ответить.")
        dispatcher.utter_message(text=text)
        return []
