from .organization import Organization
from .client import Client
from .store import Store, StoreType, StoreGeography
from .user import Role, User, StaffingUser
from .photos import Document, Photo, PhotoCategory
from .project import Project
from .forms import Form, FormMetadata, FormData, FormDefinition

NetworkNinja_Map = {
    "store": Store,
    "client": Client,
    "orgid": Organization,
    "user": User,
    "staffing_user": StaffingUser,
    'photo_category': PhotoCategory,
    'store_photo': Photo,
    "role": Role,
    "project": Project,
    "store_type": StoreType,
    "document": Document,
    'store_geography': StoreGeography,
    'form': FormDefinition,
    'form_metadata': FormMetadata,
    'form_data': FormData
}
