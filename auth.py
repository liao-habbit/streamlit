import streamlit as st 
import forgot_password 
def require_login():
    if not st.session_state.get("logged_in",False):
        st.switch_page("pages/login.py")

def logout_button():
    with st.sidebar:
        st.markdown(f"### 👤 使用者 {st.session_state.get("user","")}")
        if st.button("🚪 登出"):
            st.session_state.clear()
            st.switch_page("pages/login.py")

def go_to_register():
    st.switch_page("pages/account.py")

def back_to_login():
    st.switch_page("pages/login.py")

def go_to_forgot_password():
    forgot_password.forgot_password()