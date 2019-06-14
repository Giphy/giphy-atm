from os import environ
import requests
import json
from collections import Counter


class GiphyClient(object):
    def __init__(self):
        self.api_key = 'Oly8X4hCcCgTwilQVrYXnSZK9xlGHGrV'
        self.url = 'http://api.giphy.com/v1/gifs/search'

    def clean_list_of_tags(self, tags, query):
        return [tag for tag in tags if tag != '' and query not in tag]

    def get_all_tags(self, gifs):
        tags = []
        for gif in gifs:
            for tag in gif['tags']:
                tags.append(tag)

        return tags

    def strip_out_most_common_tags(self, list):
        counts = Counter(list).most_common(5)
        most_common_terms = []
        for term in counts:
            most_common_terms.append(term[0])
        return most_common_terms

    def get_search_tags(self, query):
        response = requests.get(self.url, params={
            "api_key": self.api_key, "q": query, "limit": 25})
        gifs = json.loads(response.content)['data']
        list_of_tags = []
        list_of_tags = self.get_all_tags(gifs)
        cleaned_tags = self.clean_list_of_tags(list_of_tags, query)

        five_most_common_terms = self.strip_out_most_common_tags(cleaned_tags)

        return five_most_common_terms
