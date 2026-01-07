import streamlit as st
import hashlib 

st.set_page_config(page_title="Login", layout="centered")

# --------- 使用者資料（之後可換成 DB）---------
USERS = {
    "chienen": hashlib.sha256("CPzQWPaW1".encode()).hexdigest()
}

# --------- 初始化 session ---------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --------- 登入畫面 ---------
st.title("🔐 系統登入")

username = st.text_input("帳號")
password = st.text_input("密碼", type="password")

if st.button("登入"):
    if username in USERS:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        if hashed_pw == USERS[username]:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("登入成功")
            st.switch_page("app.py")
        else:
            st.error("密碼錯誤")
    else:
        st.error("帳號不存在")
