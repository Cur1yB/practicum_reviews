# Ревью

# Python-код

Спасибо за предоставленный код, ты проделал большую работу. Давай разберёмся, как его можно улучшить, чтобы сделать его ещё лучше.

Во-первых, в коде не хватает обработки исключений. Например, если база данных недоступна или данные в ней некорректны, программа упадёт без объяснения. Для улучшения добавь обработку ошибок при подключении к SQLite и взаимодействии с Elasticsearch. Это сделает приложение более устойчивым.

Во-вторых, в коде использованы жёстко заданные значения для имени базы данных и параметров подключения к Elasticsearch. Это неудобно для масштабирования и изменения окружения. Лучше использовать переменные окружения.

Ещё замечание по поводу структуры: в функции `transform` встречаются переменные с двойными подчёркиваниями, что может вызывать путаницу. Лучше использовать стандартные имена. 

Импорт `pprint` внутри функции нарушает порядок, следуй PEP 8 и перенеси все импорты в начало файла. Но в идеале использовать библиотеку `logging`.

Сейчас код завершается с ошибкой при попытке подключения к Elasticsearch. Проверь параметры подключения
```bash
Traceback (most recent call last):
  File "/home/alexandr/yandex_practicum/main.py", line 124, in <module>
    load(transform(*extract()))
  File "/home/alexandr/yandex_practicum/main.py", line 119, in load
    bulk(es, acts)
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/helpers/actions.py", line 410, in bulk
    for ok, item in streaming_bulk(
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/helpers/actions.py", line 329, in streaming_bulk
    for data, (ok, info) in zip(
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/helpers/actions.py", line 256, in _process_bulk_chunk
    for item in gen:
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/helpers/actions.py", line 195, in _process_bulk_chunk_error
    raise error
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/helpers/actions.py", line 240, in _process_bulk_chunk
    resp = client.bulk(*args, body="\n".join(bulk_actions) + "\n", **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/client/utils.py", line 347, in _wrapped
    return func(*args, params=params, headers=headers, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/client/__init__.py", line 472, in bulk
    return self.transport.perform_request(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/transport.py", line 417, in perform_request
    self._do_verify_elasticsearch(headers=headers, timeout=timeout)
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/transport.py", line 606, in _do_verify_elasticsearch
    raise error
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/transport.py", line 569, in _do_verify_elasticsearch
    _, info_headers, info_response = conn.perform_request(
                                     ^^^^^^^^^^^^^^^^^^^^^
  File "/home/alexandr/yandex_practicum/.venv/lib/python3.12/site-packages/elasticsearch/connection/http_urllib3.py", line 280, in perform_request
    raise ConnectionError("N/A", str(e), e)
elasticsearch.exceptions.ConnectionError: ConnectionError((<urllib3.connection.HTTPConnection object at 0x75ff320e17c0>, 'Connection to 192.168.1.252 timed out. (connect timeout=10)'))
```

Также стоит обратить внимание на оптимизацию SQL-запросов. Их можно переписать так, чтобы уменьшить количество подзапросов и увеличить скорость выполнения.
Подумай об использовании LEFT JOIN

```SQL
select id, imdb_rating, genre, title, plot, director,
        -- comma-separated actor_id's
        (
            select GROUP_CONCAT(actor_id) from
            (
                select actor_id
                from movie_actors
                where movie_id = movies.id
            )
        ),
        
        max(writer, writers)
        from movies
```

Документация описывает не полностью функционал, иногда не указано, что функции возвращают, либо что они делают.

Наконец, избегай оставлять отладочные команды вроде `print` в финальной версии кода — они засоряют логи. Вместо этого используй `logging`.

Кроме того, в коде имеются многочисленые нарушения PEP 8:

