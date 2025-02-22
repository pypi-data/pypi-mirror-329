from typing import List, Optional
from datetime import datetime
from datamodel import BaseModel, Field
from .abstract import AbstractPayload
from .organization import Organization


class Role(BaseModel):
    role_id: int = Field(primary_key=True, required=True)
    role_name: str
    client_id: int = Field(alias="role_client_id")
    visit_id: int = Field(alias="role_visit_id")

    class Meta:
        strict = True
        as_objects = True
        name = 'roles'
        schema: str = 'nn'

class User(AbstractPayload):
    """
    User Model.

    Represents a user in the system.

    Example:
        {
            "user_id": 1,
            "username": "admin",
            "employee_number": 1234,
            "first_name": "John",
            "last_name": "Doe",
            "email": "
            "mobile_number": "123-456-7890",
            "role_id": 1,
            "role_name": "Admin",
            "address": "1234 Elm St",
            "city": "Springfield",
            "state_code": "IL",
            "zipcode": "62704",
            "latitude": 39.781721,
            "longitude": -89.650148,
        }
    """
    user_id: int = Field(primary_key=True, required=True)
    username: str = Field(required=True)
    employee_number: int
    first_name: str
    last_name: str
    display_name: str
    email_address: str = Field(alias="email")
    mobile_number: str
    role_id: Role = Field(required=True)
    role_name: str
    address: str
    city: str
    state_code: str = Field(alias="state_name")
    zipcode: str
    latitude: Optional[float]
    longitude: Optional[float]
    physical_country: Optional[str]
    is_active: bool = Field(required=True, default=True)
    orgid: List[Organization]
    # hierarchy
    region_name: List[str] = Field(alias='regions')
    district_name: List[str] = Field(alias='districts')
    market_name: List[str] = Field(alias='markets')
    client_name: List[str] = Field(alias='client_names')
    client_id: List[int] = Field(alias='client_ids')

    class Meta:
        strict = True
        as_objects = True
        name = 'users'
        schema: str = 'nn'

    def __post_init__(self):
        super().__post_init__()
        self.role_id.role_name = self.role_name
        self.display_name = f'{self.first_name} {self.last_name}'


class StaffingUser(User):
    custom_fields: List[str]
    onboarding: datetime

    class Meta:
        strict = True
        as_objects = True
        name = 'staffing_users'
        schema: str = 'nn'
