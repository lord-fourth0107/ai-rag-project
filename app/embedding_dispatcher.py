from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from qdrant_client import QdrantClient

class MongoDBDriver:
    def set_credentials(self,user_name,password,port):
        self.user_name = user_name
        self.password = password
        self.port = port
    

    def client(self):
        uri = "mongodb://{}:{}@localhost:{}/?authSource=admin".format(self.user_name,self.password,self.port);
        return MongoClient(uri)
    
class EmbeddingHandler:
    def set_data(self,sentences):
        self.model = SentenceTransformer('sentence-transformers/average_word_embeddings_glove.6B.300d')
        self.embeddings = [self.model.encode(sentence)for sentence in sentences ]
        return self.embeddings


class QDrantDriver:
    def create_client(self,vector_db_name,size):
        self.url = "http://localhost:6333"
        self.size = size
        self.name = vector_db_name
        self.client = QdrantClient(self.url)
        vectors_config = {
            "size": size,  # Set the vector size to 128 (as per your feature vector)
            "distance": "Cosine"  # Use cosine similarity for distance metric
        }
        self.client.recreate_collection(
            collection_name=vector_db_name,
            vectors_config=vectors_config
        )


    def insert_vector_db(self,embeddings):
        for id,vector in enumerate(embeddings):
            self.client.upsert(
            collection_name=self.name,
            points=[
                {
                    "id": id,
                    "vector": vector.tolist()
                }
            ]
            )
            print(id)


user_name = "admin"
password = "#rag_project"
port = "27017"
# Connect to the database and collection
db_driver = MongoDBDriver()
db_driver.set_credentials(user_name,password,port)
client = db_driver.client()
db = client['rag']  # Replace 'myDatabase' with your database name
collection = db['repositories']  # Replace 'myCollection' with your collection name

# Read all documents from the collection
documents = collection.find()
#print(documents)
for document in documents:
    # Access the 'content' field in the document
    content = document.get('content', '')  # Default to an empty string if 'content' is missing
    if content:
        sentences = list(content.values())
embedding_driver = EmbeddingHandler()
embeddings = embedding_driver.set_data(sentences)
print(embeddings[0])
print(len(embeddings))

vector_db_object = QDrantDriver();
vector_db_object.create_client('github_etl_embeddings',300)
vector_db_object.insert_vector_db(embeddings=embeddings)

