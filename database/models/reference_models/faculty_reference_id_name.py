from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional
from bson import ObjectId

class FacultyReferenceIdName(PydanticBaseModel):
    id: ObjectId = Field(..., alias="_id", description="Faculty ID")
    name: str = Field(..., description="Faculty name")
    code: Optional[str] = Field(default="", description="Faculty Code")

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }