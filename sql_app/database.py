from sqlalchemy import create_engine;
from sqlalchemy.ext.declarative import declarative_base;
from sqlalchemy.orm import sessionmaker;

#データベース接続URL
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_qpp.db'

# chek_same_thread以下は、SQLiteに必要な記述
engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# データベースの構造を作るクラスdeclarative_base()を継承する
Base = declarative_base()


