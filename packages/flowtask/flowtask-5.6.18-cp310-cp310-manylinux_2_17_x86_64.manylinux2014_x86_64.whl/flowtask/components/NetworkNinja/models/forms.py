from typing import List, Optional, Union
from datetime import datetime
from datamodel import BaseModel, Field
from .abstract import AbstractPayload
from .organization import Organization
from .client import Client
from .store import CustomStoreField, Store
from .user import User
from .account import Account


class Condition(BaseModel):
    """
    Defines a Condition, a condition for a Logic Group.
    Example:
        {
            "condition_id": 1835,
            "condition_logic": "EQUALS",
            "condition_comparison_value": "Regular",
            "condition_question_reference_id": 48,
            "condition_option_id": 4308
        }
    """
    condition_id: int = Field(primary_key=True, required=True)
    condition_logic: str = Field(required=True)
    condition_comparison_value: str = Field(required=True)
    condition_question_reference_id: str
    condition_option_id: str


class Validation(BaseModel):
    """
    Defines a Validation, a validation rule for a question.
    Example:
        {
            "validation_id": 43,
            "validation_type": "responseRequired",
            "validation_logic": null,
            "validation_comparison_value": null,
            "validation_question_reference_id": null
        }
    """
    validation_id: int = Field(primary_key=True, required=True)
    validation_type: str = Field(required=True)
    validation_logic: str
    validation_comparison_value: str
    validation_question_reference_id: str
    condition_option_id: str


class LogicGroup(BaseModel):
    """
    Defines a Logic Group, a group of questions in a Form.
    Example:
        {
            "logic_group_id": 1706,
            "conditions": [
                {
                    "condition_id": 1835,
                    "condition_logic": "EQUALS",
                    "condition_comparison_value": "Regular",
                    "condition_question_reference_id": 48,
                    "condition_option_id": 4308
                }
            ]
        }
    """
    logic_group_id: int = Field(primary_key=True, required=True)
    conditions: List[Condition]


class Question(BaseModel):
    """
    Defines a Question, a single question in a Form.
    Example:
        {
            "question_id": 48,
            "question_column_name": "8501",
            "question_description": "Purpose of Visit",
            "question_logic_groups": [],
            "validations": [
                {
                    "validation_id": 43,
                    "validation_type": "responseRequired",
                    "validation_logic": null,
                    "validation_comparison_value": null,
                    "validation_question_reference_id": null
                }
            ]
        }
    """
    question_id: int = Field(primary_key=True, required=True)
    question_column_name: Union[str, int] = Field(required=True)
    question_description: str = Field(required=True)
    question_logic_groups: List[LogicGroup]
    validations: List[Validation]

class QuestionBlock(BaseModel):
    """
    Defines a Question Block, a collection of questions in a Form.

    Example:
        {
            "question_block_id": 9,
            "question_block_type": "simple",
            "question_block_logic_groups": [],
            "questions": []
        }
    """
    block_id: int = Field(primary_key=True, required=True, alias="question_block_id")
    block_type: str = Field(alias="question_block_type")
    block_logic_groups: List[dict] = Field(alias="question_block_logic_groups")
    questions: List[dict]

class FormDefinition(AbstractPayload):
    """
    Defines a Form (recap) definition.
    """
    formid: int = Field(primary_key=True, required=True)
    form_name: str
    description: str = Field(alias='form_description')
    active: bool = Field(default=True)
    is_store_stamp: bool = Field(default=True)
    created_on: datetime
    updated_on: datetime
    client_id: Client
    client_name: str
    orgid: Organization
    org_name: str
    question_blocks: Optional[List[QuestionBlock]] = Field(default_factory=list)

    class Meta:
        strict = True
        as_objects = True
        name = 'forms'
        schema: str = 'nn'

    def __post_init__(self):
        super().__post_init__()
        self.orgid.org_name = self.org_name


class Form(AbstractPayload):
    """
    Reference to a Form:
    """
    formid: int = Field(primary_key=True, required=True)
    form_name: str
    active: bool = Field(default=True)
    client_id: Client
    client_name: str
    orgid: Organization
    org_name: str

    class Meta:
        strict = True
        as_objects = True
        name = 'forms'
        schema: str = 'nn'

    def __post_init__(self):
        super().__post_init__()
        # TODO: fixing creation of Objects
        # self.orgid.org_name = self.org_name
        # self.client_id.client_name = self.client_name

