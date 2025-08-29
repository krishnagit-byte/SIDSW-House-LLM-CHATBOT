import os 
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, ValidationAction, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
import re
from groq import Groq
import json

class ValidateUserInfoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_info_form"

    def validate_user_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate user_name value."""
        
        if len(slot_value) < 2:
            dispatcher.utter_message(text="Name must be at least 2 characters long. Please provide your full name.")
            return {"user_name": None}
        
        return {"user_name": slot_value}

    def validate_user_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate user_city value."""
        
        if len(slot_value) < 2:
            dispatcher.utter_message(text="Please provide a valid city name.")
            return {"user_city": None}
        
        return {"user_city": slot_value}

    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phone_number value."""
        
        # Simple phone validation
        phone_pattern = re.compile(r'^[\d\s\-\(\)\+]{6,15}$')
        
        if not phone_pattern.match(slot_value):
            dispatcher.utter_message(text="Please provide a valid phone number (6-15 digits).")
            return {"phone_number": None}
        
        return {"phone_number": slot_value}

class ActionSaveUserInfo(Action):
    def name(self) -> Text:
        return "action_save_user_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get slot values
        user_name = tracker.get_slot("user_name")
        user_city = tracker.get_slot("user_city")
        phone_number = tracker.get_slot("phone_number")
        
        
        print(f"Saving user info:")
        print(f"Name: {user_name}")
        print(f"City: {user_city}")
        print(f"Phone: {phone_number}") 
        # database.save_user_info(username, usercity, phone number)
        
        return []

GROQ_API_KEY = "groq api key"  # Replace with your actual Groq API key

class ActionGroq(Action):
    """
    Sends a message to Groq and returns the LLM reply.
    """


    GROQ_API_KEY = "geoq api key"   

    def name(self) -> str:
        return "action_groq"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: dict,
    ):
        # 1. Grab the user utterance
        user_message = tracker.latest_message.get("text")
        if not user_message:
            dispatcher.utter_message(text="I didn't get that. Could you repeat?")
            return []

        # 2. Build request
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.GROQ_API_KEY}",
        }
        payload = {
            "model": "llama3-8b-8192",  
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 500,
            "temperature": 0.7,
            #"top_p": 1.0,
            #"frequency_penalty": 0.1,
            #"presence_penalty": 0.1
        }

        try:
            response = requests.post(url, headers=headers, json=payload)  # Timeot = 30
            response.raise_for_status()
            data = response.json()
            assistant_reply = data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't reach Groq right now.")
            print(f"[Groq Error] {e}")   # for debugging
            return []

        dispatcher.utter_message(text=assistant_reply)
        return []