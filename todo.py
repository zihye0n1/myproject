import streamlit as st
import sqlite3

st.set_page_config(
    page_title="LIFE GOALS TO DO",
    page_icon="🗓"
)

# 데이터베이스 연결
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# goals, user 및 notes 테이블 생성
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
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    gender TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
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
menu = st.sidebar.selectbox("MENU", ['LOG IN', 'LIFE GOALS TO DO', 'JOIN IN', 'MEMO'])

# 로그인 화면
if menu == 'LOG IN':
    st.title("LOG IN")
    id = st.text_input("ID")
    pw = st.text_input("PW", type="password")

    if st.button("LOG IN"):
        cursor.execute("SELECT * FROM user WHERE username=?", (id,))
        row = cursor.fetchone()

        if row and row[2] == pw:  # Check password
            st.session_state.logged_in = True
            st.sidebar.write(f"Welcome, {id}!")
        else:
            st.error("Login failed: Please check your username or password.")

# 목표 추가 화면
if st.session_state.logged_in and menu == 'LIFE GOALS TO DO':
    st.title("LIFE GOALS TO DO")

    selected_date = st.date_input("Select date:", value=None)
    new_goal = st.text_input("Type new goal:")

    if st.button("➕ Add Goal"):
        if selected_date not in st.session_state.goals:
            st.session_state.goals[selected_date] = []
            st.session_state.completed[selected_date] = []

        if new_goal:
            st.session_state.goals[selected_date].append(new_goal)
            st.session_state.completed[selected_date].append(False)
            st.success("New goal added!")

    if selected_date in st.session_state.goals and st.session_state.goals[selected_date]:
        st.write(f"{selected_date}'s goal:")
        for i, goal in enumerate(st.session_state.goals[selected_date]):
            completed = st.checkbox(goal, value=st.session_state.completed[selected_date][i], key=f"{selected_date}_{i}")
            st.session_state.completed[selected_date][i] = completed

    if st.button("SAVE"):
        for i, goal in enumerate(st.session_state.goals.get(selected_date, [])):
            if goal:
                cursor.execute("INSERT INTO goals (goal, completed, date) VALUES (?, ?, ?)", 
                               (goal, st.session_state.completed[selected_date][i], selected_date.strftime("%Y-%m-%d")))
        conn.commit()
        st.success("Today's goal is set!")

# 회원가입 화면
elif menu == 'JOIN IN':
    st.title("JOIN IN")
    id = st.text_input("ID")
    pw = st.text_input("PW", type='password')
    pw_check = st.text_input("PW CHECK", type='password')
    email = st.text_input("EMAIL")
    gender = st.radio("GENDER", ['male', 'female'])

    if st.button("JOIN IN"):
        if pw == pw_check:
            try:
                cursor.execute("INSERT INTO user (username, password, email, gender) VALUES (?, ?, ?, ?)", 
                               (id, pw, email, gender))
                conn.commit()
                st.success("Join success!")
            except sqlite3.IntegrityError:
                st.error("Join failed: Username already exists.")
        else:
            st.error("The passwords do not match.")

# 메모 화면
elif menu == 'MEMO':
    st.title("MEMO")

    if st.session_state.logged_in:
        user_id = 1  # 실제 사용자 ID로 변경 (세션 관리 필요)
        new_note = st.text_area("Type new memo:")
        
        if st.button("Save"):
            if new_note:
                cursor.execute("INSERT INTO notes (user_id, content) VALUES (?, ?)", 
                               (user_id, new_note))
                conn.commit()
                st.success("New memo added!")
            else:
                st.error("Type your memo.")
        
        st.write("Saved memo:")
        cursor.execute("SELECT content FROM notes WHERE user_id=?", (user_id,))
        notes = cursor.fetchall()
        
        for note in notes:
            st.write(note[0])

# 데이터베이스 연결 종료
conn.close()
