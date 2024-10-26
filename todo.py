import streamlit as st
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# goals 테이블 및 user 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
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
    st.session_state.goals = []
if 'completed' not in st.session_state:
    st.session_state.completed = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 사이드바 메뉴 선택
menu = st.sidebar.selectbox("MENU", ['LOG IN', 'LIFE GOALS TO DO', 'JOIN IN'])

# 로그인 화면
if menu == 'LOG IN':
    st.title("LOG IN")
    id = st.text_input("ID")
    pw = st.text_input("PW", type="password")
    
    btn_login = st.button("LOG IN")  # 로그인 버튼

    if btn_login:  # 버튼 클릭 시
        cursor.execute("SELECT * FROM user WHERE username=?", (id,))
        row = cursor.fetchone()
        
        if row and row[2] == pw:  # 비밀번호 확인
            st.session_state.logged_in = True
            st.sidebar.write(f"{id}님 환영해요!")
        else:
            st.error("LOG IN FAIL!")

# 목표 추가 화면
if st.session_state.logged_in and menu == 'LIFE GOALS TO DO':
    st.title("LIFE GOALS TO DO")

    # '+' 버튼 클릭 시 목표 입력 칸 추가
    if st.button("➕ Add Goal"):  # 목표 추가 버튼
        st.session_state.goals.append("")  # 빈 문자열 추가
        st.session_state.completed.append(False)  # 완료 상태 추가

    # 목표 입력 칸 및 체크박스 표시
    for i in range(len(st.session_state.goals)):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.session_state.goals[i] = st.text_input(f"TODAY'S GOAL {i + 1}:", value=st.session_state.goals[i])
        with col2:
            st.session_state.completed[i] = st.checkbox("Done", value=st.session_state.completed[i])

    # 목표 목록 출력
    if st.session_state.goals:
        st.write("TODAY'S GOAL:")
        for i in range(len(st.session_state.goals)):
            status = "✔️" if st.session_state.completed[i] else "❌"
            st.write(f"- {status} {st.session_state.goals[i]}")

    # 목표를 데이터베이스에 저장하는 로직 추가
    if st.button("SAVE"):  # 저장 버튼
        for i in range(len(st.session_state.goals)):
            if st.session_state.goals[i]:  # 목표가 비어있지 않은 경우에만 저장
                cursor.execute("INSERT INTO goals (goal, completed) VALUES (?, ?)", 
                               (st.session_state.goals[i], st.session_state.completed[i]))
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
    
    btn_join = st.button("JOIN IN")  # 회원가입 버튼

    if btn_join:  # 버튼 클릭 시
        if pw == pw_check:
            cursor.execute("INSERT INTO user (username, password, email, gender) VALUES (?, ?, ?, ?)", 
                           (id, pw, email, gender))
            conn.commit()
            st.success("JOIN SUCCESS!")
        else:
            st.error("PLEASE CHECK YOUR PW")

# 데이터베이스 연결 종료
conn.close()
