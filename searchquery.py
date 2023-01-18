from elasticsearch import Elasticsearch


def shape_fields(fields):
    for field in fields:
        if (field == 'song_name'):
            fields.append('song_name.inflections')
            fields.append('song_name.case_insensitive')
            fields.append('song_name.case_insensitive_and_inflections')


def basic_search(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        },
        "size": 200
    }
    return q


def advanced_search(query, fields):
    shape_fields(fields=fields)
    q = {
        "query": {
            "multi_match": {
                "query":    query,
                "fields": fields
            }
        }
    }
    return q


def search_metaphor(query, fields, metaphor):
    shape_fields(fields=fields)
    return {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "metaphors.target": {
                            "query": metaphor
                        }
                    }
                },
                "should": {
                    "multi_match": {
                        "query":    query,
                        "fields": fields
                    }
                }
            }
        }
    }


def get_autofill(query):
    return {
        "query": {
            "query_string": {
                "query": query+"*",
                "fields": ["song_name", "song_name.case_insensitive", "song_name.case_insensitive_and_inflections", "song_name.inflections"]
            }
        }
    }


def get_unique(field):
    return {
        "size": 0,
        "aggs": {
            "years": {
                "terms": {"field": "year",  "size": 500}
            }
        }
    }


INDEX = 'lyrics-test'
client = Elasticsearch(HOST="http://localhost", PORT=9200,
                       http_auth=('elastic', 'EMyoDwDL4UH=4GHQW5X='))


def search(query, filter, fields, metaphor):
    # result = client. (index=INDEX,body=standard_analyzer(query))
    # keywords = result ['tokens']['token']
    # print(keywords)
    print(query, filter, fields, metaphor)
    # query_body= process(query)
    if (metaphor):
        query_body = search_metaphor(query, fields, metaphor)
    else:
        query_body = advanced_search(
            query, fields) if filter else basic_search(query)
    print('Making Basic Search ')
    res = client.search(index=INDEX, body=query_body)
    return res


def autofill(query):

    query_body = get_autofill(query)

    res = client.search(index=INDEX, body=query_body)
    return res
