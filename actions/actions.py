#actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionAskAboutDates(Action):
    def name(self) -> Text:
        return "action_ask_about_dates"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if program == "Мир наук и электроники":
            message = "Смена 'Мир наук и электроники' проводится с 23 июня по 6 июля 2025 года."
        elif program == "Создание 3D-миров в Roblox":
            message = "Смена 'Создание 3D-миров в Roblox' проводится с 7 по 20 июля 2025 года."
        else:
            message = "Пожалуйста, уточните, о какой смене вы спрашиваете."
        dispatcher.utter_message(text=message)
        return []


class ActionAskAboutFood(Action):
    def name(self) -> Text:
        return "action_ask_about_food"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=(
            "Во время пребывания организовано 3-разовое питание: второй завтрак, обед и полдник.\n"
            "Все порции в индивидуальной упаковке.\n"
            "Питание организовано по договору с 'Смарт': http://eda-smart.ru/"
        ))
        return []


class ActionAskAboutPreferences(Action):
    def name(self) -> Text:
        return "action_ask_about_preferences"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=(
            "Меню учитывает предпочтения детей: 'основа', 'без глютена', 'без лактозы', 'аллергик',\n"
            "'вегетарианец', 'не ем рыбу', 'не хочу курицу'.\n"
            "Дети выбирают блюда заранее."
        ))
        return []


class ActionAskAboutEvents(Action):
    def name(self) -> Text:
        return "action_ask_about_events"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Да, проводятся выездные мероприятия 1 раз в неделю с 13:30 до 18:00 по тематике смены.")
        return []


class ActionAskAboutTheme(Action):
    def name(self) -> Text:
        return "action_ask_about_theme"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        program = tracker.get_slot("selected_program")
        if program == "Мир наук и электроники":
            message = "Смена посвящена путешествию по миру наук: химия, физика, география, геология, биология."
        elif program == "Создание 3D-миров в Roblox":
            message = "Смена посвящена развитию пространственного мышления, изучению Blender и RobloxStudio."
        else:
            message = "Пожалуйста, уточните, о какой смене вы спрашиваете."
        dispatcher.utter_message(text=message)
        return []


class ActionAskAboutScienceContent(Action):
    def name(self) -> Text:
        return "action_ask_about_science_content"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=(
            "Смена 'Мир наук и электроники' включает: химические опыты, физические эксперименты,\n"
            "археологические раскопки, ботанические наблюдения, создание собственного электронного робота."
        ))
        return []


class ActionAskAboutRobloxContent(Action):
    def name(self) -> Text:
        return "action_ask_about_roblox_content"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=(
            "Включены занятия: технический английский, интенсив по 2D/3D, моделирование и программирование игр в Roblox."
        ))
        return []


class ActionAskAboutPartTime(Action):
    def name(self) -> Text:
        return "action_ask_about_part_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=(
            "Можно выбрать отдельные курсы: английский — 7200 руб.,\n"
            "математика — 8700 руб., программирование — 11 600 руб."
        ))
        return []


class ActionAskAboutPrice(Action):
    def name(self) -> Text:
        return "action_ask_about_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=(
            "Полная стоимость смены — 24 000 руб.\n"
            "До 12 мая 2025 действует скидка 10% — цена по акции: 21 600 руб."
        ))
        return []


class ActionAskAboutDiscounts(Action):
    def name(self) -> Text:
        return "action_ask_about_discounts"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=(
            "Скидка 10% до 12 мая 2025:\n"
            "- Английский — 6480 руб.\n"
            "- Математика — 7830 руб.\n"
            "- Программирование — 10 440 руб."
        ))
        return []


class ActionAskAboutHours(Action):
    def name(self) -> Text:
        return "action_ask_about_hours"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=(
            "⏰ Время пребывания детей — с 8:30 до 18:00. Можно выбрать полный день или только отдельные курсы.\n"
            "Подробнее: https://www.nextstep66.ru/course/gorodskoj-klub-letnij-drajv-2/"
        ))
        return []
