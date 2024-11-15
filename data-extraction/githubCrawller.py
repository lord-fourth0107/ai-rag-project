import requests
from bs4 import BeautifulSoup
import json
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
## Open file and read urls
def openFile():
    file = open("urls.txt", "r")
    urls = file.readlines()
    file.close()    
    return urls

visited_urls = []

for url in openFile():
    if url not in visited_urls:
        url = url.strip()
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        visited_urls.append(url)
        #print(soup.find("p"))   
    else:
        print("Already visited")
async def setUpDbConnection():
    dbConnectionUrl = "mongodb://localhost:27017/"
    dbConnectionClient = AsyncIOMotorClient(dbConnectionUrl)
    try:
        dbConnectionClient.server_info()
        await dbConnectionClient.admin.command('ping')
        print("Connected to MongoDB") 
    except Exception as e:
        print(e)
        await asyncio.sleep(2)
        await setUpDbConnection()
    return dbConnectionClient

def insertDataIntoDb(data,dbClient):
    client = dbClient
    db = client["github"]
    collection = db["data"]
    collection.insert_one(data)
if __name__ == "__main__":
    dbClient  = asyncio.run(setUpDbConnection())



