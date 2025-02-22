# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# chATLAS_Embed is free software; you can redistribute it and/or modify
# it under the terms of Apache 2.0 license; see LICENSE file for more details.
# `chATLAS_Embed/VectorStores.py`

"""A collection of VectorStores."""
import json
import math
import re
import time
from typing import List, Tuple

from sqlalchemy import bindparam
from sqlalchemy import create_engine, inspect
from sqlalchemy.sql import text
from sqlalchemy.exc import ProgrammingError
from tqdm import tqdm

from .Base import VectorStore, EmbeddingModel, Document


class PostgresParentChildVectorStore(VectorStore):
    """PostgresSQL-based vector store with pgvector extension."""

    def __init__(
        self,
        connection_string: str,
        embedding_model: EmbeddingModel,
        _update_vector_size=False,
    ):
        """PostgresSQL-based vector store initialisation.

        Once done with the vectorstore make sure to close it by `PostgresParentChildVectorStore.close()`,
        `del PostgresParentChildVectorStore` or wrapping the usage of the vectorstore in a `with`.

        :param connection_string: (str) - connection string to connect to the postgres database used. e.g. postgresql://{user}:{password}@dbod-chatlas.cern.ch:{port}/vTEST
        :param embedding_model: (EmbeddingModel) - Embedding model used to generate vector store (and used to process queries to search the db)
        :param _update_vector_size: (bool) - Debugging parameter for using embedding models with different vector sizes - **NOTE** if set to true and used with a different embeding model will drop previously made embeddings
        """
        super().__init__()
        self.connection_string = connection_string
        self.embedding_model = embedding_model
        self._ensure_database_exists()
        self.engine = create_engine(self.connection_string)
        self.vector_length = embedding_model.vector_size
        self._update_vector_size = _update_vector_size
        self._init_db()

    def _extract_db_info(self):
        """Extract database name and connection info from connection string."""
        pattern = r"(?P<base>postgresql://[^/]+)/(?P<dbname>[^?]+)"
        match = re.match(pattern, self.connection_string)
        if not match:
            raise ValueError("Invalid connection string format")

        return {
            "base_connection": match.group("base"),
            "database_name": match.group("dbname"),
        }

    def _ensure_database_exists(self):
        """Create database if it doesn't exist."""
        db_info = self._extract_db_info()
        base_connection = db_info["base_connection"]
        database_name = db_info["database_name"]

        # Connect to default 'postgres' database to create new database
        default_connection = f"{base_connection}/postgres"
        temp_engine = create_engine(default_connection)

        try:
            with temp_engine.connect() as conn:
                # Start transaction
                with conn.begin():
                    # Check if database exists
                    result = conn.execute(
                        text(f"SELECT 1 FROM pg_database WHERE datname = :dbname"),
                        {"dbname": database_name},
                    ).scalar()

                    if not result:
                        # Terminate existing connections
                        conn.execute(
                            text(
                                f"""
                                SELECT pg_terminate_backend(pid)
                                FROM pg_stat_activity
                                WHERE datname = :dbname
                            """
                            ),
                            {"dbname": database_name},
                        )
                        # Create database
                        # Note: We need to commit the transaction before creating the database
                        conn.execute(text(f"COMMIT"))
                        conn.execute(text(f'CREATE DATABASE "{database_name}"'))

        except Exception as e:
            print(f"Failed to create database: {str(e)}")
            raise
        finally:
            temp_engine.dispose()

    def _init_db(self):
        """Initialize database schema and extensions."""
        try:
            with self.engine.connect() as conn:
                # Create extension if not exists
                try:
                    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                except Exception as e:
                    raise Exception(
                        "Failed to create vector extension. "
                        "Please ensure you have superuser privileges and pgvector is installed: "
                        + str(e)
                    )

                # Create documents table if not exists
                conn.execute(
                    text(
                        """
                    CREATE TABLE IF NOT EXISTS documents (
                        id TEXT PRIMARY KEY,
                        page_content TEXT,
                        metadata JSONB,
                        parent_id TEXT
                    )
                """
                    )
                )

                # Check if the embeddings table exists
                result = conn.execute(
                    text(
                        """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'embeddings'
                    )
                """
                    )
                )
                table_exists = result.scalar()

                if table_exists:
                    # Check the existing dimension of the embeddings column
                    conn.execute(
                        text(
                            """
                            ALTER TABLE embeddings
                            DROP CONSTRAINT IF EXISTS embeddings_document_id_fkey
                            """
                        )
                    )

                    # Add the new constraint with CASCADE
                    conn.execute(
                        text(
                            """
                            ALTER TABLE embeddings
                            ADD CONSTRAINT embeddings_document_id_fkey
                            FOREIGN KEY (document_id)
                            REFERENCES documents(id)
                            ON DELETE CASCADE
                            """
                        )
                    )
                    result = conn.execute(
                        text(
                            """
                        SELECT pg_catalog.format_type(a.atttypid, a.atttypmod) AS type
                        FROM pg_catalog.pg_attribute a
                        WHERE a.attname = 'embedding' AND a.attrelid = (
                            SELECT c.oid FROM pg_catalog.pg_class c
                            WHERE c.relname = 'embeddings' AND c.relkind = 'r'
                        )
                    """
                        )
                    )
                    row = result.fetchone()

                    if row:
                        current_vector_type = row[0]  # Format: "vector(384)"
                        current_dimension = int(
                            current_vector_type.split("(")[1].rstrip(")")
                        )

                        # If dimensions differ, update the table schema
                        if current_dimension == self.vector_length:
                            pass
                        elif (
                            current_dimension != self.vector_length
                            and self._update_vector_size
                        ):
                            conn.execute(
                                text(
                                    "ALTER TABLE embeddings DROP COLUMN IF EXISTS embedding"
                                )
                            )
                            conn.execute(
                                text(
                                    f"ALTER TABLE embeddings ADD COLUMN embedding vector({self.vector_length})"
                                )
                            )
                        else:
                            raise ValueError(
                                """
                            The embedding model output vector size used does not match the one used to create the db.
                             Set `_update_vector_size` to True if trying to update the vectors in the database"""
                            )
                    else:
                        # If the embedding column doesn't exist, create it
                        conn.execute(
                            text(
                                f"ALTER TABLE embeddings ADD COLUMN embedding vector({self.vector_length})"
                            )
                        )
                else:
                    # Create the embeddings table if it doesn't exist
                    conn.execute(
                        text(
                            f"""
                            CREATE TABLE embeddings (
                                id TEXT PRIMARY KEY,
                                document_id TEXT REFERENCES documents(id) ON DELETE CASCADE,
                                embedding vector({self.vector_length})
                            )
                        """
                        )
                    )

                # Create the vector index
                conn.execute(
                    text(
                        """
                    CREATE INDEX IF NOT EXISTS embeddings_vector_idx
                    ON embeddings
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 250)
                """
                    )
                )

                # Set ivfflat probes
                conn.execute(text("SET ivfflat.probes = 32"))

                conn.commit()

        except Exception as e:
            print(f"Failed to initialize database schema: {str(e)}")
            raise

    def close(self):
        """Explicitly close and dispose of database connections"""
        if hasattr(self, "engine"):
            self.engine.dispose()

    def __del__(self):
        """Ensure connections are closed when object is deleted"""
        self.close()

    def __enter__(self):
        """Support context manager protocol"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatically close connections when exiting context"""
        self.close()

    def add_documents(
        self, parent_docs: List[Document], child_docs: List[Document]
    ) -> None:
        """Add parent documents and child documents to the database."""
        with self.engine.connect() as conn:
            with conn.begin():
                # Insert parent documents
                for parent_doc in tqdm(parent_docs, "Adding Parent Documents"):
                    conn.execute(
                        text(
                            """
                            INSERT INTO documents (id, page_content, metadata, parent_id)
                            VALUES (:id, :page_content, :metadata, NULL)
                            ON CONFLICT (id) DO NOTHING
                        """
                        ),
                        {
                            "id": parent_doc.id,
                            "page_content": parent_doc.page_content,
                            "metadata": json.dumps(parent_doc.metadata),
                        },
                    )

                # Insert child documents and embeddings
                for child_doc in tqdm(child_docs, "Adding Child Documents"):
                    conn.execute(
                        text(
                            """
                            INSERT INTO documents (id, page_content, metadata, parent_id)
                            VALUES (:id, :page_content, :metadata, :parent_id)
                            ON CONFLICT (id) DO NOTHING
                        """
                        ),
                        {
                            "id": child_doc.id,
                            "page_content": child_doc.page_content,
                            "metadata": json.dumps(child_doc.metadata),
                            "parent_id": child_doc.parent_id,
                        },
                    )

        # Prepare all child document contents for embedding
        documents_to_embed = [(doc.id, doc.page_content) for doc in child_docs]

        # Generate embeddings in batches
        embeddings = self.embedding_model.embed(
            [doc_content for _, doc_content in documents_to_embed],
            show_progress_bar=True,
        )
        print("Adding documents to db...")
        t0 = time.time()
        # Insert embeddings into the database
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(
                    text(
                        """
                        INSERT INTO embeddings (id, document_id, embedding)
                        VALUES (:id, :doc_id, :embedding)
                        ON CONFLICT (id) DO UPDATE
                        SET embedding = EXCLUDED.embedding
                    """
                    ),
                    [
                        {"id": doc_id, "doc_id": doc_id, "embedding": embedding}
                        for (doc_id, _), embedding in zip(
                            documents_to_embed, embeddings
                        )
                    ],
                )
        print(f"Total time adding embeddings to db: {time.time() - t0:.4f}s")

        self.optimize_index_for_size()

    def delete(self, document_ids: List[str] = None, document_name: str = None) -> None:
        """Delete items from the DB. Either by thier ID or by their name (not
        both at the same time)

        **NOTE** can currently only delete one document by name at a time, no options to delete before a certain date etc. There are all WIPs!

        :param document_ids: (List[str]) - list of document ids to delete
        :param document_name: (str) - Document name to delete
        """
        if document_ids is None and document_name is None:
            raise ValueError(
                "You must provide either document_ids or document_name to delete."
            )

        with self.engine.connect() as conn:
            with conn.begin():
                if document_name:
                    # Find all parent and child document IDs with the specified name in metadata
                    document_ids = (
                        conn.execute(
                            text(
                                """
                            SELECT id FROM documents
                            WHERE metadata::jsonb->>'name' = :doc_name
                        """
                            ),
                            {"doc_name": document_name},
                        )
                        .scalars()
                        .all()
                    )

                if not document_ids:
                    print(f"No documents found for the given criteria.")
                    return

                # Delete embeddings and documents
                conn.execute(
                    text(
                        """
                        DELETE FROM documents WHERE id = ANY(:doc_ids) OR parent_id = ANY(:doc_ids);
                    """
                    ),
                    {"doc_ids": document_ids},
                )
                print(f"Deleted {len(document_ids)} documents and their embeddings.")

    def update_index_lists(self, new_lists: int = 1200, new_probes: int = 50):
        """Update the IVFFlat index with a new number of lists. This will drop
        the old index and create a new one.

        :param new_lists: (int) - number of lists to use in new indexing
        :param new_probes: (int) - number of probes to use when searching embeddings
        """
        with self.engine.connect() as conn:
            with conn.begin():
                # parallel processing
                conn.execute(
                    text(
                        """
                    SET maintenance_work_mem = '1.8GB';
                    SET max_parallel_workers_per_gather = 8;
                """
                    )
                )
                # Drop the old index
                conn.execute(
                    text(
                        """
                    DROP INDEX IF EXISTS embeddings_vector_idx;
                """
                    )
                )

                # Create new index with updated lists parameter
                conn.execute(
                    text(
                        f"""
                    CREATE INDEX embeddings_vector_idx
                    ON embeddings
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = {new_lists});
                """
                    )
                )

                conn.execute(text(f"""SET ivfflat.probes = {new_probes};"""))

    def optimize_index_for_size(self):
        """Calculate and set optimal number of lists based on embedding count.

        **NOTE**: Optimal is taken very loosely here!
        """
        with self.engine.connect() as conn:
            # Get count of embeddings
            count = conn.execute(text("SELECT COUNT(*) FROM embeddings")).scalar()

            # Calculate optimal lists (roughly sqrt of count - with an extra bit added for RAG)
            optimal_lists = int(math.sqrt(count) + 0.05 * math.sqrt(count))

            optimal_probes = max(
                4, int(optimal_lists * 0.14)
            )  # optimal bins roughly 10% of number of lists

            # For very large datasets, cap at a reasonable maximum
            optimal_lists = min(max(optimal_lists, 4), 2000)

        print(
            f"Updating index for {count} embeddings with {optimal_lists} lists and {optimal_probes} probes"
        )
        self.update_index_lists(optimal_lists, optimal_probes)

    def drop_database(self) -> None:
        """
        WARNING: USE WITH CARE - WILL DELETE EVERYTHING
        **CURRENTLY BROKEN**
        (in this db name e.g. vectordb hopefully not the entirety of the server)
        Drop the entire database and its contents. Useful for testing with a new embedding model or splitter.
        """
        db_info = self._extract_db_info()
        base_connection = db_info["base_connection"]
        database_name = db_info["database_name"]

        # Connect to the default 'postgres' database
        default_connection = f"{base_connection}/postgres"
        temp_engine = create_engine(default_connection)

        try:
            with temp_engine.connect() as conn:
                # Terminate all connections to the database
                with conn.begin():
                    conn.execute(
                        text(
                            f"""
                            SELECT pg_terminate_backend(pid)
                            FROM pg_stat_activity
                            WHERE datname = :dbname;
                        """
                        ),
                        {"dbname": database_name},
                    )

                    # Drop the database
                    conn.execute(text(f'DROP DATABASE IF EXISTS "{database_name}"'))

            print(f"Database '{database_name}' has been successfully dropped.")

        except Exception as e:
            raise Exception(f"Failed to drop database: {str(e)}")

        finally:
            temp_engine.dispose()

    def clear_database(self) -> None:
        """
        WARNING: USE WITH CARE - WILL CLEAR ALL TABLE CONTENTS
        Empties all tables in the database while preserving the database structure.
        """
        try:
            with self.engine.connect() as conn:
                inspector = inspect(self.engine)
                tables = inspector.get_table_names()

                with conn.begin():
                    for table in tables:
                        conn.execute(
                            text(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE')
                        )

                print("All tables have been cleared successfully.")
        except Exception as e:
            raise Exception(f"Failed to clear the database: {str(e)}")

    def test_connection(self):
        """Test the connection to the PostgreSQL database.

        Returns:
            True if connection succeeded
            False if connection failed
        """
        try:
            with create_engine(self.connection_string).connect() as conn:
                # Execute a simple query to check the connection
                result = conn.execute(text("SELECT 1")).scalar()
                if result == 1:
                    return True  # Connection is good
                return False  # Connection failed unexpectedly
        except Exception as e:
            # Log the error or raise it if necessary
            print(f"Connection test failed: {str(e)}")
            return False

    def search(
        self,
        query: str,
        k: int = 4,
        metadata_filters: dict = None,
        date_filter: str = "01-01-2005",
    ) -> List[Tuple[Document, Document, float]]:
        """
        Search for similar documents using cosine similarity, with optional
        metadata and date filtering.

        :param query: The search query.
        :type query: str
        :param k: Number of results to return.
        :type k: int
        :param metadata_filters: Dictionary of metadata filters where keys are metadata fields
            and values can be either strings (for exact match) or lists (for containment).
        :type metadata_filters: dict[str, str | list]
        :param date_filter: A date string ('dd-mm-YYYY') to filter 'last_modification' for newer entries.
        :type date_filter: str

        :returns: List of k (child_doc, parent_doc, similarity_score) tuples.
        :rtype: List[Tuple[Document, Document, float]]
        """
        # Generate embedding for the query
        query_embedding = self.embedding_model.embed(query)

        # Build metadata filter conditions using bind parameters for safety
        metadata_filter_conditions = []
        filter_params = {}

        if metadata_filters:
            for idx, (key, value) in enumerate(metadata_filters.items()):
                param_key = f"key_{idx}"
                param_value = f"value_{idx}"

                # Handle different types of metadata values
                if isinstance(value, list):
                    # For list values, check if the metadata field contains ANY of the filter values
                    metadata_filter_conditions.append(
                        f"CAST(d_child.metadata::jsonb->:key_{idx} AS jsonb) ?| :value_{idx}"
                    )
                else:
                    # For string values, use exact match
                    metadata_filter_conditions.append(
                        f"d_child.metadata->>:key_{idx} = :value_{idx}"
                    )

                filter_params[param_key] = key
                filter_params[param_value] = (
                    value if isinstance(value, list) else str(value)
                )

        # Add date filter condition
        if date_filter:
            metadata_filter_conditions.append(
                "d_child.metadata->>'last_modification' > :date_filter"
            )
            filter_params["date_filter"] = date_filter

        # Combine all filter conditions
        metadata_filter_clause = " AND ".join(metadata_filter_conditions)

        # Final SQL query with metadata filtering
        query_text = f"""
                WITH similarity_results AS (
                    SELECT
                        e.document_id,
                        1 - (e.embedding <=> CAST(:query_embedding AS vector)) AS similarity
                    FROM embeddings e
                    JOIN documents d_child ON e.document_id = d_child.id
                    {f"WHERE {metadata_filter_clause}" if metadata_filter_conditions else ""}
                    ORDER BY e.embedding <=> CAST(:query_embedding AS vector)
                    LIMIT :k
                )
                SELECT
                    -- Child document fields
                    d_child.id AS child_id,
                    d_child.page_content AS child_content,
                    d_child.metadata AS child_metadata,
                    d_child.parent_id,
                    -- Parent document fields
                    d_parent.id AS parent_id,
                    d_parent.page_content AS parent_content,
                    d_parent.metadata AS parent_metadata,
                    -- Similarity score
                    sr.similarity
                FROM similarity_results sr
                JOIN documents d_child ON sr.document_id = d_child.id
                JOIN documents d_parent ON d_child.parent_id = d_parent.id
                ORDER BY sr.similarity DESC
            """
        try:
            with self.engine.connect() as conn:
                # Execute the query with parameters
                results = conn.execute(
                    text(query_text).bindparams(
                        query_embedding=bindparam("query_embedding"),
                        k=bindparam("k"),
                        **{key: bindparam(key) for key in filter_params.keys()},
                    ),
                    {
                        "query_embedding": query_embedding,
                        "k": (k + 10) if filter_params else k,
                        **filter_params,
                    },
                )  # Return extra 5 docs if there are filter params

                # Process results and construct Document objects
                search_results = []
                for count, row in enumerate(results):
                    if count >= k:
                        break
                    # Create child document
                    child_doc = Document(
                        id=row.child_id,
                        page_content=row.child_content,
                        metadata=row.child_metadata if row.child_metadata else {},
                        parent_id=row.parent_id,
                    )

                    # Create parent document
                    parent_doc = Document(
                        id=row.parent_id,
                        page_content=row.parent_content,
                        metadata=row.parent_metadata if row.parent_metadata else {},
                        parent_id=None,
                    )

                    # Add tuple of (child_doc, parent_doc, similarity_score) to results
                    search_results.append(
                        (child_doc, parent_doc, float(row.similarity))
                    )

                return search_results
        except Exception as e:
            print(f"Error in search: {e}")
            raise
