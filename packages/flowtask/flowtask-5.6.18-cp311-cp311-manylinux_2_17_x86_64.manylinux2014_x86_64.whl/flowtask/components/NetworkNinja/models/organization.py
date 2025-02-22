from typing import List, Optional, Union, Any
from datetime import datetime
from datamodel import BaseModel, Field

class Organization(BaseModel):
    orgid: int = Field(required=False)
    org_name: str
    status: bool = Field(required=True, default=True)

    class Meta:
        name: str = 'organizations'
        schema: str = 'nn'
        strict: bool = True

def create_organization(
    name: str,
    value: Any,
    target_type: Any,
    parent_data: BaseModel
) -> Organization:
    org_name = parent_data.get('org_name', None) if parent_data else None
    print('CREATE ORGANIZATION')
    args = {
        name: value,
        "org_name": org_name,
        "status": True,
    }
    return target_type(**args)

BaseModel.register_parser(Organization, create_organization, 'orgid')
