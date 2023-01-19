import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from searchquery import search, autofill, unique
from elasticsearch_dsl import Index

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
def index():
    return "Welcome to python server"


@app.route('/search', methods=['POST'])
@cross_origin()
def search_controller():
    data = json.loads(request.data)
    query = data['query']
    metaphor = data['metaphor']
    year = data['year']
    if ('filter' in data):
        filter = data['filter']
        fields = data['fields']
    else:
        filter = False
        fields = []
    res = search(query, filter=filter, fields=fields,
                 metaphor=metaphor, year=year)
    hits = res['hits']['hits']
    time = res['took']
    # aggs = res['aggregations']
    num_results = res['hits']['total']['value']

    return jsonify({'query': query, 'results': hits, 'total_results': num_results, 'time': time})


@app.route('/autofill', methods=['POST'])
@cross_origin()
def autofill_controller():
    data = json.loads(request.data)
    query = data['query']

    res = autofill(query)
    hits = res['hits']['hits']
    time = res['took']
    # aggs = res['aggregations']
    num_results = res['hits']['total']['value']

    return jsonify({'query': query, 'results': hits, 'total_results': num_results, 'time': time})


@app.route('/unique', methods=['POST'])
@cross_origin()
def unique_controller():
    data = json.loads(request.data)
    field = data['field']

    res = unique(field)
    items = res['aggregations']['items']['buckets']

    return jsonify(items)


if __name__ == '__main__':
    app.run()
