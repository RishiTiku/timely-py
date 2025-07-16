from beanie import PydanticObjectId
from database.models import Batch, Event  # Adjust your imports
import time
from typing import List
def get_pipeline(batch_id: PydanticObjectId):
    pipeline = [
            {"$match": {"_id": batch_id}},
            {"$lookup": {
                "from": "Events",
                "localField": "events",  # Batch.events is list of event IDs
                "foreignField": "_id",
                "as": "event_docs"
            }},
            {"$unwind": "$event_docs"},
            {"$lookup": {
                "from": "Users",
                "localField": "event_docs.faculties",
                "foreignField": "_id",
                "as": "event_docs.faculty_docs"
            }},
            {"$addFields": {
                "event_docs.faculty_names": {
                    "$map": {
                        "input": "$event_docs.faculty_docs",
                        "as": "faculty",
                        "in": "$$faculty.name"
                    }
                }
            }},
            {"$project": {
                "event_docs.faculty_docs": 0
            }},
            # Use $replaceRoot to output event_docs fields as top-level doc in the pipeline
            {"$replaceRoot": {"newRoot": "$event_docs"}}
        ]
    return pipeline

async def get_events_with_faculty_names_for_batch(batch_id: PydanticObjectId):
    events = await Batch.get_motor_collection().aggregate(get_pipeline(batch_id)).to_list()
    events = [Event(**e) for e in events]
    return events

async def explain_events_with_faculty_names_for_batch(batch_id: PydanticObjectId):
    collection = Batch.get_motor_collection()
    command = {
        "explain": {
            "aggregate": collection.name,
            "pipeline": get_pipeline(batch_id),
            "cursor": {}
        },
        "verbosity": "executionStats"
    }
    start = time.perf_counter()
    explain_plan = await collection.database.command(command)
    end = time.perf_counter()
    print(f"{end-start:.6f}")
    # return explain_plan