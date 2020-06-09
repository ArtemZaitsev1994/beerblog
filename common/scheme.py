from pydantic import BaseModel


class Comment(BaseModel):
    _id: str
    alcohol_type: str
    text: str


class ItemRating(BaseModel):
    # ужос TODO
    id: str
