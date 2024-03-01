from src.vacancies import VacanciesHH

select_vacancies = [
    {'name': 'Разаработчик Python', 'salary': {'from': 35000, 'to': 47000, 'currency': 'RUR', 'gross': True},
     'area': 'Урай', 'snippet_req': 'Желание работать', 'schedule': 'Полный день',
     'url': 'https://api.hh.ru/vacancies/00000001?host=hh.ru'}]

norus_vacancies = [
    {'name': 'Разаработчик Python', 'salary': {'from': 1500, 'to': 3000, 'currency': 'EUR', 'gross': True},
     'area': 'Урай', 'snippet_req': 'Желание работать', 'schedule': 'Полный день',
     'url': 'https://api.hh.ru/vacancies/00000001?host=hh.ru'}]

salary_vacancies = [
    {'name': 'Разаработчик Python', 'salary': {'from': None, 'to': 140000, 'currency': 'RUR', 'gross': True},
     'area': 'Урай', 'snippet_req': 'Желание работать', 'schedule': 'Полный день',
     'url': 'https://api.hh.ru/vacancies/00000001?host=hh.ru'},
    {'name': 'Разаработчик Java', 'salary': {'from': 150, 'to': None, 'currency': 'EUR', 'gross': True},
     'area': 'Урай', 'snippet_req': 'Желание работать', 'schedule': 'Полный день',
     'url': 'https://api.hh.ru/vacancies/00000002?host=hh.ru'}]


def test_init_from_jsonfile():
    # Проверка создания объекта класса VacanciesHH из данных, полученных из ДБ
    VacanciesHH.init_from_jsonfile(select_vacancies)
    assert len(VacanciesHH.all) == 1


def test_currency_rate():
    # Проверка перерасчета валюты на рубли
    assert VacanciesHH.currency_rate(1000, "EUR") == 62570
    assert VacanciesHH.currency_rate(1000, "RUR") == 1000


def test_conversion_norus_salary():
    # Проверка перерасчета зарплаты в валюте на рубли в объекте класса VacanciesHH
    VacanciesHH.init_from_jsonfile(norus_vacancies)
    for v in VacanciesHH.all:
        VacanciesHH.conversion_norus_salary(v)
        assert v.salary["from"] == 93855
        assert v.salary["to"] == 187711
        assert v.salary["currency"] == "RUR"


def test_str():
    # Проверка метода sts вывода данных о вакансиях пользователю в консоль
    VacanciesHH.init_from_jsonfile(salary_vacancies)
    assert VacanciesHH.all[0].__str__() == (
        f'Название вакансии: Разаработчик Python, город: Урай, режим работы: Полный день,\n'
        f'требования: Желание работать,\n'
        f'cсылка на вакансию: https://api.hh.ru/vacancies/00000001?host=hh.ru\n'
        f'зарплата: до 140000 RUR\n'
        f'------------------------------')


def test_repr():
    # Проверка метода repr вывод отладочной информации в консоль
    VacanciesHH.init_from_jsonfile(salary_vacancies)
    assert VacanciesHH.all[
               1].__repr__() == "VacanciesHH: Разаработчик Java, https://api.hh.ru/vacancies/00000002?host=hh.ru"


def test_uniform_salary():
    # Проверка нормализации данных по зарплате, есkи from или to None
    VacanciesHH.init_from_jsonfile(salary_vacancies)
    for vac in VacanciesHH.all:
        VacanciesHH.uniform_salary(vac)
    assert VacanciesHH.all[0].salary["from"] == 140000
    assert VacanciesHH.all[0].salary["to"] == 140000
    assert VacanciesHH.all[1].salary["from"] == 150
    assert VacanciesHH.all[1].salary["to"] == 150
