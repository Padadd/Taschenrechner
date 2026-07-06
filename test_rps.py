import pytest
from Main import Calculator


def test_rps_tie():
    assert Calculator.get_rps_result("Schere", "Schere") == "Unentschieden"
    assert Calculator.get_rps_result("Stein", "Stein") == "Unentschieden"
    assert Calculator.get_rps_result("Papier", "Papier") == "Unentschieden"


def test_rps_player_wins():
    assert Calculator.get_rps_result("Schere", "Papier") == "Du gewinnst!"
    assert Calculator.get_rps_result("Stein", "Schere") == "Du gewinnst!"
    assert Calculator.get_rps_result("Papier", "Stein") == "Du gewinnst!"


def test_rps_cpu_wins():
    assert Calculator.get_rps_result("Papier", "Schere") == "Der Gegner gewinnt."
    assert Calculator.get_rps_result("Schere", "Stein") == "Der Gegner gewinnt."
    assert Calculator.get_rps_result("Stein", "Papier") == "Der Gegner gewinnt."
