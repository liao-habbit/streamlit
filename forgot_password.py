# import streamlit as st
# import hashlib
# import random
# import string
# from pathlib import Path
# import json


# BASE_DIR = Path().resolve()
# USER_DB_FILE = BASE_DIR / "users.json"

# # 讀取使用者資料
# with open(USER_DB_FILE, "r") as f:
#     try:
#         USERS = json.load(f)
#     except json.JSONDecodeError:
#         USERS = {}

# def save_users():
#     with open(USER_DB_FILE, "w") as f:
#         json.dump(USERS, f, indent=4)

# # ---------------- 忘記密碼畫面 ----------------
# def forgot_password():
#     st.title("🔑 忘記密碼")

#     # 1️⃣ 輸入 email
#     email_input = st.text_input("請輸入註冊時的電子郵件")

#     # 按鈕觸發寄送驗證碼
#     if st.button("寄送驗證碼"):
#         found_user = None
#         for username, info in USERS.items():
#             if isinstance(info, dict) and info.get("email") == email_input:
#                 found_user = username
#                 break
        
#         if not found_user:
#             st.error("此電子郵件未註冊")
#         else:
#             # 產生 6 位數驗證碼
#             code = ''.join(random.choices(string.digits, k=6))
#             st.session_state['reset_user'] = found_user
#             st.session_state['reset_code'] = code
#             st.session_state['reset_email'] = email_input
#             st.success(f"驗證碼已寄送到 {email_input} (模擬)：{code}")

#     # 2️⃣ 如果驗證碼已產生，顯示驗證碼輸入與新密碼欄位
#     if 'reset_code' in st.session_state:
#         st.info(f"已寄送驗證碼到 {st.session_state['reset_email']} (模擬)")
#         code_input = st.text_input("請輸入驗證碼")
#         new_pw = st.text_input("新密碼", type="password")
#         confirm_pw = st.text_input("再次輸入新密碼", type="password")

#         def valid_password(pw):
#             return len(pw) >= 8 and any(c.isalpha() for c in pw) and any(c.isdigit() for c in pw)

#         if st.button("重設密碼"):
#             if code_input != st.session_state['reset_code']:
#                 st.error("驗證碼錯誤")
#             elif new_pw != confirm_pw:
#                 st.error("密碼不一致")
#             elif not valid_password(new_pw):
#                 st.warning("密碼至少8碼，需包含英文字母與數字")
#             else:
#                 # 更新密碼
#                 user = st.session_state['reset_user']
#                 USERS[user]['password'] = hashlib.sha256(new_pw.encode()).hexdigest()
#                 save_users()
#                 st.success("密碼已重設成功！請返回登入頁")
                
#                 # 清空 session 並回登入頁
#                 for key in ['reset_user', 'reset_code', 'reset_email']:
#                     st.session_state.pop(key)
                
#                 st.switch_page("pages/login.py")