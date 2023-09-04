"""Создайте класс студента.
Используя дескрипторы проверяйте ФИО на первую заглавную букву и наличие только букв.
Названия предметов должны загружаться из файла CSV при создании экземпляра. Другие предметы в экземпляре недопустимы.
Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100).
Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов вместе взятых."""

import csv
from statistics import mean


class ValidName:
    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):

        for n in value.split():
            if not n.isalpha():
                raise ValueError(f"Значение '{n}' должно содержать только буквы")
            elif not n.istitle():
                raise ValueError(f"Значение '{n}' должно начинаться с заглавной буквы")
            self.value = value

        setattr(instance, self.param_name, value)


class Student:
    name = ValidName()

    def __init__(self, name, subject_csv_file):
        self.name = name
        self._subjects = self._load_subjects(subject_csv_file)
        self.ratings = {}
        self.test_results = {}

    @staticmethod
    def _load_subjects(subject_csv_file):
        subject_name = []
        with open(subject_csv_file, 'r', encoding='utf8') as file:
            for line in csv.reader(file):
                subject_name.append(*line)
            return subject_name

    @property
    def subjects(self):
        return self._subjects

    @subjects.setter
    def subjects(self, value):
        raise AttributeError(f'Невозможно изменить список предметов')

    def add_rating(self, subject, rating):
        if subject not in self._subjects:
            raise AttributeError(f'Предмет {subject} отсутствует у студента {self.name}')
        if isinstance(rating, int) and 2 <= rating <= 5:
            self.ratings.setdefault(subject, [])
            self.ratings[subject].append(rating)

        else:
            raise AttributeError(f'Неверный формат оценки {rating} ')

    def add_test_result(self, subject, result):
        if subject not in self._subjects:
            raise AttributeError(f'Предмет {subject} отсутствует у студента {self.name}')
        if isinstance(result, int) and 0 <= result <= 100:
            self.test_results.setdefault(subject, [])
            self.test_results[subject].append(result)

        else:
            raise AttributeError(f'Неверный формат результата тестов {result} ')

    def get_average_ratings(self):
        all_ratings = []
        for key, value in self.ratings.items():
            all_ratings.extend(value)
        print(f"Средний бал студента по оценкам всех предметов вместе взятых {mean(all_ratings)}")

    def get_average_score_test_results(self, subject):
        if subject not in self._subjects:
            raise AttributeError(f'Предмет {subject} отсутствует у студента {self.name}')
        if subject in self.test_results:
            print(f"Средний бал студента по тестам предмета {subject} {mean(self.test_results[subject])}")
        else:
            raise AttributeError(f'По предмету {subject} балы не начислялись')


student1 = Student("Иванов Иван Иванович", "subjects.csv")

print(student1.name)
print(student1.subjects)
student1.add_rating("Физика", 5)
student1.add_rating("Физика", 3)
student1.add_rating("Физика", 2)
student1.add_rating("Русский", 5)
student1.add_test_result("Русский", 50)
student1.add_test_result("Русский", 60)
student1.add_test_result("Физика", 50)
student1.add_test_result("Физика", 30)
student1.add_test_result("Физика", 20)
print(student1.ratings)
print(student1.test_results)
student1.get_average_score_test_results('Русский')
student1.get_average_ratings()
