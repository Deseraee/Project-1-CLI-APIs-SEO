from recommender import get_recommendation, check_state_input, check_time


def test_good_conditions():
    verdict, reasons = get_recommendation("golf", 70, 20, 1, 2, "y")
    assert verdict == "GOOD"


def test_caution_conditions():
    verdict, reasons = get_recommendation("golf", 88, 75, 6, 3, "n")
    assert verdict == "CAUTION"


def test_avoid_conditions():
    verdict, reasons = get_recommendation("golf", 98, 160, 9, 6, "n")
    assert verdict == "AVOID"


def test_unhealthy_air_not_good():
    verdict, reasons = get_recommendation("golf", 70, 150, 1, 1, "y")
    assert verdict != "GOOD"

def test_state():
  assert check_state_input("Ohio") == False
  assert check_state_input("O") == False
  assert check_state_input("OH") == True

def test_time():
  assert check_time("2026-6-24 23:00:00") == True
  assert check_time("2026-6-25 02:00:00") == False