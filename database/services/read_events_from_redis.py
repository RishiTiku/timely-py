import json
import asyncio
from database.config.config import redis_client
import time
import csv

async def get_user_events(user_id: str):
    try:
        batch_ids_json = await redis_client.json().get(f"user:{user_id}:batches", "$")
        if not batch_ids_json:
            print(f"No batches found in Redis for user {user_id}")
            return []
        batch_ids = batch_ids_json[0] if isinstance(batch_ids_json, list) else batch_ids_json

        async def fetch_events_for_batch(batch_id):
            redis_key = f"batch:{batch_id}:events"
            events_json = await redis_client.json().get(redis_key, "$")
            if events_json:
                return events_json[0] if isinstance(events_json, list) else events_json
            return []

        all_events_lists = await asyncio.gather(*(fetch_events_for_batch(bid) for bid in batch_ids))
        all_events = [event for sublist in all_events_lists for event in sublist]
        return all_events, len(batch_ids)
    except Exception as e:
        print(f"Error fetching events for user {user_id}: {e}")
        return []

async def benchmark_user_events():
    user_keys = await redis_client.keys("user:*:batches")
    print(f"Found {len(user_keys)} users in Redis")

    # Open CSV file once in write mode
    with open("user_events_benchmark1.csv", mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["user_id", "run", "time_ms", "event_count", "batches_count"])

        for user_key in user_keys:
            user_key = user_key.decode() if isinstance(user_key, bytes) else user_key
            user_id = user_key.split(":")[1]
            # print(f"\nBenchmarking user {user_id}")

            for i in range(10):
                start = time.perf_counter()
                events, batches = await get_user_events(user_id)
                elapsed_ms = (time.perf_counter() - start) * 1000
                event_count = len(events)
                # print(f"  Run {i+1}: {elapsed_ms:.3f} ms, {event_count} events")

                csv_writer.writerow([user_id, i+1, f"{elapsed_ms:.3f}", event_count, batches])