
class StatDan:
    dan = dict()

    @staticmethod
    def __getItem__( name):
        return StatDan.dan.get(name, "")

    @staticmethod
    def __setItem__(name, d):
        StatDan.dan[name] = d

    @staticmethod
    def __delItem__( name):
        del StatDan.dan[name]

    @staticmethod
    def __contains__( name):
        return name in StatDan.dan

#__getItem__ – реализация синтаксиса obj[key], получение значения по ключу;
#__setItem__ – установка значения для ключа;
#__delItem__ – удаление значения;
#__contains__ – проверка наличия значения.
