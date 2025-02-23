# MIT License
#
# Copyright (c) 2025 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams, Distance


class Qdrant:
    """Wrapper for Qdrant vector database operations."""

    def __init__(self, qdrant_url: str, qdrant_api_key: str):
        """Initialize Qdrant client.

        Args:
            qdrant_url (str): Qdrant server URL.
            qdrant_api_key (str): API key for authentication.
        """
        self._client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    def create_collection_if_not_exist(self, collection: str, size=1536):
        """Create a collection if it doesn't exist.

        Args:
            collection (str): Collection name.
            size (int): Vector size (default: 1536).
        """
        if not self._client.collection_exists(collection):
            self._client.create_collection(
                collection,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE),
            )

    def insert(self, collection: str, embeddings: list, ids: list, payloads: list):
        """Insert points into a collection.

        Args:
            collection (str): Collection name.
            embeddings (list): List of embeddings to insert.
            ids (list): List of IDs corresponding to each embedding.
            payloads (list): List of payloads corresponding to each embedding.

        Returns:
            API response for the upsert operation.
        """
        if len(embeddings) != len(ids) or len(embeddings) != len(payloads):
            raise ValueError("Length of embeddings, ids, and payloads must match.")

        # Create a list of PointStruct instances internally
        points = [
            models.PointStruct(id=ids[i], vector=embeddings[i], payload=payloads[i])
            for i in range(len(embeddings))
        ]

        return self._client.upsert(collection, points)

    def search(self, collection, query_vector, metadata={}, limit=1):
        """Search for similar vectors in a collection.

        Args:
            collection (str): Collection name.
            query_vector: Vector to search for.
            metadata (dict): Additional metadata filters.
            limit (int): Maximum number of results.

        Returns:
            list: Search results with id and score.
        """
        must = [
            models.FieldCondition(key=key, match=models.MatchValue(value=value))
            for key, value in metadata.items()
        ]

        search_params = {
            "collection_name": collection,
            "query_vector": query_vector,
            "limit": limit,
        }
        if must:
            search_params["query_filter"] = models.Filter(must=must)

        results = self._client.search(**search_params)

        return [{"id": result.id, "score": result.score} for result in results]

    def delete(self, collection: str, document_id: str):
        """Delete a point from a collection.

        Args:
            collection (str): Collection name.
            document_id (str): ID of the point to delete.

        Returns:
            API response for the delete operation.
        """
        return self._client.delete(
            collection_name=collection,
            points_selector=models.PointIdsList(points=[document_id]),
        )


def get_qdrant_client(db_url: str, db_api_key: str) -> Qdrant:
    """Create and return a Qdrant client instance.

    Args:
        db_url (str): Qdrant server URL.
        db_api_key (str): API key for authentication.

    Returns:
        Qdrant: Initialized Qdrant client wrapper.
    """
    return Qdrant(db_url, db_api_key)
