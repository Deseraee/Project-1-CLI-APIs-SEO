# main.py - basic CLI skeleton for OutSafe

from recommender import get_recommendation

while True:
    print("\nWelcome to OutSafe CLI")
    print("1. Check activity safety")
    print("2. Exit")

    menu_choice = input("Choose an option: ")

    if menu_choice == "1":
        print("\nPick activity:")
        print("1. Golf")
        print("2. Walk")
        print("3. Run")
        print("4. Bike")

        activity_choice = input("Choice: ")

        if activity_choice == "1":
            activity = "golf"
        elif activity_choice == "2":
            activity = "walk"
        elif activity_choice == "3":
            activity = "run"
        elif activity_choice == "4":
            activity = "bike"
        else:
            print("Invalid activity choice.")
            continue

        # Fake data for now. APIs will replace these numbers later.
        temp = 88
        aqi = 75
        uv = 8

        verdict, reasons = get_recommendation(activity, temp, aqi, uv)

        print("\nOutSafe Report")
        print("Activity:", activity)
        print("Temperature:", temp, "°F")
        print("AQI:", aqi)
        print("UV Index:", uv)
        print("Verdict:", verdict)

        print("\nReasons:")
        for reason in reasons:
            print("-", reason)

    elif menu_choice == "2":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")