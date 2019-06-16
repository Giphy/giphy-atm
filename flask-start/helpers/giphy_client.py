from os import environ
import requests
import json
from collections import Counter
from model import vocab_to_int


class GiphyClient(object):
    def __init__(self):
        self.api_key = 'Oly8X4hCcCgTwilQVrYXnSZK9xlGHGrV'
        self.url = 'http://api.giphy.com/v1/gifs/search'

    def clean_list_of_tags(self, tags, query):
        return [tag for tag in tags if tag != '' and query not in tag]

    def get_all_tags(self, gifs):
        tags = []
        for gif in gifs['data']:
            for tag in gif['tags']:
                tags.append(tag)

        return tags

    def strip_out_most_common_tags_old(self, list):
        counts = Counter(list).most_common(5)

        most_common_terms = []
        for term in counts:
            most_common_terms.append(term[0])

        return most_common_terms

    def strip_out_most_common_tags(self, list):
        counts = Counter(list).most_common(100)

        # Get tags that exist in corpus
        most_common_terms = []
        for term in counts:
            if term[0] in vocab_to_int:
                most_common_terms.append(term[0])

        return most_common_terms[:5]

    def get_search_tags(self, query, old_model=False):
        response = requests.get(self.url, params={
            "api_key": self.api_key, "q": query, "limit": 25})
        gifs = json.loads(response.content.decode('utf-8'))

        list_of_tags = self.get_all_tags(gifs)
        cleaned_tags = self.clean_list_of_tags(list_of_tags, query)

        if old_model:
            five_most_common_terms = [query] + self.strip_out_most_common_tags_old(cleaned_tags)[:4]
        elif query in vocab_to_int:
            five_most_common_terms = [query] + self.strip_out_most_common_tags(cleaned_tags)[:4]
        else:
            five_most_common_terms = self.strip_out_most_common_tags(cleaned_tags)

        return five_most_common_terms
