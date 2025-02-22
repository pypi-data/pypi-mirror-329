from datamodel import BaseModel, Field


class District(BaseModel):
    district_id: str = Field(required=False)
    district_name: str
