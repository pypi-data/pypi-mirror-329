from abc import ABC, abstractmethod, ABCMeta


class MetaClassUtils:
    """
    用于定义元类的工具类
    """

    def __init__(self):
        pass

    class MetaCrawlerClass(type):
        def __new__(cls, name, bases, attrs):
            print("MetaCrawlerClass.__new__ called")
            return super().__new__(cls, name, bases, attrs)

        def __init__(cls, name, bases, attrs):
            print("MetaCrawlerClass.__init__ called")
            super().__init__(name, bases, attrs)

        def __call__(cls, *args, **kwargs):
            print("MetaCrawlerClass.__call__ called")
            return super().__call__(*args, **kwargs)

    class MetaAbstractClass(ABCMeta):
        def __new__(cls, name, bases, attrs):
            new_cls = super().__new__(cls, name, bases, attrs)
            for base in bases:
                if base.__name__ == "ABC":
                    for attr_name in getattr(base, "__abstractmethods__", set()):
                        if attr_name not in attrs:
                            raise TypeError(
                                f"Can't instantiate abstract class 【{name}】 with abstract attribute 【{attr_name}】")
                        else:
                            print(f"Attribute 【{attr_name}】 is already defined in 【{name}】")
            return new_cls


if __name__ == "__main__":
    class Animal(ABC):
        @abstractmethod
        def eat(self):
            pass


    class Dog(Animal):
        # def eat(self):
        #     print("Dog is eating")
        def __new__(cls, *args, **kwargs):
            return Animal.__new__(cls)

        def __init__(self):
            print("Dog is created")


    dog = Dog()
