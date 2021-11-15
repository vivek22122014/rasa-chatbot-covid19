
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


class Actioncoronastats(Action):

    def name(self) -> Text:
        return "actions_corona_state_stat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        responses = requests.get("https://api.covid19india.org/data.json").json()

        entities = tracker.latest_message['entities']
        print("Now Showing Data For:", entities)
        state = None

        for i in entities:
            if i["entity"] == "state":
                state = i["value"]

        message = "Please Enter Correct State Name !"

        if state == "india":
            state = "Total"
        for data in responses["statewise"]:
            if data["state"] == state.title():
                print(data)
                message = "Now Showing Cases For --> " + state.title() + " Since Last 24 Hours : "+ "\n" + "Active: " + data[
                    "active"] + " \n" + "Confirmed: " + data["confirmed"] + " \n" + "Recovered: " + data[
                              "recovered"] + " \n" + "Deaths: " + data["deaths"] + " \n" + "As Per Data On: " + data[
                              "lastupdatedtime"]

        print(message)
        dispatcher.utter_message(message)

        return []

class ActionCoronaPincode(Action):

    def name(self)-> Text:
        return "action_corona_pincode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']
        
        pincode = 0
        
        for i in entities:
            if i['entity'] == 'pincode':
                pincode = int(i['value'])
        
        try:
            #postal pincode validation check
            response = requests.get("https://api.postalpincode.in/pincode/{}".format(pincode)).json()

            data = requests.get('https://api.covid19india.org/state_district_wise.json').json()

            for i in response:
                for dis in i['PostOffice']:
                    district = dis['District']
            message = []
            for key, value in data.items():
                for d, s in value.items():
                    for k in s:
                        if district == k:
                            message +="Current covid-19 caseas --> {}".format(district),"\n", "Confirmed cases: ", s[k]['delta']['confirmed'], "\n","Deaths: ", s[k]['delta']['deceased'], "\n","Recovered cases:", s[k]['delta']['recovered'], "\n", "Total cases till now:", "\n", "active cases: ", s[k]['active'], "\n", "confirmed cases: ", s[k]['confirmed'], "\n", "deaths: ", s[k]['deceased'], "\n", "recovered: ", s[k]['recovered']

            output = ''
            for i in message:
                output += str(i)

            print(output)
            dispatcher.utter_message(output)

        except:
            print('actions is down')
            dispatcher.utter_message(text="error in api calling")
        
        return []

