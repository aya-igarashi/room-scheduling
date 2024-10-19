from sqlalchemy import Column, ForeignKey, Integer, String, DateTime;
from database import Base;

class User(Base):
  # テーブル名
  __tablename__ = 'users'
  # indexは検索を速くするための仕組み
  user_id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)

class Room(Base):
  # テーブル名
  __tablename__ = 'rooms'
  
  room_id = Column(Integer, primary_key=True, index=True)
  roomname = Column(String, unique=True, index=True)
  capacity = Column(Integer)
  
class Booking(Base):
  # テーブル名
  __tablename__ = 'bookings'
  
  booking_id = Column(Integer, primary_key=True, index=True)
  # ondeleteはForeignKeyで対応するカラムデータが削除された場合に
  # 対応するレコードごと消すのか対応するカラムのレコード部分をnullにするのかを指定する
  user_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=False)
  room_id = Column(Integer, ForeignKey('rooms.room_id', ondelete='SET NULL'), nullable=False)
  booked_num = Column(Integer)
  start_datetime = Column(DateTime, nullable=False)
  end_datetime = Column(DateTime, nullable=False)