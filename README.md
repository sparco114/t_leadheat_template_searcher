# Инструкция для проверки

1. Клонировать репозиторий

```git clone git@github.com:sparco114/t_leadheat_template_searcher.git```

2. Перейти в директорию проекта

```cd t_leadheat_template_searcher/```

3. Зпустить виртуальное окружение и установить необходимые зависимости

```poetry shell```

```poetry install```

4. Выполнить файл, который запустит сервер

```python3 run_app.py```

5. В новой вкладке терминала перейти в папку проекта

```cd t_leadheat_template_searcher/```

6. Зпустить виртуальное окружение

```poetry shell```

7. Выполнить скрипт, который отправит тестовые запросы на запущеный сервер
   
```python3 test_request_script.py```
