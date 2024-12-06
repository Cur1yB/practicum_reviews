# Ревью

Спасибо за предоставленный код, ты проделал большую работу. Давай разберёмся, как его можно улучшить, чтобы сделать его ещё лучше.

Начнем с главного - библиотека `validate` не поддерживается в python3, зависимости даже невозможно будет установить, не говоря о запуске кода. Подумай о том, чтобы заменить её на что-то современное вроде `pydantic` или `marshmallow`.

Обрати внимание на комментарии — у тебя там явно проблемы с кодировкой. Это не выглядит красиво и сбивает с толку. Просто перепиши их нормальным читаемым текстом. 

Ещё один момент: в функциях нет докстрингов. Они не обязательны, но очень помогают понять логику и назначение каждой функции. Пара коротких строк, описывающих, что делает функция, какие параметры принимает и что возвращает, могут здорово облегчить жизнь и тебе, и любому, кто будет потом работать с твоим кодом.

Сейчас у тебя настройки хоста и порта для захардкожены прямо в коде. Это может стать проблемой, если тебе нужно будет менять настройки на продакшене или на другом окружении.

Ещё один момент — в коде вызывается close() у объекта es_client, но у используемого клиента Elasticsearch метод close() отсутствует. 

И, наконец, не стоит использовать print для вывода сообщений о проблемах. Гораздо удобнее перейти на логирование с помощью стандартного модуля logging. 

Кроме того, в коде имеются многочисленые нарушения PEP 8:
```bash
task_2/main.py:5:67: W291 trailing whitespace
task_2/main.py:16:1: E302 expected 2 blank lines, found 1
task_2/main.py:31:71: W291 trailing whitespace
task_2/main.py:37:80: E501 line too long (167 > 79 characters)
task_2/main.py:38:71: W291 trailing whitespace
task_2/main.py:39:80: E501 line too long (93 > 79 characters)
task_2/main.py:65:1: W293 blank line contains whitespace
task_2/main.py:89:80: E501 line too long (85 > 79 characters)
task_2/main.py:102:2: E114 indentation is not a multiple of 4 (comment)
task_2/main.py:103:1: E305 expected 2 blank lines after class or function definition, found 1
task_2/main.py:104:37: W292 no newline at end of file
```

Их необходимо исправить.

## Резюме

Проект отправлен на доработку, жду исправленую версию. Удачи!

### Полезные ссылки

https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html - документация по Elasticsearch

https://habr.com/ru/articles/489924/ - полезная статья на Хабр по Elasticsearch

https://habr.com/ru/companies/amvera/articles/851642/ - статья по использованию валидатора pydantic (вместо устаревшего validate)

https://habr.com/ru/articles/767558/ - информация по линтерам

https://ramziv.com/article/40 - как использовать переменные окружения

https://docs.python.org/3/library/logging.html - документация по библиотеке logging