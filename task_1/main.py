import sqlite3
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def extract():
    """
    extract data from sql-db
    :return:
    """
    # В документации не описано, что возвразает функция
    # имя базы данных и параметры подключения к Elasticsearch захардкожены.
    # рекомендуется использовать переменные окружения для большей гибкости
    connection = sqlite3.connect("db.sqlite")
    cursor = connection.cursor()
    # здесь и далее по тексту стоит переписать комментарии на читаемом 
    # языке, поплыла кодировка
    # РќР°РІРµСЂРЅСЏРєР° СЌС‚Рѕ РїРёР»РёС‚СЃСЏ РІ РѕРґРёРЅ sql - Р·Р°РїСЂРѕСЃ, РЅРѕ РјРЅРµ РєР°Рє-С‚Рѕ Р»РµРЅРёРІРѕ)

    # РџРѕР»СѓС‡Р°РµРј РІСЃРµ РїРѕР»СЏ РґР»СЏ РёРЅРґРµРєСЃР°, РєСЂРѕРјРµ СЃРїРёСЃРєР° Р°РєС‚РµСЂРѕРІ Рё СЃС†РµРЅР°СЂРёСЃС‚РѕРІ, РґР»СЏ РЅРёС… С‚РѕР»СЊРєРѕ id
    # Здесь стоит добавить комментарий о цели SQL-запроса.
    # Кроме того запрос не оптимизирован, подумай об использовании 
    # LEFT JOIN
    cursor.execute("""
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
    """)

    raw_data = cursor.fetchall()
    # здесь стоит удалить закомментированный код или добавить пояснение, зачем он нужен
    # cursor.execute('pragma table_info(movies)')
    # pprint(cursor.fetchall())
    
    
    # РќСѓР¶РЅС‹ РґР»СЏ СЃРѕРѕС‚РІРµС‚СЃРІРёСЏ РёРґРµРЅС‚РёС„РёРєР°С‚РѕСЂР° Рё С‡РµР»РѕРІРµРєРѕС‡РёС‚Р°РµРјРѕРіРѕ РЅР°Р·РІР°РЅРёСЏ
    actors = {row[0]: row[1] for row in cursor.execute('select * from actors where name != "N/A"')}
    writers = {row[0]: row[1] for row in cursor.execute('select * from writers where name != "N/A"')}

    return actors, writers, raw_data


def transform(__actors, __writers, __raw_data):
    """

    :param __actors:
    :param __writers:
    :param __raw_data:
    :return:
    """
    # использование двойных подчёркиваний в названиях переменных 
    # (__actors, __writers) нестандартно и может вызывать путаницу. 
    # Рекомендуется использовать более привычные имена, 
    # например, actors, writers. 
    # В докстринг отстутствует информация о том, что делает 
    # и что возвращает функция. 
    documents_list = []
    for movie_info in __raw_data:
        # Р Р°Р·С‹РјРµРЅРѕРІР°РЅРёРµ СЃРїРёСЃРєР°
        movie_id, imdb_rating, genre, title, description, director, raw_actors, raw_writers = movie_info
        # Возможны ошибки, если raw_writers равен None или пустой строке,
        # желательно добавить обработку исключений.
        if raw_writers[0] == '[':
            parsed = json.loads(raw_writers)
            new_writers = ','.join([writer_row['id'] for writer_row in parsed])
        else:
            new_writers = raw_writers
        # Необходимо убедиться, что raw_actors и new_writers не равны None
        # перед разделением строки.
        writers_list = [(writer_id, __writers.get(writer_id)) for writer_id in new_writers.split(',')]
        actors_list = [(actor_id, __actors.get(int(actor_id))) for actor_id in raw_actors.split(',')]

        document = {
            "_index": "movies",
            "_id": movie_id,
            "id": movie_id,
            "imdb_rating": imdb_rating,
            "genre": genre.split(', '),
            "title": title,
            "description": description,
            "director": director,
            "actors": [
                {
                    "id": actor[0],
                    "name": actor[1]
                }
                # Зачем здесь проверка if actor[1]? Перенеси в 
                # list comprehension при создании actors_list.
                for actor in set(actors_list) if actor[1]
            ],
            "writers": [
                {
                    "id": writer[0],
                    "name": writer[1]
                }
                # Аналогично, зачем здесь if writer[1]? Лучше
                # сразу фильтровать при формировании writers_list.
                for writer in set(writers_list) if writer[1]
            ]
        }

        for key in document.keys():
            if document[key] == 'N/A':
                # тут лучше убрать ненужный print. Если это нужно для отладки, 
                # используй logging.
                # print('hehe')
                document[key] = None

        document['actors_names'] = ", ".join([actor["name"] for actor in document['actors'] if actor]) or None
        document['writers_names'] = ", ".join([writer["name"] for writer in document['writers'] if writer]) or None
        
        # желательно переместить импорт pprint в начало файла или использовать
        # логирование
        import pprint
        pprint.pprint(document)

        documents_list.append(document)

    return documents_list

def load(acts):
    """

    :param acts:
    :return:
    """
    # В документации не указано, что функция делает, и что возвращает

    # тут стоит указать параметры подключения через переменные окружения
    es = Elasticsearch([{'host': '192.168.1.252', 'port': 9200}])
    bulk(es, acts)

    return True # Зачем возврат значения, если далее оно не используется?

if __name__ == '__main__':
    load(transform(*extract()))