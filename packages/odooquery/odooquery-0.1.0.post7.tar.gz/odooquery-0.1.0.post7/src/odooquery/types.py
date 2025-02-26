from typing_extensions import TypedDict, List, Optional, Union
from pydantic import BaseModel

class Message(TypedDict):
    id: int
    date: str
    body: str
    author_id: int
    author_name: str
    subtype_id: int
    subtype_name: str
    attachment_ids: List[int]
    is_internal: bool
    description: str
    message_type: str
    needaction: bool

class Ticket(TypedDict):
    id: int
    subject: str
    author_name: str
    author_email: str
    description: str
    messages: List[Message]
    stage: str

class TransferLine(TypedDict):
    product_id: int
    product_name: str
    reference_code: str
    quantity: float
    quantity_done: float

class Transfer(TypedDict):
    name: str
    state: str
    date_done: str
    items: List[TransferLine]

class OrderLine(TypedDict):
    product: str
    quantity: float

class Order(TypedDict):
    order_number: int
    items: List[OrderLine]
    transfers: List[Transfer]
    status: str

class Partner(TypedDict):
    id: int
    name: str
    email: str
    phone: str
    company_name: str
    street: str
    city: str
    state_id:int
    state_name: str
    country_id: int
    country_name: str
    zip: str

class ProductStock(TypedDict):
    location_id: int
    location_name: str
    quantity: float
    reserved_quantity: float
    available_quantity: float

class ProductVariant(TypedDict):
    id: int
    name: str
    default_code: str  # SKU/reference code
    barcode: Optional[str]
    list_price: float
    standard_price: float  # cost price

class Product(TypedDict):
    id: int
    name: str
    default_code: str
    description: str
    category_id: int
    category_name: str

class MailingStatistic(TypedDict):
    id: int
    mass_mailing_id: int
    model: str
    res_id: int
    email: str
    sent: str  # datetime
    opened: Optional[str]  # datetime
    clicked: Optional[str]  # datetime
    bounced: Optional[str]  # datetime
    exception: Optional[str]

class MailingContact(TypedDict):
    id: int
    name: str
    email: str
    list_ids: List[int]
    unsubscribed: bool
    opt_out: bool

class MassMailing(TypedDict):
    id: int
    name: str
    subject: str
    sent_date: str  # datetime
    state: str
    mailing_model: str
    statistics_ids: List[int]
    contact_list_ids: List[int]