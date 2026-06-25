from recommender import get_recommendation


def test_good_conditions():
    verdict, reasons = get_recommendation("walk", 70, 20, 1)
    assert verdict == "GOOD"


def test_caution_conditions():
    verdict, reasons = get_recommendation("golf", 88, 75, 6)
    assert verdict == "CAUTION"


def test_avoid_conditions():
    verdict, reasons = get_recommendation("run", 98, 160, 9)
    assert verdict == "AVOID"


def test_unhealthy_air_not_good():
    verdict, reasons = get_recommendation("walk", 70, 150, 1)
    assert verdict != "GOOD"