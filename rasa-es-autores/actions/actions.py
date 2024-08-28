# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
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

import requests

def fetch_wikidata():
    url = 'https://query.wikidata.org/sparql'
    try:
        
        query = '''
                SELECT * WHERE {{
                    ?resource rdfs:label ?label .
                    ?resource wdt:P31 wd:Q5 .
                    ?resource wdt:P135 wd:Q530936 .
                    FILTER(LANGMATCHES(LANG(?label), "es"))
               }}
               LIMIT 5
               '''
        print(query)
        r = requests.get(url, params = {'format': 'json', 'query': query})

        return r.json()
    except:
        return 'There was and error'


class ActionSearchAuthorWikidata(Action):

     def name(self) -> Text:
         return "action_sugerir_autor"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # What text to search for
        query = tracker.latest_message['text']

	# Fetch API
        data = fetch_wikidata()
	 
        #show response as JSON
        print(data)

        #dispatcher.utter_message(text="Hello World!")

        dispatcher.utter_message(text="He encontrado estos autores del Siglo de Oro:")
        matches = data['results']['bindings']
        print(matches)
        for a in matches[:5]:
            dispatcher.utter_message(text=f"- {a['label']['value']} - {a['resource']['value']}")

        return []
