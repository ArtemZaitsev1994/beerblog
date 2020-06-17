from pydantic import BaseModel


class ItemsList(BaseModel):
    page: int
    sorting: str
    query: str = ''
    notConfirmed: bool = None


class Item(BaseModel):
    # ужос TODO
    id: str


class ChangeStateItem(Item):
    not_confirmed: bool


class ResponseBeerItem(BaseModel):
    name: str
    rate: int
    review: str
    alcohol: float
    fortress: float
    others: str = ''
    manufacturer: str = ''
    not_confirmed: bool = None
    ibu: int = -1


class ResponseWineItem(BaseModel):
    name: str
    rate: int
    review: str
    style: str
    alcohol: float
    others: str = ''
    manufacturer: str = ''
    not_confirmed: bool = None
    sugar: str = ''


class ResponseBarItem(BaseModel):
    name: str
    rate: int
    review: str
    others: str = ''
    address: str = ''
    not_confirmed: bool = None
    worktime: str = ''
    city: str = ''
    country: str = ''
    site: str = ''
