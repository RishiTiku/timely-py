from ..core import BaseDocument
from pydantic import Field
from beanie import Indexed, Link
from typing import List, Optional, TYPE_CHECKING
from ..embedded import EventId
from bson import ObjectId

class Subject(BaseDocument):
    name: str = Field(..., description="Subject name")
    code: str = Field(..., description="Subject code")
    events: Optional[List[EventId]] = Field(default=[], description="Events associated with the subject")

    class Settings:
        name = "Subjects"
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
