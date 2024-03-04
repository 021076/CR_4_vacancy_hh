import pytest
import os
import os.path
from src.vacancies_data import DataVacanciesJson

data_vacancies = DataVacanciesJson()
# БД полученная с сайта hh.ru
bd_hh = [
    {
        "id": "00000001", "name": "Разаработчик Python",
        "area": {"id": "1382", "name": "Урай", "url": "https://api.hh.ru/areas/1382"},
        "salary": {"from": 35000, "to": 47000, "currency": "RUR", "gross": True},
        "url": "https://api.hh.ru/vacancies/00000001?host=hh.ru",
        "alternate_url": "https://hh.ru/vacancy/00000001",
        "snippet": {"requirement": "Желание работать", "responsibility": "Разработка приложений"},
        "schedule": {"id": "fullDay", "name": "Полный день"}
    }]


def test_save_vacancies():
    # сохранение данных в файл
    data_vacancies.save_vacancies(bd_hh)
    # проверка, что файл существует
    assert os.path.exists(DataVacanciesJson.json_file)


def test_read_from_json():
    # подготовка к проверке: удаление файла
    os.remove(DataVacanciesJson.json_file)
    # проверка исключения FileNotFoundError
    with pytest.raises(FileNotFoundError):
        DataVacanciesJson.read_from_json(data_vacancies)
    # подготовка к проверке: сохранение данных в файл
    data_vacancies.save_vacancies(bd_hh)
    # чтение из файла
    bd_json = DataVacanciesJson.read_from_json(data_vacancies)
    for j in bd_json:
        # проверка, что файл не пустой и вычитан
        assert os.stat("../data/vacancies_hh.json").st_size > 0
        assert j["id"] == "00000001"
        assert j["area"]["name"] == "Урай"


def test_selection_vacancies():
    # подготовка к проверке: сохранение данных в файл
    data_vacancies.save_vacancies(bd_hh)
    # чтение из файла
    bd_json = DataVacanciesJson.read_from_json(data_vacancies)
    # выборка данных, вычитанных из фала  json
    bd_select = data_vacancies.selection_vacancies(bd_json)
    for s in bd_select:
        # проверка, что данные собрались в нужную структуру
        assert s["name"] == "Разаработчик Python"
        assert s["area"] == "Урай"
        assert s["salary"] == {'from': 35000, 'to': 47000, 'currency': 'RUR', 'gross': True}
        assert s["snippet_req"] == "Желание работать"
        assert s["schedule"] == "Полный день"
        assert s["url"] == "https://api.hh.ru/vacancies/00000001?host=hh.ru"


def test_delete_vacancies():
    # подготовка к проверке: удаление файла
    os.remove(DataVacanciesJson.json_file)
    # проверка исключения FileNotFoundError
    with pytest.raises(FileNotFoundError):
        DataVacanciesJson.delete_vacancies(data_vacancies)
    # подготовка к проверке: сохранение данных в файл
    data_vacancies.save_vacancies(bd_hh)
    # очищение файла
    DataVacanciesJson.delete_vacancies(data_vacancies)
    # проверка, что файл пустой
    assert os.stat(DataVacanciesJson.json_file).st_size == 0
