from qdrant_client import QdrantClient

class QDrantDriver:
    _instance: QdrantClient | None = None
    def __new__(cls,*args, **kwargs):
        if cls._instance is None:
            # self.url = "http://localhost:6333" # Replace with your Qdrant server URL in docker file
            # self.size = size
            # self.name = vector_db_name
            cls._instance = QdrantClient("http://localhost:6333")
            # vectors_config = {
            #     "size": size,  # Set the vector size to 128 (as per your feature vector)
            #     "distance": "Cosine"  # Use cosine similarity for distance metric
            # }
            # self.client.recreate_collection(
            #     collection_name=vector_db_name,
            #     vectors_config=vectors_config
            # )
        return cls._instance


vectorDBClient = QDrantDriver()
