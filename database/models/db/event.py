from ..core import BaseDocument
from pydantic import Field
from typing import List, Optional
from ..embedded import SubjectIdName, FacultyIdNameCode, BatchIdNameCode, RoomIdCode
from datetime import time
from bson import ObjectId
from beanie import PydanticObjectId

class Event(BaseDocument):
    start_time: str = Field(..., description="Start time in hh:mm")
    end_time: str = Field(..., description="End time in hh:mm")
    online_links: Optional[List[str]] = Field(default=[], description="Online Links")
    description: Optional[str] = Field(None, description="Describe the event")
    batches: Optional[List[PydanticObjectId]] = Field(default=[], description="Batches associated with the event")
    faculties: Optional[List[PydanticObjectId]] = Field(default=[], description="Faculty associated with the event")
    subjects: Optional[List[PydanticObjectId]] = Field(default=[], description="Subjects associated with the event")
    rooms: Optional[List[PydanticObjectId]] = Field(default=[], description="Room Data") 
    class Settings:
        name = "Events"
        is_root = True
    class Config:
        json_encoders = {PydanticObjectId: str, ObjectId: str}
        populate_by_name = True


class RecurringEvent(Event):
    day_of_week: int = Field(..., description="Day of Week (1, 7)<==>(Monday, Sunday)")