from datamodel import BaseModel, Field


class Market(BaseModel):
    market_id: str = Field(required=False)
    market_name: str
