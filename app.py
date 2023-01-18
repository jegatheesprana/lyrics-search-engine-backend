import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from searchquery import search
from elasticsearch_dsl import Index

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
def index():
    return "Welcome to python server"


@app.route('/search', methods=['POST'])
@cross_origin()
def hello_world():
    query = json.loads(request.data)['query']
    res = search(query)
    hits = res['hits']['hits']
    time = res['took']
    # aggs = res['aggregations']
    num_results = res['hits']['total']['value']

    return jsonify({'query': query, 'hits': hits, 'num_results': num_results, 'time': time})


if __name__ == '__main__':
    app.run()
