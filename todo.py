import streamlit as st
import sqlite3


import streamlit as st
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# completed 컬럼 추가
try:
    cursor.execute("ALTER TABLE goals ADD COLUMN completed BOOLEAN NOT NULL DEFAULT FALSE;")
    print("컬럼이 성공적으로 추가되었습니다.")
except sqlite3.OperationalError:
    print("컬럼 추가 시 오류가 발생했습니다. 이미 존재하는지 확인해 주세요.")

# goals 테이블 및 user 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    date TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    gender TEXT NOT NULL
)
""")
conn.commit()

# 나머지 코드 ...

# 데이터베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# goals 테이블 및 user 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    date TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    gender TEXT NOT NULL
)
""")
conn.commit()

# 세션 상태 초기화
if 'goals' not in st.session_state:
    st.session_state.goals = {}
if 'completed' not in st.session_state:
    st.session_state.completed = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 사이드바 메뉴 선택
menu = st.sidebar.selectbox("MENU", ['LOG IN', 'LIFE GOALS TO DO', 'JOIN IN'])

# 로그인 화면
if menu == 'LOG IN':
    st.title("LOG IN")
    id = st.text_input("ID")
    pw = st.text_input("PW", type="password")
    
    btn_login = st.button("LOG IN")

    if btn_login:
        cursor.execute("SELECT * FROM user WHERE username=?", (id,))
        row = cursor.fetchone()
        
        if row and row[2] == pw:
            st.session_state.logged_in = True
            st.sidebar.write(f"{id}님 환영해요!")
        else:
            st.error("LOG IN FAIL!")

# 목표 추가 화면
if st.session_state.logged_in and menu == 'LIFE GOALS TO DO':
    st.title("LIFE GOALS TO DO")

    # 목표 입력란
    selected_date = st.date_input("날짜 선택:", value=None)
    
    # 목표 추가 입력 필드
    new_goal = st.text_input("새 목표 입력:")

    if st.button("➕ Add Goal"):  # 목표 추가 버튼
        if selected_date not in st.session_state.goals:
            st.session_state.goals[selected_date] = []
            st.session_state.completed[selected_date] = []  # 완료 상태 초기화
        if new_goal:  # 목표가 비어있지 않으면 추가
            st.session_state.goals[selected_date].append(new_goal)  # 목표 추가
            st.session_state.completed[selected_date].append(False)  # 완료 상태 추가
            st.success("목표가 추가되었습니다.")

    # 목표 목록 출력
    if selected_date in st.session_state.goals and st.session_state.goals[selected_date]:
        st.write(f"{selected_date}의 목표:")
        for i in range(len(st.session_state.goals[selected_date])):
            goal = st.session_state.goals[selected_date][i]
            completed = st.session_state.completed[selected_date][i]
            # 체크박스 상태 유지
            completed = st.checkbox(f"{goal}", value=completed, key=f"{selected_date}_{i}")

            # 체크박스 상태 업데이트
            st.session_state.completed[selected_date][i] = completed

    # 목표를 데이터베이스에 저장하는 로직 추가
    if st.button("SAVE"):
        for i, goal in enumerate(st.session_state.goals.get(selected_date, [])):
            if goal:
                cursor.execute("INSERT INTO goals (goal, completed, date) VALUES (?, ?, ?)", 
                               (goal, st.session_state.completed[selected_date][i], selected_date.strftime("%Y-%m-%d")))
        conn.commit()
        st.success("YOUR GOAL IS SAVED!")

# 회원가입 화면
elif menu == 'JOIN IN':
    st.title("JOIN IN")
    id = st.text_input("ID")
    pw = st.text_input("PW", type='password')
    pw_check = st.text_input("PW CHECK", type='password')
    email = st.text_input("EMAIL")
    gender = st.radio("GENDER", ['male', 'female'])
    
    btn_join = st.button("JOIN IN")

    if btn_join:
        if pw == pw_check:
            cursor.execute("INSERT INTO user (username, password, email, gender) VALUES (?, ?, ?, ?)", 
                           (id, pw, email, gender))
            conn.commit()
            st.success("JOIN SUCCESS!")
        else:
            st.error("PLEASE CHECK YOUR PW")

# 데이터베이스 연결 종료
conn.close()
