import requests
import json
from abc import ABC, abstractmethod
from src.vacancies_api import HeadHunterAPI


class SaveVacancies(ABC):
    @abstractmethod
    def save_vacancies(self, *args, **kwargs):
        pass

    @abstractmethod
    def sorted_vacancies_from_json(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete_vacancies_from_json(self, *args, **kwargs):
        pass


class SaveVacanciesJson(SaveVacancies):
    def save_vacancies(self, text):
        data_vacancies = HeadHunterAPI()
        json_vacancies = data_vacancies.get_vacancies(text)
        with open('../data/vacancies_hh.json', 'w', encoding='utf-8') as file:
            json.dump(json_vacancies, file, indent=2, ensure_ascii=False) # структурированный
            # json.dump(json_vacancies, file, ensure_ascii=False) # строкой


    def sorted_vacancies_from_json(self):
        pass


    def delete_vacancies_from_json(self):
        pass
