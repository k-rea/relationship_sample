from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import cruds, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_index():
    return {'msg': 'test message'}


@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    ret = cruds.create_post(db=db, post=post)
    print(ret)
    print('test~~~~~~~~s')
    return ret


@app.get("/posts/", response_model=List[schemas.Post])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = cruds.get_posts(db, skip=skip, limit=limit)
    return posts


@app.get("/posts/{user_id}", response_model=schemas.Post)
def read_user(post_id: int, db: Session = Depends(get_db)):
    # Get Models[Post, TagsMap]
    db_post = cruds.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_tags = cruds.get_tags_map_by_post_id(db=db, post_id=post_id)

    # Translate Models to Schemas
    sc_tags = [schemas.TagsMap(**dict(db_tag)) for db_tag in db_tags]
    sc_post = schemas.Post.from_orm(db_post)

    # Add TagsMap to Post
    sc_post.tags = sc_tags

    return sc_post


@app.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return cruds.create_tag(db=db, tag=tag)


@app.get("/tags/", response_model=List[schemas.Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = cruds.get_tags(db, skip=skip, limit=limit)
    return tags


@app.get("/tags/{tag_id}", response_model=schemas.Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = cruds.get_tag(db, tag_id=tag_id)
    if tag_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    return tag_id


@app.post("/tagsMap/", response_model=schemas.TagsMap)
def add_tags_map(tags_map: schemas.TagsMapCreate, db: Session = Depends(get_db)):
    return cruds.add_tag(db=db, tags_map=tags_map)
