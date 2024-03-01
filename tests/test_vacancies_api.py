import pytest

from src.vacancies_api import HeadHunterAPI

hh_api = HeadHunterAPI()


def test_get_areas():
    assert hh_api.get_areas("Москва") == "1"


def test_test_vacancies_api():
    assert hh_api.get_vacancies("", False, None) != []
    assert hh_api.get_vacancies("Python, разработка", True, "1") != []
    with pytest.raises(Exception):
        hh_api.get_vacancies(0, "", "")
    with pytest.raises(AssertionError):
        hh_api.get_vacancies("ghggfhghgfhff", True, "131")
