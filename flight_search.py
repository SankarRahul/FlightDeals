import os
import requests

IATA_URL = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:

    def __init__(self) -> None:
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_API_SECRET"]
        self._token = self._get_new_token()
    
    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url=TOKEN_URL, headers=header, data=body)

        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def get_iata_code(self, city_name):
        """
        Retrieves IATA code for specified city using Amadeus Location API.
        """

        print(f"Using this token to get destination {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }

        response = requests.get(
            url=IATA_URL,
            headers=headers,
            params=query
        )
        
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")

        try:
            code = response.json()["data"][0]['iataCode']
            
        except (ValueError, KeyError) as e:
            print(f"Error parsing API response for {city_name}: {e}")
            return "N/A"
        
        return code
    
    def check_flights(self, origin_city_code, destination_city_code, dep_date, return_date):
        """
        Searches for flight options between two cities on specified departure and return dates
        using the Amadeus API.
        Parameters:
            origin_city_code (str): The IATA code of the departure city.
            destination_city_code (str): The IATA code of the destination city.
            dep_date (datetime): The departure date.
            return_date (datetime): The return date.
        """
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": dep_date.strftime("%Y-%m-%d"),
            "returnDate": return_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "USD",
            "max": "10",
        }

        response = requests.get(
            url=FLIGHT_URL,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.")
            print("Response body:", response.text)
            return None

        return response.json()