from sqlalchemy.orm import Session;
import model
import schemas;
from fastapi import HTTPException

# ユーザー一覧
# offset(skip)は上位〜こ分のデータをスキップ
# どのデータベースでも対応できるように引数はdbで設定:Sessionは型ヒント
# limit()、いくつ分のレコードを取ってくるかを指定
def get_users(db: Session, skip: int = 0, limit: int = 100):
  # query(model.User)でmodel.Userテーブルに問い合わせる
  return db.query(model.User).offset(skip).limit(limit).all()

# 会議室一覧取得
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
  return db.query(model.Room).offset(skip).limit(limit).all()

# 予約一覧取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
  return db.query(model.Booking).offset(skip).limit(limit).all()

# ユーザー登録
def create_user(db: Session, user: schemas.User):
  db_user = model.User(username=user.username)
  # addではまだ追加されていない
  db.add(db_user)
  # ユーザーがdbに登録される
  db.commit()
  # データベースを変更を反映、更新するためにリフレッシュする
  db.refresh(db_user)
  return db_user
  
# 会議室登録
def create_room(db: Session, room: schemas.Room):
  db_room = model.Room(roomname=room.roomname, capacity=room.capacity)
  db.add(db_room)
  db.commit()
  db.refresh(db_room)
  return db_room

# 予約登録
def create_booking(db: Session, booking: schemas.Booking):
  db_booked = db.query(model.Booking).\
    filter(model.Booking.room_id == booking.room_id).\
    filter(model.Booking.end_datetime > booking.start_datetime).\
    filter(model.Booking.start_datetime < booking.end_datetime).\
    all()
  
  # 重複するデータがなければ
  if len(db_booked) == 0:
    db_booking = model.Booking(
      user_id = booking.user_id, 
      room_id = booking.room_id,
      booked_num = booking.booked_num,
      start_datetime = booking.start_datetime,
      end_datetime = booking.end_datetime 
    )  
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
  else:
    raise HTTPException(status_code=404, detail="Already booked")