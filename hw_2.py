"""Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных, обработки вложенных структур и сериализации.
 Система должна обрабатывать данные в формате JSON.

Задачи:
Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic, валидирует данные,
 и в случае успеха сериализует объект обратно в JSON и возвращает его.
Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
Написать несколько примеров JSON строк для проверки различных сценариев валидации: успешные регистрации и случаи,
 когда валидация не проходит (например возраст не соответствует статусу занятости).

Модели:
Address: Должен содержать следующие поля:
    city: строка, минимум 2 символа.
    street: строка, минимум 3 символа.
    house_number: число, должно быть положительным.

User: Должен содержать следующие поля:
    name: строка, должна быть только из букв, минимум 2 символа.
    age: число, должно быть между 0 и 120.
    email: строка, должна соответствовать формату email.
    is_employed: булево значение, статус занятости пользователя.
    address: вложенная модель адреса.

Валидация:
Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65 лет.

"""
from pydantic import BaseModel, Field, field_validator, EmailStr, model_validator


json_input_1 = {
    "name": "John Doe",
    "age": 25 ,
    "email": "john.doe@example.com",
    "is_employed": True,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}

json_input_2 = {
    "name": "Olaf Scholz",
    "age": 67,
    "email": "olaf.scholz@example.com",
    "is_employed": False,
    "address": {
        "city": "Berlin",
        "street": "Hauptbahnhof 1",
        "house_number": 0
    }
}

json_input_3 = {
    "name": "Paul Abend",
    "age": 13,
    "email": "pauli.example.com",
    "is_employed": True,
    "address": {
        "city": "Leipzig",
        "street": "Czermaks Garten 6",
        "house_number": 14
    }
}

json_input_4 = {
    "name": "John Doe",
    "age": 134,
    "email": "john.doe@example.com",
    "is_employed": True,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}



class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(ge=1)


class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=1, lt=120)
    email: EmailStr
    is_employed: bool  # смотря для чего делается, можно добавить Field(default=False)
    address: Address


    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("The name should contain only the letters.")
        return value

    @model_validator(mode="after")
    def check_employment_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError("Employed users must be between 18 and 65.")
        return self


user_1 = User(**json_input_1)
print(user_1)

# user_2 = User(**json_input_2)
# print(user_2)
#
# user_3 = User(**json_input_3)
# print(user_3)

# user_4 = User(**json_input_4)
# print(user_4)
#

