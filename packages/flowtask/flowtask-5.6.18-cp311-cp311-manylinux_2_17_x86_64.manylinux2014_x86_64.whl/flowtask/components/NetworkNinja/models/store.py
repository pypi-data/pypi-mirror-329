from typing import List, Optional, Union, Dict, Any
from datetime import datetime
from datamodel import BaseModel, Field
from slugify import slugify
from .abstract import AbstractPayload
from .organization import Organization
from .client import Client
from .region import Region
from .market import Market
from .district import District


class StoreGeography(AbstractPayload):
    """
    Store Geography Model.

    Represents a store's geographical information.

    Example:
        {
            "geoid": 479,
            "region": "Assembly - Region",
            "district": "Assembly - District",
            "market": "136",
            "company_id": 61,
            "orgid": 71,
            "client_id": 61,
            "client_name": "ASSEMBLY"
        }
    """
    geoid: int = Field(primary_key=True, required=True)
    region_id: Region = Field(alias='region')
    district_id: District = Field(alias='district')
    market_id: Market = Field(alias='market')
    company_id: int
    orgid: Organization
    client_id: Client
    client_name: str

    class Meta:
        strict = True
        as_objects = True
        name = 'stores_geographies'
        schema: str = 'nn'

    def __post_init__(self):
        super().__post_init__()
        self.client_id.client_name = self.client_name

class StoreType(AbstractPayload):
    """
    Store Type Model.

    Represents a store type in the system.

    Example:
        {
            "store_type_id": 1,
            "store_type_name": "Retail",
            "store_type_description": "Retail Store"
        }
    """
    store_type_id: int = Field(primary_key=True, required=True)
    store_type: str = Field(alias="store_type_name")
    description: str
    client_id: Client
    client_name: str

    class Meta:
        strict = True
        as_objects = True
        name = 'store_types'
        schema: str = 'nn'


class CustomStoreField(BaseModel):
    """
    Custom Field Model for Store.

    Represents a custom field for a store.

    Example:
        {
        "custom_id": 33,
        "custom_name": "Store Name",
        "custom_value": "Best Buy 4350",
        "custom_orgid": null,
        "custom_client_id": 1
    }
    """
    store_id: int
    custom_id: int = Field(primary_key=True, required=True)
    name: str = Field(alias="custom_name")
    column_name: Union[str, int]
    value: Union[str, None] = Field(alias="custom_value")
    obj_type: str = Field(alias="custom_type", default="Text")
    orgid: int = Field(alias="custom_orgid")
    client_id: str = Field(alias="custom_client_id")

    class Meta:
        name = 'stores_attributes'
        schema: str = 'nn'

    def __post_init__(self):
        self.column_name = slugify(self.name, separator="_")
        return super().__post_init__()

    def get_field(self):
        return {
            self.column_name: self.value
        }

def default_timezone(*args, **kwargs):
    return "America/New_York"


class Store(AbstractPayload):
    """
    Store Model.

    Represents a store in the system.

    Example:
        {
            "store_name": "KILMARNOCK-4350",
            "store_address": "200 Old Fair Grounds Way",
            "city": "Kilmarnock",
            "zipcode": "22482",
            "phone_number": "804-435-6149",
        }
    """
    store_id: int = Field(primary_key=True, required=True)
    store_name: str
    store_address: str
    city: str
    zipcode: str
    phone_number: Optional[str]
    email_address: str = Field(alias="emailAddress")
    store_number: Optional[str]
    store_status: bool = Field(required=False, default=True)
    latitude: float
    longitude: float
    timezone: str = Field(default=default_timezone)
    account_id: int
    country_id: str
    created_at: datetime
    updated_at: datetime
    store_type: str
    account_name: str
    visit_rule: List[str]
    visit_category: List[str]
    orgid: List[Organization] = Field(alias='orgids', default_factory=list)
    custom_fields: List[CustomStoreField] = Field(default_factory=list)
    client_id: List[Client] = Field(alias='client_ids', default_factory=list)
    client_name: List[str] = Field(alias='client_names', default_factory=list)
    market_name: Dict[str, str] = Field(required=False, alias='markets')
    region_name: Dict[str, str] = Field(required=False, alias='regions')
    district_name: Dict[str, str] = Field(required=False, alias='districts')

    class Meta:
        strict = True
        as_objects = True
        name = 'stores'
        schema: str = 'nn'

    def __post_init__(self):
        super().__post_init__()
        # if isinstance(self.store_id, self):
        #     self.store_id.store_name = self.store_name
