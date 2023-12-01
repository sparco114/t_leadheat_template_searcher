from fastapi import Request, APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

from template_search_app.api.models import Template
from template_search_app.api.utils.logic_db import insert_templates_in_tinydb
from template_search_app.api.utils.logic_search import search_template
from template_search_app.api.utils.logic_validate import validate_fields, request_data_to_dict


router = APIRouter()


@router.post("/get_form/")
async def get_form(req: str = Form()):
    """
    Получение имени шаблона, который соответствует отправленной в запросе форме.

    :param req: строка в формате "f_name1=value1&f_name2=value2"

    :return: - в случае, если в БД найден соответствующий шаблон: имя шаблона
             - в ином случае: полученная в запросе форма, в которой вместо значений полей будет указан их тип,
                на основании правил валидации предусмотренных функцией validate_fields
    """

    # преобразуем полученную информацию в словарь, для дальнейшей валидации
    fields_dict = request_data_to_dict(req)

    # валидируем типы полей в полученной форме
    form_with_fields_types = validate_fields(fields_dict)

    # ищем в БД шаблон, соответствующий форме
    template_name = search_template(form_with_fields_types)
    return JSONResponse(content=template_name, status_code=200)


@router.post("/create_new_template/")
async def create_new_template(new_template: Template):
    """
    Создание нового шаблона

    :param new_template: данные для создания нового шаблона в формате словаря, с ключами 'name' и 'fields',
            где значение 'fields' является словарем, в котором ключами являются названия полей, а значениями
            являются значения этих полей

    :return: данные созданного шаблона
    """
    new_template_dict = dict(new_template)  # преобразуем в словарь для передачи в функцию

    # добавляем шаблон в БД
    created_template = insert_templates_in_tinydb(new_template_dict)
    return JSONResponse(content=created_template, status_code=201)