class FormMetadata(AbstractPayload):
    """
    Defines a Form Metadata, a single question from a Form.

    Example:
        {
            "column_name": "8452",
            "description": "Please provide a photo of the starting odometer reading",
            "is_active": true,
            "data_type": "FIELD_IMAGE_UPLOAD",
            "formid": 1,
            "form_name": "Territory Manager Visit Form TEST",
            "client_id": 59,
            "client_name": "TRENDMICRO",
            "orgid": 77
        }
    """
    # Column ID is not returned by Form Metadata payload but Form Data.
    column_id: str  # = Field(primary_key=True, required=True)
    column_name: Union[str, int] = Field(primary_key=True, required=True)
    data_type: str = Field(required=True, alias='data_type')
    formid: Form = Field(required=True)
    form_name: str
    is_active: bool = Field(required=True, default=True)
    client_id: Client = Field(required=True)
    client_name: str
    orgid: Organization = Field(required=True)

    class Meta:
        strict = True
        as_objects = True
        name = 'forms_metadata'
        schema: str = 'nn'

    def __post_init__(self):
        super().__post_init__()
        self.formid.form_name = self.form_name
        self.client_id.client_name = self.client_name


class FormResponse(BaseModel):
    """
    Defines a Form Response, a response to a Form.

    Example:
        {
            "column_name": 8550,
            "data": "Arturo",
            "question_shown_to_user": true,
            "column_id": "150698"
        }
    """
    column_name: FormMetadata = Field(primary_key=True, required=True)
    data: str
    question_shown_to_user: bool = Field(default=True)
    column_id: str

    def __post_init__(self):
        super().__post_init__()
        self.column_name.column_id = self.column_id


class FormData(AbstractPayload):
    """
    Defines a Form Data, a collection of responses to a Form.

    Example:
        {
            "form_data_id": 1,
            "formid": 1,
            "client_id": 59,
            "orgid": 77,
            "store_id": 1,
            "store_name": "Best Buy 4350",
            "user_id": 1,
            "user_name": "Arturo",
            "created_at": "2025-02-01T00:00:00-06:00",
            "updated_at": "2025-02-01T00:00:00-06:00",
            "form_responses": [
                {
                    "column_name": "8550",
                    "data": "Arturo",
                    "question_shown_to_user": true,
                    "column_id": "150698"
                }
            ]
        }
    """
    form_id: int = Field(primary_key=True, required=True)
    formid: Form = Field(required=True)
    version: str
    creation_timestamp: Optional[datetime]
    start_lat: Optional[float]
    start_lon: Optional[float]
    end_lat: Optional[float]
    end_lon: Optional[float]
    visit_timestamp: Optional[datetime]
    updated_timestamp: Optional[datetime]
    time_in_local: str
    time_in: datetime
    time_out_local: str
    time_out: datetime
    device_model: str
    visitor_id: int
    visitor_username: str
    visitor_name: str
    visitor_email: str
    visitor_mobile_number: str
    visitor: User
    position_id: str  # TODO: validate position ID
    store_visits_category: int
    visit_status: str
    ad_hoc: bool = Field(required=True, default=False)
    visitor_role: str
    account_id: Account
    account_name: str
    retailer: str
    store_id: Store
    store_name: str
    store_type_id: int
    store_type_name: str
    store_timezone: str
    store_is_active: bool = Field(default=True)
    # hierarchy:
    store_market_id: int
    store_market_name: str
    store_city: str
    store_zipcode: str
    region_id: int
    region_name: str
    district_id: int
    district_name: str
    market_id: int
    market_name: str
    client_id: Client = Field(required=True)
    client_name: str
    orgid: Organization = Field(required=True)
    field_responses: List[FormResponse]
    store_custom_fields: List[CustomStoreField]
    manager_role: str

    class Meta:
        strict = True
        as_objects = True
        name = 'form_data'
        schema: str = 'nn'

    def __post_init__(self):
        super().__post_init__()
        # self.formid.form_name = self.formid.form_name
        # self.client_id.client_name = self.client_id.client_name
        # self.visitor.user_id = self.visitor_id
        # self.visitor.username = self.visitor_username
        # self.visitor.email_address = self.visitor_email
        # self.visitor.mobile_number = self.visitor_mobile_number
        # self.visitor.display_name = self.visitor_name
        # self.orgid.org_name = self.orgid.org_name
        # self.account_id.account_name = self.account_name
        # self.account_id.retailer = self.retailer
