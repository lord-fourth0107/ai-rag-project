from vectorDBdriver import vectorDBClient
from typing import Any
from uuid import UUID
import numpy as np 
from qdrant_client.models import CollectionInfo, PointStruct, Record


class BaseVectorDocument:
    def _uuid_to_str(self, item: Any) -> Any:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, UUID):
                    item[key] = str(value)
                elif isinstance(value, list):
                    item[key] = [self._uuid_to_str(v) for v in value]
                elif isinstance(value, dict):
                    item[key] = {k: self._uuid_to_str(v) for k, v in value.items()}

        return item
    

    def batch_upsert(self,embedded_chunks):
        if not isinstance(embedded_chunks,list):
            embedded_chunks = [embedded_chunks]
        for embedded_chunk in embedded_chunks:
            payload = self._uuid_to_str(embedded_chunk.__dict__)
            vector = payload.pop("embedding", {})
            uuid = str(payload.pop("uuid"))
            if vector and isinstance(vector, np.ndarray):
                vector = vector.tolist()
            annotated = PointStruct(id=uuid, vector=vector, payload=payload)
            vectorDBClient.upsert(annotated)

    
    def similarity_search(self,query,rank=10):
        
        search_result = vectorDBClient.search(
            collection_name="ai_rag",
            query_vector=query.tolist(),
            limit=rank,  # Number of similar items to retrieve
            with_payload=True
        )
        metadata = []
        for result in search_result:
            metadata.append(result.payload)
        return metadata
        