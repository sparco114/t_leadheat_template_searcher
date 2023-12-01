from template_search_app.api.utils.logic_db import take_templates_from_tinydb


def search_template(form: dict[str, str]) -> dict[str, str]:
    """
    Поиск в БД шаблона, который соответствует полученной форме

    :param form: полученная форма в виде словаря, в котором ключами являются имена полей,
            а значениями - ТИПЫ значений этих полей

    :return: - в случае, если в БД найден соответствующий шаблон: имя шаблона
             - в ином случае: полученная в качестве аргумента форма без изменений
    """

    fields_names_list = [name for name, _ in form.items()]  # список названий полей

    # пробуем получить из БД только те шаблоны, у которых имеется хотя бы одно поле указанное во входящей форме
    #   (чтобы сразу отфильтровать точно не подходящие поля и далее работать с небольшим количеством шаблонов)
    try:
        filtered_templates_list = take_templates_from_tinydb(fields_names_list)
    except Exception as err:
        print('error:', type(err), err)
        return {'error': "Не удалось получить список шаблонов из базы данных TinyDB для "
                         "поиска соответствующего шаблона"}

    template_name = ""

    for template in filtered_templates_list:

        # для каждого шаблона из отфильтрованного списка проверяем все ли его поля содержатся в полученной форме
        if all(field_name in form and form[field_name] == field_type
               for field_name, field_type in template.items() if field_name != 'name'):

            # если шаблон подходит, тогда записываем его имя и возвращаем
            template_name = template['name']
            return template_name

    # если ни один шаблон не подошел, тогда просто возвращаем саму форму
    if not template_name:
        return form
