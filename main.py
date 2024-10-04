import time
from datetime import datetime,timedelta
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
from pprint import pprint

def main():
    flight_search = FlightSearch()
    data_manager = DataManager()
    notification_manager = NotificationManager()
    ORIGIN_CITY_IATA = "AUS"

    # Get initial sheet data
    sheet_data = data_manager.get_sheet_data()

    if sheet_data is None:
        print("Failed to fetch sheet data.")
        return

    # Update empty "iataCode"
    for row in sheet_data:
        if row["iataCode"] == "":
            row["iataCode"] = flight_search.get_iata_code(row["city"])

            # Avoid API rate limit
            time.sleep(2)

            new_row = {
                "city": row["city"],
                "iataCode": row["iataCode"],
                "lowestPrice": row["lowestPrice"]
            }
            data_manager.update_sheet_data(row["id"], new_row)
    pprint(sheet_data)

    tomorrow = datetime.now() + timedelta(days=1)
    six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

    for destination in sheet_data:
        print(f"Getting flights for {destination['city']}...")
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            dep_date=tomorrow,
            return_date=six_month_from_today
        )
        cheapest_flight = find_cheapest_flight(flights)
        print(f"{destination['city']}: ${cheapest_flight.price}")

        notification_manager = NotificationManager()

        if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
            print(f"Lower price flight found to {destination['city']}!")
            notification_manager.send_email(
                message_body=f"Low price alert! Only ${cheapest_flight.price} to fly "
                            f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                            f"on {cheapest_flight.dep_date} to {cheapest_flight.return_date}."
            )
        # Avoid API rate limit
        time.sleep(2)
    

if __name__ == "__main__":
    main()
