import streamlit as st
import datetime
import requests
import json
import pandas as pd

page = st.sidebar.selectbox('Choose your page', ['users', 'rooms', 'bookings'])

if page == 'users':
  st.title('ユーザー登録画面')

  with st.form(key='user'):
    # user_id: int = random.randint(0, 10)
    username: str = st.text_input('ユーザー名', max_chars=12)
    data = {
      # 'user_id': user_id,
      'username': username
    }
    submit_button = st.form_submit_button(label='リクエスト送信')

  if submit_button:
    url = 'http://127.0.0.1:8000/users'
    res = requests.post(
      url, 
      data=json.dumps(data)
    )
    st.json(res.json())

elif page == 'rooms':
  st.title('会議室登録画面')

  with st.form(key='room'):
    # room_id: int = random.randint(0, 10)
    roomname: str = st.text_input('会議室名', max_chars=12)
    capacity: int = st.number_input('定員', step=1)
    data = {
      'roomname': roomname,
      'capacity': capacity
    }
    submit_button = st.form_submit_button(label='リクエスト送信')

  if submit_button:
    url = 'http://127.0.0.1:8000/rooms'
    res = requests.post(
      url, 
      data=json.dumps(data)
    )
    if res.status_code == 200:
      st.success("登録完了")
    st.json(res.json())
  
else: 

  st.title('予約登録画面')
  # ユーザー一覧取得
  users_url = 'http://127.0.0.1:8000/users'
  # ユーザー一覧をリクエストしレスポンスをresに入れる
  res = requests.get(users_url)
  # resをjson形式にしてusersに代入
  users = res.json()
  
  # usernamをkey,user_idをvalueとして辞書を作成
  user_name = {}
  for user in users:
    user_name[user['username']] = user['user_id']
  
  # 会議室一覧取得
  rooms_url = 'http://127.0.0.1:8000/rooms'
  # ユーザー一覧をリクエストしレスポンスをresに入れる
  res = requests.get(rooms_url)
  # resをjson形式にしてroomsに代入
  rooms = res.json()
  
  # roomnamをkey, capacity, room_idをvalueとして辞書を作成
  room_name = {}
  for room in rooms:
    room_name[room['roomname']] = {
      'capacity': room['capacity'],
      'room_id': room['room_id']
      }

  st.write('### 会議室一覧')
  df_rooms = pd.DataFrame(rooms)
  print(rooms)
  df_rooms.columns = ['会議室名', '定員', '会議室ID']
  st.table(df_rooms)
  
  
  # 会議室一覧取得
  bookings_url = 'http://127.0.0.1:8000/bookings'
  # ユーザー一覧をリクエストしレスポンスをresに入れる
  res = requests.get(bookings_url)
  # resをjson形式にしてbookingsに代入
  bookings = res.json()
  df_bookings = pd.DataFrame(bookings)
  
  users_id = {}
  for user in users:
    users_id[user["user_id"]] = user["username"]
  rooms_id = {}
  for room in rooms:
    rooms_id[room["room_id"]] = {
      "roomname" : room["roomname"],
      "capacity" : room["capacity"]
    }
  
  #IDを各値に変更
  to_username = lambda x : users_id[x]
  to_room_name = lambda x: rooms_id[x]["roomname"]
  to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime("%Y/%m%d %H:%M")
  
  # 特定の列に同じ処理を適用
  df_bookings["user_id"] = df_bookings['user_id'].map(to_username)
  df_bookings["room_id"] = df_bookings['room_id'].map(to_room_name)
  df_bookings["start_datetime"] = df_bookings['start_datetime'].map(to_datetime)
  df_bookings["end_datetime"] = df_bookings['end_datetime'].map(to_datetime)
  
  df_bookings = df_bookings.rename(columns={
    "user_id":"予約者名",
    "room_id":"会議室名",
    "booked_num":"予約人数",
    "start_datetime":"開始時刻",
    "end_datetime":"終了時刻",
    "booking_id":"予約番号"
  })
  st.write("### 予約一覧")
  st.table(df_bookings)
  
  with st.form(key='booking'):
    username: str = st.selectbox('予約者名', user_name.keys())
    roomname: str = st.selectbox('予約者名', room_name.keys())
    booked_num: int = st.number_input('予約人数', step=1, min_value=1)
    date = st.date_input('日付を入力: ', min_value=datetime.date.today())
    start_time = st.time_input('開始時刻: ', value=datetime.time(hour=9, minute=0))
    end_time = st.time_input('終了時刻: ', value=datetime.time(hour=9, minute=0))
    
    submit_button = st.form_submit_button(label='予約登録')

  if submit_button:
    user_id: int = user_name[username]
    room_id: int = room_name[roomname]['room_id']
    capacity: int = room_name[roomname]['capacity']
    
    data = {
      'user_id': user_id,
      'room_id': room_id,
      'booked_num': booked_num,
      'start_datetime': datetime.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=start_time.hour,
        minute=start_time.minute
      ).isoformat(),
      'end_datetime': datetime.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=end_time.hour,
        minute=end_time.minute
      ).isoformat()
    }
    
    # 定員より多い予約人数の場合
    if booked_num > capacity:
      st.error(f'{roomname}の定員は、{capacity}名です。{capacity}以下の予約人数まで受け付けます。')
    # 開始時刻 >= 終了時刻
    elif start_time >= end_time:
      st.error("開始時刻が終了時刻を超えています。")
    elif start_time < datetime.time(hour=9, minute=0, second=0) or end_time > datetime.time(hour=20, minute=0, second=0):
      st.error("利用時間は9:00~20:00になります。")
    else:
      url = 'http://127.0.0.1:8000/bookings'
      res = requests.post(
        url, 
        data=json.dumps(data)
      )
      if res.status_code == 200:
        st.success('予約が完了しました。')
      elif res.status_code == 404 and res.json()["detail"] == "Already booked":
        st.error("指定の時間には既に予約が入っています。")
      
      
    
  
