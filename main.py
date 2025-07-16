from database.dummy.bulk_inserts import bulk_inserts
from database.services.batch import get_events_with_faculty_names_for_batch, explain_events_with_faculty_names_for_batch
from database.config.config import connect_db, connect_redis
from database.services.warm_redis import warm_batch_events, warm_user_batches
from database.services.read_events_from_redis import get_user_events, benchmark_user_events
import asyncio
from bson import ObjectId
import time
from pprint import pprint

async def main():
    s = time.perf_counter()
    await connect_db()
    await connect_redis()
    await bulk_inserts()
    # await get_events_with_faculty_names_for_batch(ObjectId("68374924a346a057c731a64e"))
    await warm_batch_events()
    await warm_user_batches()
    start = time.perf_counter()
    await benchmark_user_events()
    end = time.perf_counter()
    print(f"{end - start:.6f}")
    print(f"{end - s:.6f}")


if __name__ == "__main__":
    asyncio.run(main())