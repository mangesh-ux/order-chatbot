from os import access
# from dotenv import dotenv_values
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
import csv
import re
from datetime import date
from datetime import datetime
import requests
from requests.structures import CaseInsensitiveDict

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ValidateOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_form"

    def validate_tshirt_count(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `tshirt_count` value."""

        tshirt_stock = 50
        # Check if Tshort Count is valid
        # regex = fr'\b[0-{tshirt_stock}]\b'

        if not slot_value.isdigit():
            dispatcher.utter_message(f"Could you please specify a valid quantity of T-shirts you'd like to order? 📋 Just a heads up, we currently have {tshirt_stock} T-shirts available in our stock. Let's make sure we can fulfill your request perfectly!")
            return {"tshirt_count": None}
        elif int(slot_value) > tshirt_stock:
            dispatcher.utter_message(f"Oops! It looks like we don't have {slot_value} T-shirts in our inventory at the moment. 📋 Just a heads up, we currently have {tshirt_stock} T-shirts available in our stock. Let's find a perfect match for your request within our current selection!")
            return {"tshirt_count": None}
        else:
            return {"tshirt_count": slot_value}
        

    def validate_tshirt_category(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `tshirt_category` value."""

        tshirt_categories = ['Round-Neck-Tee', 'Collared-Tee', 'Ringer-Tee']
        # Check if tshirt category is valid
        if slot_value in tshirt_categories:
            return {'tshirt_category': slot_value}
        dispatcher.utter_message(f"Could you please select a valid T-shirt category from the buttons provided? 🛍️ The available categories are {', '.join(tshirt_categories)}.")
        return {"tshirt_category": None}
    

    def validate_pants_count(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pants_count` value."""

        pants_stock = 60
        # Check if Tshort Count is valid
        # regex = fr'\b[0-{pants_stock}]\b'

        if not slot_value.isdigit():
            dispatcher.utter_message(f"Could you please specify a valid quantity of Pants you'd like to order? 📋 Just a heads up, we currently have {pants_stock} Pants available in our stock. Let's make sure we can fulfill your request perfectly!")
            return {"pants_count": None}
        elif int(slot_value) > pants_stock:
            dispatcher.utter_message(f"Oops! It looks like we don't have {slot_value} Pants in our inventory at the moment. 📋 Just a heads up, we currently have {pants_stock} Pants available in our stock. Let's find a perfect match for your request within our current selection!")
            return {"tshirt_count": None}
        else:
            return {"pants_count": slot_value}

    def validate_pants_category(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `tshirt_category` value."""

        pants_categories = ['Jeans', 'Trousers', 'Ringer-Pants']
        # Check if tshirt category is valid
        if slot_value in pants_categories:
            return {'pants_category': slot_value}
        dispatcher.utter_message(f"Could you please select a valid Pants category from the buttons provided? 🛍️ The available categories are {', '.join(pants_categories)}.")
        return {"pants_category": None}
    

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        tshirt_count = int(tracker.get_slot("tshirt_count"))
        tshirt_category = tracker.get_slot("tshirt_category")
        pants_count = int(tracker.get_slot("pants_count"))
        pants_category = tracker.get_slot("pants_category")

        tshirt_price = 399
        pants_price = 499
        
        #  Initialize total_price to 0
        total_price = 0
        items_ordered = []

        # Check for tshirt_category and calculate its price if not "None"
        if tshirt_category != "Ringer-Tee":
            total_price += tshirt_count * tshirt_price
            items_ordered.append(f"{tshirt_count} {tshirt_category} T-shirt(s)")
            
        # Check for pants_category and calculate its price if not "None"
        if pants_category != "Ringer-Pants  ":
            total_price += pants_count * pants_price
            items_ordered.append(f"{pants_count} {pants_category} pants")

        # Generate the appropriate message based on items ordered
        if tshirt_category == "Ringer-Tee" and pants_category == "Ringer-Pants":
            dispatcher.utter_message(response='utter_continue')

        items_text = " and ".join(items_ordered)
        text = f"""Congratulations! 🎉 Your order for INR {total_price} has been successfully processed. 🛍️ You've ordered {items_text}. Thank you for choosing us for your fashion needs!"""
        dispatcher.utter_message(text)

        return []