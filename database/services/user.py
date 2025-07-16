from database.models import User, Student, Faculty
from bson import ObjectId

def get_pipeline(user_id: ObjectId):
    pipeline = [
        {
            "$match": {
                "_id": user_id
            }
        },
        {
            "$lookup": {
                "from": "Batch",
                "localField": "in_batches",
                "foreignField": "_id",
                "as": "batches"
            }
        },
        {
            "$unwind": {
                "path": "$batches",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "faculty_events": 1,
                "batch_event_ids": "$batches.events"
            }
        },
        {
            "$project": {
                "event_ids": {
                    "$setUnion": [
                        "$faculty_events",
                        { "$ifNull": ["$batch_event_ids", []] }
                    ]
                }
            }
        },
        {
            "$lookup": {
                "from": "Events",
                "localField": "event_ids",
                "foreignField": "_id",
                "as": "all_events"
            }
        },
        {
            "$project": {
                "_id": 0,
                "all_events": 1
            }
        }
    ]
    return pipeline
