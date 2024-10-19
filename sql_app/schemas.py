import datetime;
from pydantic import BaseModel, Field;


class BookingCreate(BaseModel):
  user_id: int
  room_id: int
  booked_num: int
  start_datetime: datetime.datetime
  end_datetime: datetime.datetime
  
  
class Booking(BookingCreate):
  booking_id: int

  # ormapper用のモードをTrueにする
  # dictだけでなくormapperにも対応する
  class Config:
    orm_mode = True

class UserCreate(BaseModel):
  # intのみの型指定だとuser_idが必須のパラメータとなってしまうため
  # int | Noneで初期値をNoneとすることで、解決する
  # autonumberにしていないとNoneの値がそのまま入ってしまうので注意
  # リクエスト用とレスポンス用のスキーマを分けることもある
  # user_id: int | None = None
  username: str = Field(max_length=12)

class User(UserCreate):
  user_id: int
   # orm_modeはデータを取得するときにのみ必要になる
  class Config:
    orm_mode = True
    
    
class RoomCreate(BaseModel):
  roomname: str = Field(max_length=12)
  capacity: int  
    
class Room(RoomCreate):
  room_id: int
  
  class Config:
    orm_mode = True