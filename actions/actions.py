from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction
from rasa_sdk.types import DomainDict
import requests

class Action_Otions1(Action):

    def name(self) -> Text:
        return "action_options1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_intent_of_latest_message() == "our_services":
            dispatcher.utter_message(response="utter_our_services")

        elif tracker.get_intent_of_latest_message() == "demo":
            return [FollowupAction("detail_form")]
        
        elif tracker.get_intent_of_latest_message() == "solution":
            dispatcher.utter_message(response="utter_solution")

        elif tracker.get_intent_of_latest_message() == "about_us":
            dispatcher.utter_message(response="utter_about_us")

        elif tracker.get_intent_of_latest_message() == "exit":
            dispatcher.utter_message(text="Thank you have a good day!")
        


        return []
    

class Action_Otions2(Action):

    def name(self) -> Text:
        return "action_options2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_intent_of_latest_message() == "banking":
            dispatcher.utter_message(response="utter_banking")
        
        if tracker.get_intent_of_latest_message() == "voice":
            dispatcher.utter_message(response="utter_voice")

        elif tracker.get_intent_of_latest_message() == "messaging":
            dispatcher.utter_message(response="utter_messaging")

        elif tracker.get_intent_of_latest_message() == "contact_center":
            dispatcher.utter_message(response="utter_contact_center")

        elif tracker.get_intent_of_latest_message() == "exit":
            dispatcher.utter_message(text="Thank you have a good day!")
  
        return []
    
    
class Action_Otions3(Action):

    def name(self) -> Text:
        return "action_options3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_intent_of_latest_message() == "chatbot":
            dispatcher.utter_message(response="utter_chatbot")
        
        if tracker.get_intent_of_latest_message() == "inbound":
            dispatcher.utter_message(response="utter_inbound")

        elif tracker.get_intent_of_latest_message() == "outbound":
            dispatcher.utter_message(response="utter_outbound")

        elif tracker.get_intent_of_latest_message() == "reporting":
            dispatcher.utter_message(response="utter_reporting")

        elif tracker.get_intent_of_latest_message() == "exit":
            dispatcher.utter_message(text="Thank you have a good day!")
  
        return []


class ValidateDetail_form(FormValidationAction):
    def name(self) -> Text:
        return "validate_detail_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print("validate_name")

        last_text = tracker.latest_message["text"]
        if len(last_text) < 5:
            return {"name": None}
        else:
            return {"name": last_text}



class ActionUtterTalkLLm(Action):

    def name(self) -> Text:
        return "action_utter_talkllm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_text = tracker.latest_message.get("text")
        
        last_text = last_text.split("123_")[1]
        print(last_text)
        url = f'http://58.65.231.164:5000/llama3?text={last_text}'
        
        response = requests.post(url)
        genText = response.json()["genText"]
        bot_response = genText
        print(bot_response)

        dispatcher.utter_message(text = bot_response)
        
        # dispatcher.utter_message(text="Hi there, this is Disha with LLM power. How can I help you?")

        return []

class ActionValidateTalkToLLm(FormValidationAction):
    """validate_end_llm"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "validate_talk_to_llm_form"

    
    async def validate_end_llm(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        print("validate_end_llm")
    
        endLLm = tracker.get_slot('end_llm')
        last_text = tracker.latest_message.get("text")
        
        # print("********** ", endLLm)
        
        if last_text == "end_llm":
            #dispatcher.utter_message(text = "Thank you for using out LLM")
            dispatcher.utter_message(text = "LLM not available")
            return {"end_llm": endLLm, "requested_slot": None}
        else:
            url = f'http://58.65.231.164:5000/llama3?text={last_text}'
            ### LLM ##########
            # url = f'http://192.168.10.97:5000/llama3?text={last_text}'
            response = requests.post(url)
            genText = response.json()["genText"]
            bot_response = genText
            print(bot_response)
        
            dispatcher.utter_message(text = bot_response)
            return {"end_llm": None, "requested_slot": "end_llm"}