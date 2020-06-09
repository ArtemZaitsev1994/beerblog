from typing import List

from fastapi import UploadFile, Form
from pydantic import BaseModel


class AddWine(BaseModel):
    name: str
    rate: int
    review: str
    others: str
    manufacturer: str
    photos: List[UploadFile]
    alcohol: float
    style: str
    sugar: str

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
        style: str = Form(''),
        sugar: str = Form(''),
    ):
        return cls(
            name=name, rate=rate, review=review,
            others=others, manufacturer=manufacturer, photos=photos,
            style=style, sugar=sugar, alcohol=alcohol
        )


class WineList(BaseModel):
    page: int
    sorting: str
    query: str = ''


class WineItem(BaseModel):
    # ужос TODO
    id: str
