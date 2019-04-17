

class Programmer(object):

    cls_argu = "Play Python"

    def __new__(cls, *args, **kwargs):

        print("call __new__ method")
        print(args)

        return super(Programmer, cls).__new__(cls, **kwargs)


    def __init__(self, name, age, gender):
        print("call __init__ method")

        self.name = name
        self._age = age
        self.__gender = gender
        print(self.__dict__)


    def __setattr__(self, key, value):
        # setattr(self, key, value)
        self.__dict__[key] = value


    def __getattribute__(self, item):
        # return getattr(self, item) # 这种用法引起无线递归
        # return self.__dict__[item] # 引起无线递归
        return super(Programmer, self).__getattribute__(item)

    def __getattr__(self, item):
        print("call __getattr__({ite})".format(ite=item))
        raise AttributeError("'{class_name}' object has no attribute '{item}'".format(class_name=self.__class__.__name__, item=item))

    def __delattr__(self, item):
        del self.__dict__[item]


    @classmethod
    def get_cls_argu(cls):
        return cls.cls_argu


    @property
    def get_age(self):
        return self._age


    @property
    def get_gender(self):
        return self.__gender


    def get_info(self):
        return "{name} is {age} {gender}".format(name=self.name, age=self._age, gender=self.__gender)


class ProgrammerL(Programmer):
    
    def __new__(cls, *args, **kwargs):
        print("call __new__ method")
        print(args)
        super(ProgrammerL, cls).__new__(*args)

    def __init__(self, name, age, gender, language):
        print("call __init__ method")
        super(ProgrammerL, self).__init__(name, age, gender)
        print(self.__dict__)
        self.language = language


    def get_info(self):
        return "{name} is {age} {gender}, my fav language is {language}".format(name=self.name, age=self._age, gender=self.get_gender, language=self.language)


def ainstance(pr):
    if isinstance(pr, Programmer):
        return pr.get_info()


if __name__ == "__main__":

    te = Programmer('louis', 30, 'male')

    te.__setattr__('language', 'Python')
    print(te.language)
    te.__delattr__('language')
    print(te.language)
    # print(te.name)
    # print(te.get_age)
    # print(te.hk)
    # print(te.get_info())

    # print(type(te))
    # print(isinstance(te,Programmer))
    # print(isinstance(te,ProgrammerL))
    # print(ainstance(te))
    # print(ainstance(te))
    # print(te.cls_argu, te.name, te.get_age, te.get_gender)
    # print(te.get_info())
    # te.get_info = 100
    # print(te.get_info)
