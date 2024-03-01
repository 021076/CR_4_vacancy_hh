import json

import requests
from abc import ABC, abstractmethod


class VacanciesAPI(ABC):
    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass


class HeadHunterAPI(VacanciesAPI):

    def get_areas(self, find_area):
        """ Получение базы регионов и создание справочника регионов формата 'name:id'"""
        area_respose = requests.get("https://api.hh.ru/areas/")
        hh_areas = area_respose.json()
        areas_list = []
        for area_level_1 in hh_areas:
            dict_area_level_1 = {area_level_1["name"]: area_level_1["id"]}
            areas_list.append(dict_area_level_1)
            if area_level_1["areas"] != []:
                areas_1 = area_level_1["areas"]
                for area_level_2 in areas_1:
                    dict_area_level_2 = {area_level_2["name"]: area_level_2["id"]}
                    areas_list.append(dict_area_level_2)
                    if area_level_2["areas"] != []:
                        areas_2 = area_level_2["areas"]
                        for area_level_3 in areas_2:
                            dict_area_level_3 = {area_level_3["name"]: area_level_3["id"]}
                            areas_list.append(dict_area_level_3)

        for df in areas_list:
            for k, v in df.items():
                if k == find_area:
                    return (v)
                elif k == None:
                    return ("")

    def get_vacancies(self, text, with_salary_param, area_id):
        """ Получение базы вакансий по параметрам
            text - параметр берется из данных полученных от пользователя
            area_id - параметр берется из сформированного справочника регионов по значению полученному от пользователя,
                        если код не определен, поиск выполняется по всем регионам
            with_salary_param (True, False) - параметр берется в зависимости от данных полученных от пользователя
        """
        self.params = {"text": text, "area": area_id, "page": 0, "per_page": 50, "only_with_salary": with_salary_param}
        hh_response = requests.get("https://api.hh.ru/vacancies/", self.params)
        try:
            if hh_response.status_code != 200:
                raise Exception(f'Ошибка {hh_response.status_code}: {hh_response.json()}')
        except Exception:
            raise
        else:
            try:
                if hh_response.json()["items"] == []:
                    raise AssertionError(f'Вакансии не найдены')
            except Exception:
                raise
            else:
                # return json.dumps(hh_response.json()["items"], indent=2, ensure_ascii=False)
                return hh_response.json()["items"]
