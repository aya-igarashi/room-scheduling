from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud, model, schemas
from database import SessionLocal, engine

# データベースの作成, bindでどのエンジンを使うかを指定
model.Base.metadata.create_all(bind=engine)
  
app = FastAPI()

#dbSessionを獲得するための関数
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# @app.get("/")
# async def index():
#   return {"message": "Success"}

# Read
# ユーザーデータをリスト形式で返す
# 引数のdbで依存関係を設定
@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int =0, limit: int = 100, db: Session = Depends(get_db)) -> list[schemas.User]:
  users = crud.get_users(db, skip=skip, limit=limit)
  print(users)
  return users

@app.get("/rooms", response_model=List[schemas.Room])
def read_rooms(skip: int =0, limit: int = 100, db: Session = Depends(get_db)):
  rooms = crud.get_rooms(db, skip=skip, limit=limit)
  return rooms

@app.get("/bookings", response_model=List[schemas.Booking])
def read_bookings(skip: int =0, limit: int = 100, db: Session = Depends(get_db)):
  bookings = crud.get_bookings(db, skip=skip, limit=limit)
  return bookings


# Create
@app.post("/users", response_model = schemas.User)
def users(user: schemas.UserCreate, db: Session = Depends(get_db)):
  return crud.create_user(db=db, user=user)

@app.post("/rooms", response_model = schemas.Room)
def rooms(room: schemas.RoomCreate, db: Session = Depends(get_db)):
  return crud.create_room(db=db, room=room)

@app.post("/bookings", response_model = schemas.Booking)
def bookings(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
  return crud.create_booking(db=db, booking=booking)