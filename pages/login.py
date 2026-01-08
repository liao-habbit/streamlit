import streamlit as st
import hashlib
from pathlib import Path
from utils.db import get_user_by_login  # 你之前寫的 SQLite 函數
from auth import go_to_register, go_to_forgot_password

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 ES6")

# 初始化 session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# 登入畫面
login_input = st.text_input("帳號或電子郵件")
password = st.text_input("密碼", type="password")


if st.button("登入"):
    # 先以 username 查詢，再以 email 查詢
    user = get_user_by_login(login_input)
    if not user:
        st.error("帳號或電子郵件不存在")
    else:
        user_id, username, email, password_hash, _ = user
        if hashlib.sha256(password.encode()).hexdigest() == password_hash:
            st.success(f"登入成功！歡迎 {username}")
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.username = username
            # 跳轉到 main.py
            st.switch_page("pages/main.py")
        else:
            st.error("密碼錯誤")
st.divider()


if st.button("註冊新帳號"):
    go_to_register()
