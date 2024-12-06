from flask import Flask, abort, request, jsonify
import elasticsearch as ES

# Библиотека validate устарела, и не поддерживается в python 3
# стоит рассмотреть современные альтернативы для валидации данных, 
# такие как pydantic, Cerberus или marshmallow.
from validate import validate_args

app = Flask(__name__)


@app.route('/')
def index():
    return 'worked'

@app.route('/api/movies/')
def movie_list():
    validate = validate_args(request.args)

    if not validate['success']:
        # Ошибка валидации не даёт информативного ответа пользователю,
        # можно добавить описание проблемы.
        return abort(422)

    defaults = {
        'limit': 50,
        'page': 1,
        'sort': 'id',
        'sort_order': 'asc'
    }
    # здесь и далее по тексту стоит переписать комментарии на читаемом 
    # языке, поплыла кодировка
    # РўСѓС‚ СѓР¶Рµ РІР°Р»РёРґРЅРѕ РІСЃРµ
    for param in request.args.keys():
        defaults[param] = request.args.get(param)

    # РЈС…РѕРґРёС‚ РІ С‚РµР»Рѕ Р·Р°РїСЂРѕСЃР°. Р•СЃР»Рё Р·Р°РїСЂРѕСЃ РЅРµ РїСѓСЃС‚РѕР№ - РјСѓР»СЊС‚РёСЃРµСЂС‡, РµСЃР»Рё РїСѓСЃС‚РѕР№ - РІС‹РґР°РµС‚ РІСЃРµ С„РёР»СЊРјС‹
    # Если параметр search отсутствует, запрос отправляется без query. 
    # Это может быть некорректно обработано Elasticsearch, лучше явно использовать match_all.
    body = {
        "query": {
            "multi_match": {
                "query": defaults['search'],
                "fields": ["title"]
            }
        }
    } if defaults.get('search', False) else {}
    # Оптимизировать создание _source, чтобы избежать лишнего дублирования.
    body['_source'] = dict()
    body['_source']['include'] = ['id', 'title', 'imdb_rating']

    params = {
        # '_source': ['id', 'title', 'imdb_rating'],
        'from': int(defaults['limit']) * (int(defaults['page']) - 1),
        'size': defaults['limit'],
        'sort': [
            {
                defaults["sort"]: defaults["sort_order"]
            }
        ]
    }
    # параметры подключения к Elasticsearch захардкожены.
    # рекомендуется использовать переменные окружения для большей гибкости
    es_client = ES.Elasticsearch([{'host': '192.168.11.128', 'port': 9200}], )
    
    search_res = es_client.search(
        body=body,
        index='movies',
        params=params,
        filter_path=['hits.hits._source']
    )
    # Метод close() у клиента Elasticsearch отсутствует,
    # этот вызов вызовет ошибку
    es_client.close()
    # Отсутствует проверка ключа hits в ответе, это может вызвать
    # KeyError, если Elasticsearch вернёт неожиданное значение.
    return jsonify([doc['_source'] for doc in search_res['hits']['hits']])


@app.route('/api/movies/<string:movie_id>')
def get_movie(movie_id):
    # параметры подключения к Elasticsearch захардкожены.
    # рекомендуется использовать переменные окружения для большей гибкости
    # Также, чтобы избежать излишнего дублирования кода, можно вынести
    # в отдельную функцию
    es_client = ES.Elasticsearch([{'host': '192.168.11.128', 'port': 9200}], )

    if not es_client.ping():
        # Этот print лучше заменить на логирование, и добавить конкретную информацию.
        print('oh(')

    search_result = es_client.get(index='movies', id=movie_id, ignore=404)

    es_client.close()

    if search_result['found']:
        return jsonify(search_result['_source'])
    # Ошибка 404 не информативна для пользователя, можно добавить описание,
    # что именно не найдено.
    return abort(404)

 # Хост и порт приложения лучше тоже вынести в переменные окружения.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)