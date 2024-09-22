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

#   https://github.com/jaimeteb/tutoriales-rasa-es/blob/master/02_pokebot/actions.py


from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset, Restarted
from rasa_sdk.executor import CollectingDispatcher

from typing import Any, Text, Dict, List, Union, Optional

import requests

def fetch_wikidata_nombre(nombre_autor):
    url = 'https://query.wikidata.org/sparql'
    try:
        
        query = '''
                SELECT * WHERE {{
                    ?resource rdfs:label ?label .
                    ?resource wdt:P31 wd:Q5 .
                    OPTIONAL {{?resource wdt:P18 ?imagen }}.
                    ?resource wdt:P135 wd:Q530936 .
                    FILTER(LANGMATCHES(LANG(?label), "es")) .
                    FILTER(REGEX(?label, "{nombre}", "i" ))   
               }}
               LIMIT 1
               '''
        print(query)
        r = requests.get(url, params = {'format': 'json', 'query': query.format(nombre=nombre_autor)})

        if r.status_code == 404:
            dispatcher.utter_message(template="utter_autor_no_encontrado")
            return [AllSlotsReset()]

        return r.json()
    except:
        return 'There was and error'

def fetch_wikidata_id(id_autor):
    url = 'https://query.wikidata.org/sparql'
    try:
        
        query = '''
                SELECT * WHERE {{
                    VALUES ?resource {{ wd:{id} }}
                    ?resource rdfs:label ?label .
                    OPTIONAL {{?resource wdt:P18 ?imagen }}.
                    ?resource wdt:P31 wd:Q5 .
                    ?resource wdt:P135 wd:Q530936 .
                    FILTER(LANGMATCHES(LANG(?label), "es")) .
               }}
               LIMIT 1
               '''
        print(query)
        r = requests.get(url, params = {'format': 'json', 'query': query.format(id=id_autor)})

        if r.status_code == 404:
            dispatcher.utter_message(template="utter_autor_no_encontrado")
            return [AllSlotsReset()]

        return r.json()
    except:
        return 'There was and error'


class ActionSearchAuthorWikidata(Action):

     def name(self) -> Text:
         return "action_buscar_autor"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # What text to search for
        #query = tracker.latest_message['text']

        nombre_autor = tracker.get_slot("nombre_autor")
        id_autor = tracker.get_slot("id_autor")

        data = ''
        if nombre_autor and not id_autor:
            # Fetch API
            data = fetch_wikidata_nombre(nombre_autor)
        elif id_autor and not nombre_autor:
            # Fetch API
            data = fetch_wikidata_id(id_autor)

        #show response as JSON
        print(data)

        #dispatcher.utter_message(text="Hello World!")

        dispatcher.utter_message(text="He encontrado estos autores del Siglo de Oro:")
        matches = data['results']['bindings']
        
        for a in matches:
            #dispatcher.utter_message(text=f"- {a['label']['value']} - {a['resource']['value']}")
           
            info_id_autor = str(a['resource']['value'])
            info_nombre_autor = a['label']['value']
            info_imagen_autor = a['imagen']['value']
            
            if info_imagen_autor:
                print(info_imagen_autor)
                dispatcher.utter_message(
                    response="utter_info_autor",
                    id=info_id_autor,
                    nombre=info_nombre_autor,
                    imagen=info_imagen_autor
                )
            else:
                dispatcher.utter_message(
                    response="utter_info_autor_sin_imagen",
                    id=info_id_autor,
                    nombre=info_nombre_autor
                )

        return [AllSlotsReset()]
