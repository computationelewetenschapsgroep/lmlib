from pydantic import BaseModel, field_validator
from datetime import datetime


class ActivityModel(BaseModel):
    activity_id: str
    activity_name: str
    activity_start_date: datetime
    activity_end_date: datetime
    activity_cost: float = 0


# PUT Request model for /v1/pt/activities/{activity_id}
class ActivityPutRequest(ActivityModel):
    @field_validator('activity_end_date')
    def validate_activity_dates(cls, v, values):
        start_date = values.get('activity_start_date')
        if start_date and v < start_date:
            raise ValueError("Activity end date must be after the start date.")
        return v


# Response model for PUT /v1/pt/activities/{activity_id}
class ActivityPutResponse(BaseModel):
    twin_id: str


# GET Request model for /v1/pt/activities/{activity_id}
class ActivityGetRequest(BaseModel):
    activity_id: str


# GET Response model for /v1/pt/activities/{activity_id}
class ActivityGetResponse(ActivityModel):
    pass