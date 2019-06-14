from flask import Flask, request, redirect, abort, jsonify, \
    url_for, flash

import random
import string
import logging
import json
import requests

from helpers.poem_generate import PoemService
from helpers.giphy_client import GiphyClient

app = Flask(__name__)


@app.route('/poem', methods=['GET'])
def generate_poem():
    query = request.args.get('query')

    if not query:
        abort(400)

    giphy_client = GiphyClient()
    # list_of_tags = giphy_client.get_search_tags(query)

    poem_instance = PoemService()
    poem = poem_instance.pass_query_to_model(query, 25)

    return jsonify({"data": poem})


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
