from typing import Optional
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry


class LanceDBConnector:
    """
    Encapsulates the connection to a LanceDB database and all the methods to interact with it.
    :param db_path: The path to the LanceDB database.
    :param collection_name: The name of the collection/table to use.
    :param embedding_provider: The embedding provider to use (e.g., 'openai', 'sentence-transformers').
    :param model_name: The name of the embedding model to use.
    :param device: The device to use for embeddings (e.g., 'cpu', 'cuda').
    """

    def __init__(
        self,
        db_path: str,
        collection_name: str,
        embedding_provider: str = "sentence-transformers",
        model_name: str = "BAAI/bge-small-en-v1.5",
        device: str = "cpu"
    ):
        self._db = lancedb.connect(db_path)
        self._collection_name = collection_name
        self._embedding_func = get_registry().get(embedding_provider).create(
            name=model_name, 
            device=device
        )
        
        # Define the schema for the table
        class TextItem(LanceModel):
            text: str = self._embedding_func.SourceField()
            vector: Vector(self._embedding_func.ndims()) = self._embedding_func.VectorField()
        
        self._schema = TextItem
        # Create or get the table
        if collection_name not in self._db.table_names():
            self._table = self._db.create_table(collection_name, schema=self._schema)
        else:
            self._table = self._db.open_table(collection_name)

    def store_memory(self, information: str):
        """
        Store a memory in the LanceDB collection.
        :param information: The information to store.
        """
        self._table.add([{"text": information}])

    def find_memories(self, query: str, limit: int = 10) -> list[str]:
        """
        Find memories in the LanceDB collection. If there are no memories found, an empty list is returned.
        :param query: The query to use for the search.
        :param limit: Maximum number of results to return.
        :return: A list of memories found.
        """
        try:
            results = self._table.search(query).limit(limit).to_pydantic(self._schema)
            return [item.text for item in results]
        except Exception:
            return []

# Example usage
connector = LanceDBConnector(
    db_path="/tmp/db",
    collection_name="memories",
    embedding_provider="sentence-transformers",
    model_name="BAAI/bge-small-en-v1.5"
)

# Store some memories
connector.store_memory("hello world")
connector.store_memory("goodbye world")

# Search for memories
results = connector.find_memories("greetings")
print(results)  # Will return similar texts