```bash
main.py:11:1: E302 expected 2 blank lines, found 1
main.py:22:80: E501 line too long (116 > 79 characters)
main.py:24:80: E501 line too long (157 > 79 characters)
main.py:37:1: W293 blank line contains whitespace
main.py:43:80: E501 line too long (87 > 79 characters)
main.py:46:1: W293 blank line contains whitespace
main.py:47:1: W293 blank line contains whitespace
main.py:48:5: E303 too many blank lines (2)
main.py:48:80: E501 line too long (130 > 79 characters)
main.py:49:80: E501 line too long (99 > 79 characters)
main.py:50:80: E501 line too long (101 > 79 characters)
main.py:63:65: W291 trailing whitespace
main.py:64:68: W291 trailing whitespace
main.py:65:56: W291 trailing whitespace
main.py:70:80: E501 line too long (104 > 79 characters)
main.py:78:80: E501 line too long (102 > 79 characters)
main.py:79:80: E501 line too long (101 > 79 characters)
main.py:109:75: W291 trailing whitespace
main.py:110:77: W291 trailing whitespace
main.py:116:80: E501 line too long (110 > 79 characters)
main.py:117:80: E501 line too long (115 > 79 characters)
main.py:118:1: W293 blank line contains whitespace
main.py:128:1: E302 expected 2 blank lines, found 1
main.py:135:70: W291 trailing whitespace
main.py:142:1: E305 expected 2 blank lines after class or function definition, found 1
main.py:143:32: W292 no newline at end of file
```
Их необходимо исправить. 

# Тесты

Теперь давай перейдем к тестам:

В тесте **Проверка количества элементов** у тебя есть строчка:
```javascript
pm.expect(jsonData['hits']['total']['value']).to.equal(999);
```
Здесь ты жёстко задаёшь ожидание, что записей ровно 999. Но стоит учесть, что количество данных может меняться при обновлении или миграции. Попробуй сделать проверку более гибкой, например, проверять, что число не нулевое или выше определённого минимума, если тебе не важен точный размер.

Ещё пример из теста на поиск по слову `camp`:
```javascript
pm.expect(jsonData['hits']['max_score']).to.equal(7.500733);
```
`max_score` – это метрика, которую Elasticsearch может менять при любых изменениях данных. Жёстко фиксировать такое значение — плохая идея. Если цель теста — проверить, что ответ не пустой или что вернулись какие-то подходящие записи, лучше проверить наличие необходимого поля или факт, что найдено хотя бы несколько записей, соответствующих запросу.

В тестах типа **Запрос на поиск N/A элементов** ты делаешь проверку:
```javascript
pm.expect(jsonData['hits']['total']['value']).to.equal(7);
pm.expect(pm.response.text()).not.to.have.string('N/A');
```
Если у тебя в будущем появятся дополнительные данные без ‘N/A’, тест упадёт при их изменении. Может лучше проверить, что `N/A` действительно отсутствует, но не жёстко зафиксировать число результатов? Так твои тесты будут менее хрупкими.

Наконец, стоит обратить внимание на структуры данных. Если, например, в коде `writers_names` возвращается строкой, а ты проверяешь, как будто это массив, ничего не сработает. Приведи тесты в соответствие с фактической структурой ответа.

Сейчас тесты смотрят только на определённые значения. Было бы полезно проверить, что все нужные поля вообще присутствуют и имеют ожидаемый тип данных. 

Сейчас твои тесты проверяют только успешные варианты запросов. А что, если запрос будет некорректным? Или Elasticsearch временно будет недоступен? В реальном окружении такие ситуации не редкость. Стоит добавить тесты, которые проверяют реакцию системы на неправильные параметры поиска или отсутствие данных. 

## Резюме

Проект отправлен на доработку, жду исправленую версию. Удачи!

### Полезные ссылки

https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html - документация по Elasticsearch

https://habr.com/ru/articles/489924/ - полезная статья на Хабр по Elasticsearch

https://habr.com/ru/articles/767558/ - информация по линтерам

https://habr.com/ru/companies/yandex_praktikum/articles/743422/ - хорошая статья по использованию JOIN

https://habr.com/ru/companies/wunderfund/articles/736526/ - статья по обработке исключений

https://peps.python.org/pep-0257/ - информация по документации

https://ramziv.com/article/40 - как использовать переменные окружения

https://docs.python.org/3/library/logging.html - документация по библиотеке logging