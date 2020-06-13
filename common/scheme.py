from typing import Dict

from pydantic import BaseModel


class Comment(BaseModel):
    itemId: str
    alcohol_type: str
    comment: Dict[str, str]


class ItemRating(BaseModel):
    itemId: str
    alcohol_type: str
    rate: int
    login: str


class VersionSchema(BaseModel):
    version: str
