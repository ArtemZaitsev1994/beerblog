from typing import Dict

from pydantic import BaseModel


class Comment(BaseModel):
    _id: str
    alcohol_type: str
    comment: Dict[str, str]


class ItemRating(BaseModel):
    _id: str
    alcohol_type: str
    rate: int
    login: str
