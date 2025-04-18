from ..base_model import BaseModel
from pydantic import Field
from beanie import Indexed, Link, UnionDoc
from typing import List, Optional, TYPE_CHECKING, Annotated
from ..reference_models import SubjectReferenceIdName, FacultyReferenceIdNameCode, BatchReferenceIdNameCode, RoomReferenceIdCode

if TYPE_CHECKING:
    from ..batch.batch import Batch
    from ..user.base_user import User

class Event(BaseModel):
    start_time: str = Field(..., description="Start time in hh:mm")
    end_time: str = Field(..., description="End time in hh:mm")
    online_links: Optional[List[str]] = Field(default=[], description="Online Links")
    description: Optional[str] = Field(None, description="Describe the event")
    batches: Optional[List[BatchReferenceIdNameCode]] = Field(default=[], description="Batches associated with the event")
    faculties: Optional[List[FacultyReferenceIdNameCode]] = Field(default=[], description="Faculty associated with the event")
    subjects: Optional[List[SubjectReferenceIdName]] = Field(default=[], description="Subjects associated with the event")
    rooms: Optional[List[RoomReferenceIdCode]] = Field(default=[], description="Room Data") 
    class Settings:
        name = "Events"
        is_root = True

from ..batch.batch import Batch
from ..user.base_user import User

# TODO Clean up unused imports

Event.model_rebuild()


# TODO Figure out UnionDoc