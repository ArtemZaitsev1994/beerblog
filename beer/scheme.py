from typing import List

from fastapi import UploadFile, Form
from pydantic import BaseModel


class AddBeer(BaseModel):
    name: str
    rate: int
    review: str
    others: str
    manufacturer: str
    photos: List[UploadFile]
    alcohol: float
    ibu: int
    fortress: float

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        rate: int = Form(...),
        review: str = Form(''),
        others: str = Form(''),
        manufacturer: str = Form(''),
        photos: List[UploadFile] = [],
        alcohol: float = Form(''),
        ibu: int = Form(''),
        fortress: float = Form('')
    ):
        return cls(
            name=name, rate=rate, review=review,
            others=others, manufacturer=manufacturer, photos=photos,
            alcohol=alcohol, ibu=ibu, fortress=fortress
        )


class BeerList(BaseModel):
    page: int
    sorting: str
    query: str = ''


class BeerItem(BaseModel):
    # ужос TODO
    id: str
