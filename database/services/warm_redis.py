from database.config.config import redis_client
from database.services.batch import get_events_with_faculty_names_for_batch
from database.models import Batch, Event, User
from beanie import PydanticObjectId, Document
from pydantic import Field, BaseModel
from typing import Optional, List
from bson import ObjectId
import json
import asyncio

class Id(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    class Config:
        json_encoders = {PydanticObjectId: str}

class IdBatch(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    in_batches: Optional[List[PydanticObjectId]] = Field(...)
    class Config:
        json_encoders = {PydanticObjectId: str}

async def warm_batch_events():
    batches = await Batch.find(projection_model=Id).to_list()
    print(f"Found {len(batches)} batches")

    semaphore = asyncio.Semaphore(10)

    async def warm_batch(batch):
        async with semaphore:
            try:
                batch_id = batch.id
                redis_key = f"batch:{str(batch_id)}:events"
                events = await get_events_with_faculty_names_for_batch(batch_id)
                events = [json.loads(event.model_dump_json()) for event in events]
                await redis_client.json().set(redis_key, "$", events)
            except Exception as e:
                print(f"Error warming batch {batch.id}: {e}")

    await asyncio.gather(*(warm_batch(batch) for batch in batches))


async def warm_user_batches():
    users = await User.find(projection_model=IdBatch).to_list()  # Adjust projection to only id and batch_ids
    print(f"Found {len(users)} users")

    semaphore = asyncio.Semaphore(10)

    async def warm_user(user):
        async with semaphore:
            try:
                user_id = user.id
                batch_ids = [str(batch_id) for batch_id in user.in_batches]  # Assuming user.batch_ids is list of ObjectId or strings
                redis_key = f"user:{user_id}:batches"
                await redis_client.json().set(redis_key, "$", batch_ids)
            except Exception as e:
                print(f"Error warming user {user.id}: {e}")

    await asyncio.gather(*(warm_user(user) for user in users))


    

