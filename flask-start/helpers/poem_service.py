from model import Model560Epocs, Model10kEpocs


class PoemService(object):
    old_model = Model560Epocs()
    model = Model10kEpocs()

    def __init__(self):
        self.path_to_file = ""

    def pass_query_to_old_model(self, query, length):
        return self.old_model.generate(query, length)

    def pass_query_to_model(self, query, length):
        return self.model.generate(query, length)
