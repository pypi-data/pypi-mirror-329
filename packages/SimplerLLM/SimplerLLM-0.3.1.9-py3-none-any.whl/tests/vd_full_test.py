import asyncio
import numpy as np
from SimplerLLM.vectors.vector_storage import VectorDatabase, SerializationFormat

async def test_vector_database():
    # Initialize the database
    db = VectorDatabase("test_db", use_semantic_connections=True)

    # Test adding vectors
    print("Testing add_vector...")
    id1 = db.add_vector("Test vector 1", np.array([1, 2, 3]), {"tag": "test1"})
    id2 = db.add_vector("Test vector 2", np.array([4, 5, 6]), {"tag": "test2"})
    id3 = db.add_vector("Test vector 3", np.array([7, 8, 9]), {"tag": "test3"})

    # Test adding vectors in batch
    print("Testing add_vectors_batch...")
    batch_records = [
        {"text": "Batch 1", "embedding": [1, 1, 1], "metadata": {"tag": "batch1"}},
        {"text": "Batch 2", "embedding": [2, 2, 2], "metadata": {"tag": "batch2"}},
    ]
    db.add_vectors_batch(batch_records)

    # Test saving and loading
    print("Testing save_to_disk and load_from_disk...")
    await db.save_to_disk(SerializationFormat.BINARY)
    new_db = VectorDatabase("test_db.pkl", use_semantic_connections=True)
    await new_db.load_from_disk(SerializationFormat.BINARY)

    # Test updating a vector
    print("Testing update_vector...")
    db.update_vector(id1, {"text": "Updated vector 1", "embedding": [10, 11, 12], "tag": "updated"})

    # Test deleting a vector
    print("Testing delete_vector...")
    db.delete_vector(id2)

    # Test similarity search
    print("Testing top_cosine_similarity...")
    similar_vectors = db.top_cosine_similarity(np.array([1, 1, 1]), top_n=2)
    print(f"Top 2 similar vectors: {similar_vectors}")

    # Test semantic search
    print("Testing semantic_search...")
    semantic_results = db.semantic_search(np.array([1, 1, 1]), top_k=2, depth=1)
    print(f"Semantic search results: {semantic_results}")

    # Test query by metadata
    print("Testing query_by_metadata...")
    metadata_results = db.query_by_metadata({"tag": "test3"})
    print(f"Query by metadata results: {metadata_results}")

    # Test get by ID
    print("Testing get_by_id...")
    vector_by_id = db.get_by_id(id3)
    print(f"Vector retrieved by ID: {vector_by_id}")

    # Test connected chunks
    print("Testing get_connected_chunks...")
    connected_chunks = db.get_connected_chunks(id3, depth=1)
    print(f"Connected chunks: {connected_chunks}")

    # Test database record count
    print("Testing check_database_records...")
    record_count = db.check_database_records()
    print(f"Number of records in the database: {record_count}")

    # Test image-related functions
    print("Testing image-related functions...")
    image_id = db.add_image_embedding("image1.jpg", np.array([1, 2, 3]), {"type": "image"})
    similar_images = db.get_similar_images(np.array([1, 2, 3]), top_k=2)
    print(f"Similar images: {similar_images}")

    image_semantic_results = db.image_semantic_search(np.array([1, 2, 3]), top_k=2, depth=1)
    print(f"Image semantic search results: {image_semantic_results}")

    # Test clearing the database
    #print("Testing clear_database...")
    #db.clear_database()
    record_count_after_clear = db.check_database_records()
    print(f"Number of records after clearing: {record_count_after_clear}")

    print("All tests completed.")

if __name__ == "__main__":
    asyncio.run(test_vector_database())