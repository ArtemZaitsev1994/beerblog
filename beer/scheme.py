from typing import List

from fastapi import UploadFile, Form
from pydantic import BaseModel


class AddBeer(BaseModel):
    name: str
    rate: int
    review: str
    alcohol: float
    fortress: float
    others: str
    manufacturer: str
    photos: List[UploadFile]
    ibu: int = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        rate: int = Form(...),
        review: str = Form(...),
        alcohol: float = Form(...),
        fortress: float = Form(...),
        others: str = Form(''),
        manufacturer: str = Form(''),
        photos: List[UploadFile] = [],
        ibu: int = Form(None),
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
