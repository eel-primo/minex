from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(uuid=user.uuid)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # return db_user

def add_server(db: Session, item: schemas.ServerCreate, user_id: int):
    db_item = models.Servers(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # return db_item

def get_user(db: Session, user_uuid: str):
    return db.query(models.User).filter(models.User.uuid == user_uuid).first()

def get_user_servers(db: Session, user_uuid: str, skip: int = 0, limit: int = 10):
    return db.query(models.Servers).filter(models.Servers.owner_id == user_uuid).offset(skip).limit(limit).all()

def count_servers(db: Session):
    return len(db.query(models.Servers).all())