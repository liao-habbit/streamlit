import streamlit as st
import hashlib
import re
from auth import back_to_login
from utils.db import init_db, add_user_safe, get_user_by_login, change_password, delete_account

# ---------------- 初始化資料庫 ----------------
init_db()  # 確保 users 表格存在

# ---------------- 驗證函數 ----------------
def valid_email(email: str) -> bool:
    """簡單檢查 email 格式"""
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None

def valid_password(pw: str) -> bool:
    """至少 8 碼，且包含英文字母與數字"""
    return len(pw) >= 8 and any(c.isalpha() for c in pw) and any(c.isdigit() for c in pw)

def hash_password(password: str) -> str:
    """SHA256 雜湊密碼"""
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- 判斷使用者是否登入 ----------------
current_user = st.session_state.get("username", None)
current_user_id = st.session_state.get("user_id", None)

# ---------------- 尚未登入：顯示註冊頁 ----------------
if not current_user:
    st.title("📝 註冊新帳號")
    st.info("請填寫以下資訊以建立新帳號")

    new_user = st.text_input("帳號")
    new_email = st.text_input("電子郵件")
    new_pw = st.text_input("密碼", type="password")
    new_pw_confirm = st.text_input("再次輸入密碼", type="password")

    if st.button("註冊"):
        if not new_user or not new_email or not new_pw:
            st.warning("帳號、電子郵件或密碼不可空白")
        elif not valid_email(new_email):
            st.warning("電子郵件格式錯誤")
        elif not valid_password(new_pw):
            st.warning("密碼至少8碼，且需包含英文字母與數字")
        elif new_pw != new_pw_confirm:
            st.warning("密碼不一致")
        else:
            hashed_pw = hash_password(new_pw)
            success, msg = add_user_safe(new_user, new_email, hashed_pw)
            if success:
                st.success("帳號新增成功！請返回登入頁登入")
                back_to_login()
            else:
                st.warning(msg)

# ---------------- 已登入：顯示帳號管理 ----------------
else:
    st.title("👤 帳號管理")
    st.write(f"歡迎, {current_user}")

    user = get_user_by_login(current_user)
    if not user:
        st.error("使用者資料不存在！")
        st.stop()

    action = st.radio("選擇操作", ["修改密碼", "刪除帳號"])

    # ---------------- 修改密碼 ----------------
    if action == "修改密碼":
        st.session_state.new_pw = st.text_input("新密碼", type="password")
        st.session_state.confirm_pw = st.text_input("再次輸入新密碼", type="password")

        if st.button("更新密碼"):
            new_hash = hash_password(st.session_state.new_pw)
            old_hash = user[3]  
            if not st.session_state.new_pw or not st.session_state.confirm_pw:
                st.warning("密碼不可空白")
            elif st.session_state.new_pw != st.session_state.confirm_pw:
                st.warning("密碼不一致")
            elif not valid_password(st.session_state.new_pw):
                st.warning("密碼至少8碼，且需包含英文字母與數字")
            elif hash_password(st.session_state.new_pw) == old_hash:
                st.warning("新密碼不能與舊密碼相同")
            else:
                change_password(current_user, hash_password(st.session_state.new_pw))
                st.success("密碼已更新成功！請重新登入")
                st.session_state.user = None
                st.session_state.logged_in = False
                back_to_login()

    # ---------------- 刪除帳號 ----------------
    elif action == "刪除帳號":
        confirm_checkbox = st.checkbox("我確定要刪除我的帳號")

        if st.button("刪除帳號") and confirm_checkbox:
            delete_account(current_user)
            st.success("您的帳號已成功刪除")
            st.session_state['username'] = None
            st.session_state['user_id'] = None
            st.session_state['logged_in'] = False
            back_to_login()
