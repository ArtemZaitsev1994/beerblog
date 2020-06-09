from typing import List

from fastapi import UploadFile, Form
from pydantic import BaseModel


class AddBar(BaseModel):
    name: str
    rate: int
    review: str
    others: str
    address: str
    photos: List[UploadFile]
    worktime: str
    city: str
    country: str
    site: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        rate: int = Form(...),
        review: str = Form(''),
        others: str = Form(''),
        address: str = Form(''),
        photos: List[UploadFile] = [],
        worktime: str = Form(''),
        city: str = Form(''),
        country: str = Form(''),
        site: str = Form(''),
    ):
        return cls(
            name=name, rate=rate, review=review,
            others=others, address=address, photos=photos,
            worktime=worktime, city=city, country=country,
            site=site
        )


class BarList(BaseModel):
    page: int
    sorting: str
    query: str = ''


class BarItem(BaseModel):
    # ужос TODO
    id: str
