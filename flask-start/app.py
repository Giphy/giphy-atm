from flask import Flask, request, redirect, abort, jsonify, \
    url_for, flash

import random
import string
import logging
import json
import requests

from helpers.poem_service import PoemService
from helpers.giphy_client import GiphyClient

app = Flask(__name__)
poem_service = PoemService()


@app.route('/poem', methods=['GET'])
def generate_poem():
    query = request.args.get('query')

    if not query:
        abort(400)

    giphy_client = GiphyClient()
    list_of_tags = giphy_client.get_search_tags(query)
    poem_string = ",".join(list_of_tags)

    poem = poem_service.pass_query_to_model(poem_string, 10)
    poem = '{}:\n{}'.format(query.upper(), poem)

    return jsonify({"data": poem})


@app.route('/poem_old', methods=['GET'])
def generate_old_poem():
    query = request.args.get('query')

    if not query:
        abort(400)

    giphy_client = GiphyClient()
    list_of_tags = [query] + giphy_client.get_search_tags(query, old_model=True)[:4]
    poem_string = ",".join(list_of_tags)

    poem = poem_service.pass_query_to_old_model(poem_string, 10)
    poem = '{}:\n{}'.format(query.upper(), poem)

    return jsonify({"data": poem})


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=9000)
