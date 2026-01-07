import streamlit as st
from auth import require_login,logout_button

# --------- 登入保護 ---------
import streamlit as st
from auth import require_login, logout_button

require_login()
logout_button()

st.switch_page("pages/main.py")
