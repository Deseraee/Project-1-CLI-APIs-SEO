# main.py - OutSafe CLI

from weather_api import get_coordinates, get_weather, get_uv, get_aqi, get_forecast
from recommender import get_recommendation


def choose_activity():
    print("\nPick activity:")
    print("1. Golf")
    print("2. Walk")
    print("3. Run")
    print("4. Bike")

    choice = input("Choice: ")

    if choice == "1":
        return "golf"
    elif choice == "2":
        return "walk"
    elif choice == "3":
        return "run"
    elif choice == "4":
        return "bike"
    else:
        return None


while True:
    print("\nWelcome to OutSafe CLI")
    print("1. Check activity safety")
    print("2. Exit")

    menu_choice = input("Choose an option: ")

    if menu_choice == "1":
        city = input("\nEnter your city: ")
        state = input("Enter your state abbreviation, like OH or GA: ")

        city = city.strip()
        state = state.strip().upper()

        if city == "" or state == "":
            print("City and state cannot be blank.")
            continue

        location = city + "," + state + ",US"
        display_location = city + ", " + state

        activity = choose_activity()

        if activity is None:
            print("Invalid activity choice.")
            continue

        print("\nGetting outdoor conditions...")

        try:
            lat, lon = get_coordinates(location)

            temp, description, humidity = get_weather(location)
            uv = get_uv(lat, lon)
            aqi = get_aqi(lat, lon)

            forecast_time, forecast_temp, forecast_description = get_forecast(location)

            verdict, reasons = get_recommendation(activity, temp, aqi, uv)

            print("\nOutSafe Report")
            print("--------------------")
            print("Location:", display_location)
            print("Activity:", activity)
            print("Current Temperature:", round(temp, 1), "°F")
            print("Current Weather:", description)
            print("Humidity:", humidity, "%")
            print("AQI:", aqi)
            print("UV Index:", round(uv, 1))
            print("Verdict:", verdict)

            print("\nReasons:")
            for reason in reasons:
                print("-", reason)

            print("\nNext Forecast:")
            print("Time:", forecast_time)
            print("Temperature:", round(forecast_temp, 1), "°F")
            print("Weather:", forecast_description)

        except Exception as error:
            print("\nSomething went wrong.")
            print("Error:", error)
            print("Try using a US city and state, like Columbus and OH.")

    elif menu_choice == "2":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")