from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional
from bson import ObjectId

class UserReferenceIdNameEmail(PydanticBaseModel):
    id: ObjectId = Field(..., alias="_id", description="User document _id")
    name: str = Field(..., description="Name")
    email: str = Field(..., description="Email")

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }