from qdrant_client import QdrantClient
from settings import QDRANT_HOST_URL

class QDrantDriver:
    _instance: QdrantClient | None = None
    def __new__(cls,*args, **kwargs):
        """
        The function is a custom implementation of the singleton design pattern in Python.
        
        :param cls: The `cls` parameter in the `__new__` method refers to the class itself. It is
        automatically passed as the first argument to the method and represents the class that the
        method is called on
        :return: The `__new__` method is returning an instance of the `QdrantClient` class, which is
        created with the `QDRANT_HOST_URL` as a parameter.
        """
        if cls._instance is None:
          
            cls._instance = QdrantClient(QDRANT_HOST_URL)
        return cls._instance

# `vectorDBClient = QDrantDriver()` is creating an instance of the `QDrantDriver` class using a custom
# implementation of the singleton design pattern in Python. The `__new__` method of the `QDrantDriver`
# class ensures that only one instance of the `QdrantClient` class is created and returned. This
# instance is stored in the `vectorDBClient` variable, allowing access to the QdrantClient
# functionality with the specified `QDRANT_HOST_URL`.

vectorDBClient = QDrantDriver()
