import json

import requests
from abc import ABC, abstractmethod


class VacanciesAPI(ABC):
    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass


class HeadHunterAPI(VacanciesAPI):
    def get_vacancies(self, text):
        self.params = {"text": text}
        response = requests.get("https://api.hh.ru/vacancies/", self.params)
        try:
            if response.status_code != 200:
                raise Exception(f'Ошибка код {response.status_code}: {response.json()}')
        except Exception:
            raise
        else:
            if response.json()["items"] == []:
                return f'Вакансии не найдены'
            else:
                # return json.dumps(response.json()["items"], indent=2, ensure_ascii=False)
                return response.json()["items"]
