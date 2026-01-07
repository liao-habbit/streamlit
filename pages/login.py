import streamlit as st
import hashlib
from auth import go_to_register,go_to_forgot_password
from pathlib import Path
import json

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 ES6")
BASE_DIR = Path().resolve()  # 專案根目錄
USER_DB_FILE = BASE_DIR / "users.json"

# --------- 使用者資料 ---------
with open(USER_DB_FILE, "r") as f:
    try:
        USERS = json.load(f)
    except json.JSONDecodeError:
        USERS = {}  # 防止 JSON 壞掉或空檔

# --------- 初始化 session ---------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --------- 登入畫面 ---------
login_input = st.text_input("帳號或電子郵件")
password = st.text_input("密碼", type="password")
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("登入"):
        found_user = None
        # 搜尋帳號或 email
        for username, info in USERS.items():
            if login_input == username or login_input == info.get("email"):
                found_user = username
                break

        if not found_user:
            st.error("帳號或電子郵件不存在")
        else:
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            if hashed_pw == USERS[found_user]["password"]:
                st.session_state.logged_in = True
                st.session_state.user = found_user
                st.success(f"登入成功！歡迎 {found_user}")
                st.switch_page("pages/main.py")  # Streamlit >=1.22 可以直接用檔名，不加 .py
            else:
                st.error("密碼錯誤")
# with col2:
#      if st.button("忘記密碼？"):
#         go_to_forgot_password() 
st.divider()

# --------- 註冊導向 ---------
if st.button("註冊新帳號"):
    go_to_register()  # 導向 register 頁
