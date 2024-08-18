from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    """
    Абстрактный родительский класс для подключения по API
    """

    @abstractmethod
    def load_vacancies(self, keyword):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом
    """

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 10}
        self.vacancies = []
        self.validate_vacancies = []

    def load_vacancies(self, keyword):
        """
        Функция для получения вакансий по заданному слову.
        Приводит полученный список к нужному виду.
        """
        self.params["text"] = keyword
        while self.params.get("page") != 2:
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.params)
            except Exception as e:
                print(f'Произошла ошибка {e}')
            else:
                vacancies = response.json()["items"]
                # print(vacancies)
                self.vacancies.extend(vacancies)
                self.params["page"] += 1
                # print(self.vacancies)

        for vacancy in self.vacancies:
            if vacancy['name'] is None:
                vacancy['name'] = 'Название не указано'
            if vacancy['alternate_url'] is None:
                vacancy['alternate_url'] = 'Ссылка отсутствует'
            if vacancy['salary'] is None:
                vacancy['salary'] = 'Зарплата не указана'
            else:
                vacancy['salary'] = vacancy['salary']['from']
            if vacancy['snippet'] is None or vacancy['snippet']['responsibility'] is None:
                vacancy["snippet"]["responsibility"] = 'Описание отсутствует'
            if vacancy["area"] is None or vacancy['area']['name'] is None:
                vacancy["area"]["name"] = 'Город не указан'
            self.validate_vacancies.append(vacancy)
            # print(self.validate_vacancies)
            # print(self.vacancies)

    def get_vacancies(self):
        """
        Возвращает список вакансий
        """
        # print(self.validate_vacancies)
        return self.validate_vacancies


if __name__ == "__main__":
    hh = HH()
    hh.load_vacancies('Junior Python Developer')
    hh_vacancies = hh.get_vacancies()
    print(hh_vacancies)