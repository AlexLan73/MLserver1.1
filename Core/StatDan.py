
class StatDan:
    dan = dict()

    @staticmethod
    def add(name, d):
        StatDan.dan[name] = d

    @staticmethod
    def read( name):
        return StatDan.dan.get(name, "")
