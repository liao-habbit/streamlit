import streamlit as st
from auth import require_login, logout_button

require_login()
logout_button()

st.markdown("# Page 3")
