from recommender import check_state_input, get_sunscreen_reapply_count, get_golf_recommendation, find_better_tee_window


def test_good_conditions():
    verdict, reasons, score = get_golf_recommendation(70, 20, 1, "9 holes", "cart", "clear sky")
    assert verdict == "GOOD TO PLAY"


def test_caution_conditions():
    verdict, reasons, score = get_golf_recommendation(88, 75, 6, "18 holes", "cart", "clear sky")
    assert verdict == "PLAY WITH CAUTION"


def test_avoid_conditions():
    verdict, reasons, score = get_golf_recommendation(98, 160, 9, "18 holes", "walking", "clear sky")
    assert verdict == "AVOID OR RESCHEDULE"


def test_storm_is_avoid():
    verdict, reasons, score = get_golf_recommendation(70, 20, 1, "9 holes", "cart", "thunderstorm")
    assert verdict == "AVOID OR RESCHEDULE"


def test_state_input():
    assert check_state_input("OH") == True
    assert check_state_input("Ohio") == False


def test_sunscreen_count():
    assert get_sunscreen_reapply_count("18 holes", 8) == 2


def test_better_tee_window_ignores_2am():
    forecasts = [
        {
            "time": "2026-06-26 2:00 AM",
            "hour": 2,
            "temp": 70,
            "description": "clear sky"
        },
        {
            "time": "2026-06-26 6:00 PM",
            "hour": 18,
            "temp": 76,
            "description": "clear sky"
        }
    ]

    better_time = find_better_tee_window(forecasts, "18 holes", "walking", 10, 60, 8)

    assert better_time["hour"] == 18