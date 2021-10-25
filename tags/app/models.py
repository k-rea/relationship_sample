from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    tags_map = relationship("TagsMap", back_populates="tag")


class TagsMap(Base):
    __tablename__ = "tags_map"
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)

    tag = relationship("Tag")
    post = relationship("Post", back_populates="tags")

    tags_map_pk = PrimaryKeyConstraint("tag_id", "post_id")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    tags = relationship("TagsMap")
