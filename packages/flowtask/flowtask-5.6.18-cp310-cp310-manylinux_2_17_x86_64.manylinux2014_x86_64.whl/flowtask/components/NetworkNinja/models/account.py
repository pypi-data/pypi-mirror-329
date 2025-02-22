from datamodel import Field
from .abstract import AbstractPayload


class Account(AbstractPayload):
    account_id: int = Field(primary_key=True, required=True)
    account_name: str
    retailer: str
    retailer_id: str

    class Meta:
        strict = True
        as_objects = True
        name = 'accounts'
        schema: str = 'nn'

    def __post_init__(self):
        super().__post_init__()
        self.retailer_id = self.account_id
