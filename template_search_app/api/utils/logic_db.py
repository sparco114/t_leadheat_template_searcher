from functools import reduce

from tinydb import Query as tinydbQuery, TinyDB

db_templates = TinyDB('./template_search_app/api/db_templates.json')
Templates = tinydbQuery()


def take_templates_from_tinydb(fields_names_for_query: list[str]) -> list[dict]:
    """
    Поиск в БД шаблонов, имеющих хотя бы одно поле, указанное в полученном списке.

    :param fields_names_for_query: список полей, которые может иметь шаблон

    :return: список подходящих по условиям шаблонов (которые записаны в виде словарей)
    """

    # формируем запрос в БД, чтобы получить все шаблоны, которые имеют хотя бы одно поле, указанное в списке
    query_params = reduce(lambda acc, field_name: acc | Templates[f'{field_name}'].exists(),
                          fields_names_for_query,
                          Templates.query_params[0].exists())

    query_result = db_templates.search(query_params)

    # формируем список словарей, где словарями будут найденные шаблоны
    result_list_of_dict = [dict(template) for template in query_result]
    return result_list_of_dict


def insert_templates_in_tinydb(new_template: dict[str, str]) -> dict[str, str]:

    try:
        # изменяем вид словаря так, чтоб все элементы вложенного словаря 'fields' стали элементами основного
        #   словаря, то есть формируем словарь без вложенностей
        template_to_db = {'name': new_template['name'], **new_template['fields']}

        # записываем данные в ДБ
        db_templates.insert(template_to_db)
        return template_to_db

    except Exception as err:
        print('error:', type(err), err)
        return {'error': "Ошибка записи нового шаблона в базу данных TinyDB"}
