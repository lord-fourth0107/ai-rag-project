from qdrant_client import QdrantClient

class QDrantDriver():
    def __call__(self,vector_db_name,size):
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


vectorDBClient = QdrantClient("ai_rag",300)