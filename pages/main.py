import streamlit as st
import pandas as pd
import numpy as np
import time
from auth import require_login, logout_button
import home
import page_2
require_login()
logout_button()
page = st.sidebar.selectbox(
    "pages",
    ["首頁", "視覺化1", "視覺化2", "設定頁面"]  # 可以自由指定頁面名稱
)
if page == "首頁":
    home.app()
elif page == "視覺化1":
    page_2.app()