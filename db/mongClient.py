from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import asyncio
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError,ConnectionFailure
from loguru import logger


class MongoDBConnector:
    _instance: MongoClient | None = None
    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = MongoClient("mongodb://localhost:27017/") # replace this with setting files when u have docker compose
            except ConnectionFailure as e:
                logger.error(e)
            logger.info("Connected to MongoDB")
        return cls._instance
connection = MongoDBConnector()
# def insertDataIntoDb(data,dbClient):
#     client = dbClient
#     db = client["github"]
#     collection = db["data"]
#     collection.insert_one(data)

# async def setUpDbConnection():
#     dbConnectionUrl = "mongodb://localhost:27017/"
#     dbConnectionClient = AsyncIOMotorClient(dbConnectionUrl)
#     try:
#         dbConnectionClient.server_info()
#         await dbConnectionClient.admin.command('ping')
#         print("Connected to MongoDB") 
#     except Exception as e:
#         print(e)
#         await asyncio.sleep(2)
#         await setUpDbConnection()
#     return dbConnectionClient
