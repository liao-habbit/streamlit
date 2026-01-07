import streamlit as st
import json
import hashlib
from pathlib import Path
from auth import back_to_login
import re
def valid_email(email):
            # 簡單檢查有 @ 與 .
            return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None

def valid_password(pw):
    # 至少 8 碼，且包含英文字母與數字
    return len(pw) >= 8 and re.search(r"[A-Za-z]", pw) and re.search(r"\d", pw)
BASE_DIR = Path().resolve()
USER_DB_FILE = BASE_DIR / "users.json"

# 建立空 JSON 如果不存在
if not USER_DB_FILE.exists() or USER_DB_FILE.stat().st_size == 0:
    USER_DB_FILE.write_text("{}")

with open(USER_DB_FILE, "r") as f:
    USERS = json.load(f)

def save_users():
    with open(USER_DB_FILE, "w") as f:
        json.dump(USERS, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- 判斷使用者是否登入 ----------------
current_user = st.session_state.get("user", None)

# ---------------- 如果已登入 ----------------
if current_user:
    st.sidebar.write(f"👤 已登入：{current_user}")
    action = st.sidebar.selectbox(
        "帳號管理功能",
        ["修改密碼", "刪除帳號"]
    )

    # ---------------- 修改密碼 ----------------
    if action == "修改密碼":
        st.subheader("修改密碼")
        new_pw = st.text_input("新密碼", type="password")
        confirm_pw = st.text_input("再次輸入新密碼", type="password")

        # 密碼驗證函數
        def valid_password(pw):
            # 至少 8 碼，且包含英文字母與數字
            return len(pw) >= 8 and any(c.isalpha() for c in pw) and any(c.isdigit() for c in pw)

        if st.button("更新密碼"):
            if not new_pw or not confirm_pw:
                st.warning("密碼不可空白")
            elif new_pw != confirm_pw:
                st.warning("密碼不一致")
            elif not valid_password(new_pw):
                st.warning("密碼至少8碼，且需包含英文字母與數字")
            elif hashlib.sha256(new_pw.encode()).hexdigest() == USERS[current_user]["password"]:
                st.warning("新密碼不能與舊密碼相同")
            else:
                # 更新密碼
                USERS[current_user]["password"] = hashlib.sha256(new_pw.encode()).hexdigest()
                save_users()
                st.success("密碼已更新成功！請使用新密碼重新登入")
                
                # 清除登入狀態
                st.session_state['user'] = None
                st.session_state['logged_in'] = False

                # 立即返回登入頁
                back_to_login()


    # ---------------- 刪除帳號 ----------------
    elif action == "刪除帳號":
        st.subheader("刪除帳號")
        st.warning("刪除帳號會永久移除，無法復原！")

        login_input = st.text_input("請輸入您的帳號或電子郵件")
        password_input = st.text_input("請輸入密碼", type="password")
        confirm_checkbox = st.checkbox("我確定要刪除我的帳號")

        if st.button("刪除帳號") and confirm_checkbox:
            found_user = None
            # 找到對應帳號
            for username, info in USERS.items():
                if login_input == username or login_input == info.get("email", ""):
                    found_user = username
                    break

            if not found_user:
                st.error("帳號或電子郵件不存在")
            else:
                # 驗證密碼
                if USERS[found_user]["password"] != hashlib.sha256(password_input.encode()).hexdigest():
                    st.error("密碼錯誤")
                elif found_user != current_user:
                    st.error("只能刪除自己的帳號")
                else:
                    USERS.pop(found_user)
                    save_users()
                    st.success("您的帳號已成功刪除")
                    st.session_state['user'] = None
                    back_to_login()

# ---------------- 如果尚未登入 ----------------
else:
    st.subheader("尚未登入")
    st.info("請先登入或新增帳號")

    action = st.sidebar.selectbox(
        "帳號管理功能",
        ["新增帳號"]
    )

    if action == "新增帳號":
        new_user = st.text_input("帳號")
        new_email = st.text_input("電子郵件")
        new_pw = st.text_input("密碼", type="password")
        new_pw_confirm = st.text_input("再次輸入密碼", type="password")
        # ---------------- 註冊按鈕 ----------------
        if st.button("註冊新帳號"):
            # 1️⃣ 空白檢查
            if not new_user or not new_pw or not new_email:
                st.warning("帳號、電子郵件或密碼不可空白")
            # 2️⃣ email 格式檢查
            elif not valid_email(new_email):
                st.warning("電子郵件格式錯誤")
            # 3️⃣ 密碼格式檢查
            elif not valid_password(new_pw):
                st.warning("密碼至少8碼，且需包含英文字母與數字")
            # 4️⃣ 密碼確認
            elif new_pw != new_pw_confirm:
                st.warning("密碼不一致")
            # 5️⃣ 帳號已存在
            elif new_user in USERS:
                st.warning("帳號已存在")
            else:
                USERS[new_user] = {"password": hash_password(new_pw), "email": new_email}
                save_users()
                st.success("帳號新增成功！請返回登入頁登入")
                back_to_login()