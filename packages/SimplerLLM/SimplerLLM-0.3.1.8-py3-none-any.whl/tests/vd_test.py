from SimplerLLM.vectors.vector_storage import VectorDatabase
import numpy as np
import asyncio

async def test_check_database_records():
    # Initialize the database
    db = VectorDatabase("yVdz_GgyGaI")
    record_count = await db.check_database_records("yVdz_GgyGaI")
    print(f"Number of records in yVdz_GgyGaI: {record_count}")

    await db.delete_all_collections()
    record_count = await db.check_database_records("yVdz_GgyGaI")
    print(f"Number of records in yVdz_GgyGaI: {record_count}")



# Run the test
asyncio.run(test_check_database_records())


