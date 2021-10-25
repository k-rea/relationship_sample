from typing import List, Optional, Any

from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class TagsMapBase(BaseModel):
    tag_id: int
    post_id: int


class TagsMapCreate(TagsMapBase):
    pass


class TagsMap(TagsMapBase):
    tag_name: str = ''

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    description: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    tags: List[TagsMap] = []

    class Config:
        orm_mode = True
