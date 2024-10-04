import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHEETY_API_URL = os.environ["SHEETY_API_URL"]

class DataManager:
    """This class communicates with Google Sheets through Sheety API"""

    def __init__(self):
        self._sheet_data = {}
        self._headers = {"Authorization": os.environ["SHEETY_AUTH"]}

    def get_sheet_data(self):
        try:
            response = requests.get(
                url=SHEETY_API_URL,
                headers=self._headers
            )
            response.raise_for_status()
            self._sheet_data = response.json()["prices"]
            return self._sheet_data
        except requests.exceptions.RequestException as error:
            print(f"Error fetching data: {error}")
            return None

    def update_sheet_data(self, city_id, new_data):
        # PUT request to update rows with new IATA code
        sheety_put_url = f"{SHEETY_API_URL}/{city_id}"
        try:
            response = requests.put(
                url=sheety_put_url, 
                headers=self._headers,
                json={"price": new_data}
            )
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error updating data for city ID {city_id}: {error}")
            return None