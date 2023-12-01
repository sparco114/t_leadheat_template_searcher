import re
from abc import abstractmethod, ABC
from datetime import datetime

from fastapi import HTTPException


# создаем класс с абстрактным методом, чтоб наследовать от него все классы валидации, которые должны
#   иметь метод validate
class TypeValidator(ABC):

    @abstractmethod
    def validate(self, data_to_validate: str) -> bool:
        pass


class DateTypeValidator(TypeValidator):
    # валидация строки на соответствие формату даты, путем попытки преобразовать данные в дату datatime,
    #   необходимых форматов
    def validate(self, data_to_validate: str) -> bool:

        field_type_is_data = False
        try:
            datetime.strptime(data_to_validate, "%Y-%m-%d")
            field_type_is_data = True
        except Exception:
            pass  # в случае любого исключения просто переходим к валидации по следующему формату даты

        try:
            datetime.strptime(data_to_validate, "%d.%m.%Y")
            field_type_is_data = True
        except Exception:
            pass  # в случае любого исключения и по этому формату значение field_type_is_data остается False

        return field_type_is_data


class PhoneTypeValidator(TypeValidator):
    # валидация строки на соответствие формату телефона, путем сравнения с заданным регулярным выражением
    def validate(self, data_to_validate: str) -> bool:
        field_type_is_phone = False
        phone_template = re.compile("^\+7 \d{3} \d{3} \d{2} \d{2}$")

        if phone_template.match(data_to_validate):
            field_type_is_phone = True

        return field_type_is_phone


class EmailTypeValidator(TypeValidator):
    # валидация строки на соответствие формату email, путем сравнения с заданным регулярным выражением
    def validate(self, data_to_validate: str) -> bool:
        field_type_is_email = False
        email_template = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,4}$")

        if email_template.match(data_to_validate):
            field_type_is_email = True

        return field_type_is_email


def validate_fields(fields: dict[str, str]) -> dict[str, str]:
    """
    Определение типа значения каждого поля на основе правил валидации.

    :param fields: словарь, в котором ключами являются имена полей, а значениями - значения этих полей

    :return: словарь, в котором ключами являются имена полей, а значениями - ТИПЫ значений этих полей
    """

    fields_with_types = {}  # словарь, в котором будут храниться результаты валидации полей

    for field_name, field_data in fields.items():

        if DateTypeValidator().validate(field_data):  # первая валидация по типу "date"
            fields_with_types[field_name] = "date"
        elif PhoneTypeValidator().validate(field_data):  # вторая валидация по типу "phone"
            fields_with_types[field_name] = "phone"
        elif EmailTypeValidator().validate(field_data):  # третья валидация по типу "email"
            fields_with_types[field_name] = "email"

        # если ни одна из валидаций не прошла успешно, тогда присваиваем тип "text"
        else:
            fields_with_types[field_name] = "text"

    return fields_with_types


def request_data_to_dict(request_data: str) -> dict[str, str]:
    """
    Преобразование полученной информации в словарь

    :param request_data: полученная в форме запроса информация

    :return: словарь, в котором ключами являются имена полей, а значениями - значения этих полей
    """
    fields_dict = {}  # словарь, в котором будут храниться результаты преобразования
    try:
        # разбиваем строку по символу '&', чтобы разделить поля, и проходим циклом по получившемуся списку полей
        for field in request_data.split('&'):
            # разбавим каждое значение по символу '=', чтобы отделить имя поля от значения поля
            field_data = field.split('=')

            # добавляем полученные имя поля и его значения в результирующий словарь
            fields_dict[field_data[0]] = field_data[1]

    except Exception as err:
        print("error:", type(err), err)
        raise HTTPException(status_code=400, detail="В запросе получена неверная форма")

    return fields_dict
