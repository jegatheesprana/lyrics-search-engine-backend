from elasticsearch import Elasticsearch


def shape_fields(fields):
    for field in fields:
        if (field == 'song_name'):
            fields.append('song_name.inflections')
            fields.append('song_name.case_insensitive')
            fields.append('song_name.case_insensitive_and_inflections')


def basic_search(query):
    return {
        "query": {
            "query_string": {
                "query": query
            }
        },
        "size": 200
    }


def year_search(year):
    return {
        "query": {
            "match": {
                "year": year
            }
        },
        "size": 200
    }


def advanced_search(query, fields):
    shape_fields(fields=fields)
    return {
        "query": {
            "multi_match": {
                "query":    query,
                "fields": fields
            }
        },
        "size": 200
    }


def search_metaphor(query, fields, metaphor):
    shape_fields(fields=fields)
    return {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "metaphors.source": {
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
        },
        "size": 200
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
            "items": {
                "terms": {"field": field,  "size": 500}
            }
        }
    }


INDEX = 'lyrics-test'
client = Elasticsearch(HOST="http://localhost", PORT=9200,
                       http_auth=('elastic', 'EMyoDwDL4UH=4GHQW5X='))


def search(query, filter, fields, metaphor, year):
    # result = client. (index=INDEX,body=standard_analyzer(query))
    # keywords = result ['tokens']['token']
    # print(keywords)
    print(query, filter, fields, metaphor)
    # query_body= process(query)
    if (year):
        query_body = year_search(year)
    elif (metaphor):
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


def unique(field):

    query_body = get_unique(field)

    res = client.search(index=INDEX, body=query_body)
    return res
