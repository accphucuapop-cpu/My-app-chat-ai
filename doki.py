import streamlit as st
from groq import Groq

# 1. Giao diện & CSS Dark Mode
st.set_page_config(page_title="Doki Premium - Bạch Thần", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ececec; }
    [data-testid="stChatMessage"] { border-radius: 10px; border-left: 3px solid #ff4b4b; background-color: #1a1a1a; }
    .stChatInputContainer { background-color: #0d0d0d !important; }
    .stButton>button { width: 100%; background-color: #262626; color: #ff4b4b; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# 2. Thiết lập nhân vật chi tiết (Dữ liệu cố định)
if "all_chars" not in st.session_state:
    st.session_state.all_chars = {
        "Bạch Thần": {
            "history": [],
            "bio": """
            Bạch Thần (22t, 1m92): Bị cha mẹ xích và tiêm thuốc thí nghiệm từ bé. Giết cha mẹ lúc 22t để trốn thoát.
            Đặc điểm: 8 múi, đẹp trai, kiện lời, thô lỗ, cọc cằn, tàn nhẫn, thông minh cực đỉnh, nhanh nhẹn gấp 5 lần người thường. 
            Không biết gì về thế giới bên ngoài, đa nghi, cảnh giác cao.
            Hạ Lạc (20t, 1m5): Loli, mặt baby, body ngon, trắng nõn, răng thỏ, dễ thương, thích đồ ngọt.
            """,
            "rules": "Sử dụng *: hành động, /: suy nghĩ, (): ngoài lời, []: tin nhắn. Luôn nhắc Địa điểm ở đầu.",
            "location": "Căn hẻm tối tăm, ẩm ướt"
        }
    }
if "active_char" not in st.session_state:
    st.session_state.active_char = "Bạch Thần"

char_info = st.session_state.all_chars[st.session_state.active_char]

# Sidebar quản lý
with st.sidebar:
    st.title("⛓️ DOKI - LAB")
    api_key = st.text_input("🔑 Nhập GROQ Key:", type="password")
    char_info["location"] = st.text_input("📍 Địa điểm:", value=char_info["location"])
    st.divider()
    if st.button("🗑️ Reset Khúc Này"):
        char_info["history"] = char_info["history"][:-2]
        st.rerun()
    if st.button("🧹 Reset Toàn Bộ"):
        char
