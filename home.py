import streamlit as st
from pathlib import Path
from utils.db import add_file, file_exists, get_user_files, delete_file
from auth import require_login
from datetime import datetime
import hashlib
from PIL import Image
from streamlit_image_gallery import streamlit_image_gallery
import base64
from io import BytesIO
import glob
# ---------------- 登入保護 ----------------
def app():
    require_login()

    # 取得登入使用者資訊
    current_user = st.session_state.get("username")
    user_id = st.session_state.get("user_id")
    if not current_user or not user_id:
        st.warning("請先登入！")
        st.stop()

    st.subheader("🏠 主頁面")

    # ---------------- 上傳圖片 ----------------
    st.subheader("📤 上傳圖片（可多選）")
    uploaded_files = st.file_uploader(
        "",
        type=["png", "jpg", "jpeg", "gif"],
        accept_multiple_files=True,
        key="uploaded_files_multi"
    )

    # 暫存上傳檔案
    if uploaded_files:
        st.session_state['pending_uploads'] = uploaded_files

    pending = st.session_state.get('pending_uploads', [])

    if st.button("開始上傳", key="upload_button"):
        if not pending:
            st.info("沒有檔案可上傳")
        else:
            uploads_dir = Path("uploads") / str(user_id)
            uploads_dir.mkdir(parents=True, exist_ok=True)

            total_files = len(pending)
            progress_bar = st.progress(0)
            status_text = st.empty()

            for idx, uploaded_file in enumerate(pending, start=1):
                file_bytes = uploaded_file.getbuffer()
                file_hash = hashlib.sha256(file_bytes).hexdigest()

                # 已存在就跳過
                if file_exists(user_id, file_hash):
                    status_text.text(f"跳過已存在檔案：{uploaded_file.name}")
                    progress_bar.progress(idx / total_files)
                    continue

                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                file_path = uploads_dir / f"{timestamp}_{uploaded_file.name}"

                with open(file_path, "wb") as f:
                    f.write(file_bytes)

                add_file(user_id, file_path.name, file_hash)
                progress_bar.progress(idx / total_files)
                status_text.text(f"上傳 {uploaded_file.name} 完成")

            status_text.text("🎉 所有圖片處理完成")
            st.success("圖片上傳完成！")
            st.session_state['pending_uploads'] = []  # ✅ 清空暫存

    st.subheader("📂 已上傳圖片")
    def load_images():
        image_files = glob.glob("*.jpg")
        st.write(len(image_files))
        for image_file in image_files:
            st.wrtie(image_file)
        return  
    image_files = load_images()