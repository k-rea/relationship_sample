from sqlalchemy import select, func
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine


def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tag).offset(skip).limit(limit).all()


def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    print("debug: success commit")
    return db_post


def add_tag(db: Session, tags_map: schemas.TagsMapCreate):
    db_map = models.TagsMap(**tags_map.dict())
    db.add(db_map)
    db.commit()
    db.refresh(db_map)
    return db_map


def get_tags_map_by_post_id(db: Session, post_id: int):
    print('\============')
    sql = select(
        [models.TagsMap, models.Tag.name.label("tag_name")]).join(
        models.Tag, models.Tag.id == models.TagsMap.tag_id).filter(
        models.TagsMap.post_id == post_id)
    # print(sql)
    db_tags = engine.execute(sql).fetchall()
    print('\============*****')
    return db_tags
