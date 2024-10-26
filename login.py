import streamlit as st
import sqlite3

menu = st.sidebar.selectbox("MENU", ['로그인', '회원가입', '회원정보수정', '탈퇴'])


if menu == '로그인':
    conn = sqlite3 .connect('db.db')
    cursor = conn.cursor()

    st.title("로그인")
    id = st.text_input("아이디")
    pw = st.text_input("비밀번호", type="password")
    btn = st.button("로그인")
    
    #로그인 버튼을 클릭
    if btn:
        #입력한 데이터(아이디, 비번) 가져온다
        #db에서 (입력한 아이디)정보를 가져오기
        cursor.execute(f"SELECT * FROM user WHERE username='{id}'")
        row = cursor.fetchone()
        #비밀번호 일치 여부 확인
        #userid, username, password....
        if row:
            db_id = row[1]
            db_pw = row[2]
        else:
            db_id = ''
            db_pw = ''

        if db_pw == pw:
            #로그인을 성공! sidebar ID님 환영합니다
            st.sidebar.write(f"{id}님 환영합니다.")
        else:
            #로그인 실패-> 로그인 실패!
            #ID test
            #PW 123
            st.error("로그인 실패!!")

elif menu == '회원가입':
    conn = sqlite3 .connect('db.db')
    cursor = conn.cursor()
   
#데이터 베이스 연결
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    #회원가입 화면
    st.title("회원가입")
    #아이디
    id = st.text_input("아이디")
    #비밀번호
    pw = st.text_input("비밀번호", type='password')
    #비밀번호 확인
    pw_check = st.text_input("비밀번호 확인", type='password')
    #이메일
    email = st.text_input("이메일")
    #성별(라디오버튼)
    gender = st.radio("성별을 선택하세요", ['male','female'])
    #회원가입 버튼
    btn = st.button("회원가입")

    #버튼을 누르면
    if btn:
        #비밀번호가 잘 입력되었는지를 확인
        if pw == pw_check:            
            #입력한 정보를 DB에 저장
            sql = f"""
insert into user(username, password, email, gender)
values('{id}','{pw}','{email}','{gender}')"""
            cursor.execute(sql)
            conn.commit()
            st.success("회원가입 성공!")
        else:
            #회원가입 실패
            st.error("비밀번호가 일치하지 않습니다.")
    conn.close()

if menu == '회원정보 수정':
    conn = sqlite3 .connect('db.db')
    cursor = conn.cursor()

#회원정보 수정 화면
    st.title("회원정보 수정")
    #아이디
    id = st.text_input("아이디")
    #비밀번호
    pw = st.text_input("비밀번호", type='password')  
    #회원가입 버튼
    btn = st.button("수정")

    if btn:
        sql=f"""
UPDATE user  SET 
password = "{pw}".
email = "{email}",
gender = "{gender}",
WHERE username = "{id}"
"""
    cursor.execute(sql)
    conn.commit()

if menu == '탈퇴':
    conn = sqlite3 .connect('db.db')
    cursor = conn.cursor()

    st.title("탈퇴")
    id = st.text_input("아이디")
    pw = st.text_input("비밀번호", type="password")
    btn = st.button("탈퇴")
    
    #로그인 버튼을 클릭
    if btn:
        #입력한 데이터(아이디, 비번) 가져온다
        #db에서 (입력한 아이디)정보를 가져오기
        cursor.execute(f"SELECT * FROM user WHERE username='{id}'")
        row = cursor.fetchone()
        #비밀번호 일치 여부 확인
        #userid, username, password....
        if row:
            db_id = row[1]
            db_pw = row[2]
        else:
            db_id = ''
            db_pw = ''

        if db_pw == pw:
            #로그인을 성공! sidebar ID님 환영합니다
            st.sidebar.write("계정탈퇴 완료")
        else:
            #로그인 실패-> 로그인 실패!
            #ID test
            #PW 123
            st.error("탈퇴실패")




#데이터 삭제
if btn:
    sql="""
DELETE FROM user WHERE username="{id}"
"""

    conn.execute(sql)
    conn.commit()