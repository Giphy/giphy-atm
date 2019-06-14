from sean import call_model


class PoemService(object):
    def __init__(self):
        self.path_to_file = ""

    def pass_query_to_model(self, query, length):
        return call_model(query, length)
