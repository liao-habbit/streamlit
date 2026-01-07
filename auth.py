import streamlit as st 
def require_login():
    if not st.session_state.get("logged_in",False):
        st.switch_page("pages/login.py")

def logout_button():
    with st.sidebar:
        st.markdown("### 👤 使用者")
        st.write(st.sesssion_state.get("user",""))

        if st.button("🚪 登出"):
            st.session_state.clear()
            st.switch_page("pages/login.py")