from datamodel import BaseModel, Field


class AbstractPayload(BaseModel):
    """Abstract Payload Model.

    Common fields implemented by any Object in NetworkNinja Payloads.
    """
    client: str
    client_id: int
    orgid: int
    payload_time: int
    status: bool = Field(required=False, default=True)
    created_by: int
    updated_by: int
