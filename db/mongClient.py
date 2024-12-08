from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import asyncio
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from loguru import logger
from settings import MONGO_HOST_URL


# The class `MongoDBConnector` is a singleton class that establishes a connection to a MongoDB
# database using MongoClient.
class MongoDBConnector:
    _instance: MongoClient | None = None
    def __new__(cls):
        """
        This Python function creates a singleton instance of a MongoDB client connected to a local
        server.
        
        :param cls: In the given code snippet, `cls` refers to the class itself. The `__new__` method is
        a special method in Python classes that is called to create a new instance of a class. In this
        case, the `__new__` method is being used to implement a Singleton pattern
        :return: The `__new__` method is returning an instance of the `MongoClient` class that is
        connected to a MongoDB database running on `localhost:27017`. If the `_instance` attribute is
        already set, it will return the existing instance without creating a new one.
        """
        if cls._instance is None:
            try:
                cls._instance = MongoClient(MONGO_HOST_URL) # replace this with setting files when u have docker compose
            except ConnectionFailure as e:
                logger.error(e)
            logger.info("Connected to MongoDB")
        return cls._instance
# `connection = MongoDBConnector()` is creating an instance of the `MongoDBConnector` class. This
# instance represents a connection to a MongoDB database running on `localhost:27017`. The
# `MongoDBConnector` class is designed as a singleton, meaning that only one instance of it can exist
# at a time.
connection = MongoDBConnector()
