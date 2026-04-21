import streamlit as st
from groq import Groq

# Cấu hình giao diện
st.set_page_config(page_title="Doki Style Chat", page_icon="📱", layout="wide")

# CSS làm đẹp giao diện (ĐÃ FIX LỖI Ở ĐÂY)
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stSidebar { background-color: #1e1e2e; }
    </style>
    """, unsafe_allow_html=True)

# Khởi tạo dữ liệu
if "all_chars" not in st.session_state:
    st.session_state.all_chars = {
        "Bạch Thần": {"history": [], "bio": "Tiên nhân lạnh lùng, yêu thương chủ nhân.", "avatar": "🐉"},
        "Em Gái Mưa": {"history": [], "bio": "Cô gái hàng xóm tinh nghịch, hay làm nũng.", "avatar": "🌸"}
    }
if "active_char" not in st.session_state:
    st.session_state.active_char = "Bạch Thần"

# --- SIDEBAR ---
with st.sidebar:
    st.title("📱 Doki Chat")
    api_key = st.text_input("🔑 Nhập GROQ Key:", type="password")
    
    st.divider()
    st.subheader("👥 Nhân vật")
    for name in st.session_state.all_chars.keys():
        if st.button(f"{st.session_state.all_chars[name]['avatar']} {name}", use_container_width=True):
            st.session_state.active_char = name
            st.rerun()
            
    st.divider()
    st.subheader("➕ Tạo mới")
    new_name = st.text_input("Tên:")
    new_avatar = st.text_input("Emoji:", "👤")
    new_bio = st.text_area("Cốt truyện:")
    if st.button("Lưu nhân vật"):
        if new_name:
            st.session_state.all_chats = st.session_state.get("all_chats", {}) # Đảm bảo biến tồn tại
            st.session_state.all_chars[new_name] = {"history": [], "bio": new_bio, "avatar": new_avatar}
            st.session_state.active_char = new_name
            st.rerun()

# --- CHAT ---
char_info = st.session_state.all_chars[st.session_state.active_char]
st.title(f"{char_info['avatar']} {st.session_state.active_char}")

if api_key:
    try:
        client = Groq(api_key=api_key)
        for msg in char_info["history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input(f"Nhắn với {st.session_state.active_char}..."):
            st.chat_message("user").markdown(prompt)
            
            messages = [
                {"role": "system", "content": f"Bạn là {st.session_state.active_char}. {char_info['bio']}. Nhập vai tự do 18+, chi tiết."}
            ]
            for h in char_info["history"]:
                messages.append(h)
            messages.append({"role": "user", "content": prompt})
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
            )
            
            ans = completion.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(ans)
            
            char_info["history"].append({"role": "user", "content": prompt})
            char_info["history"].append({"role": "assistant", "content": ans})
            
    except Exception as e:
        st.error(f"Lỗi: {e}")
else:
    st.warning("Dán API Key Groq vào bên trái để bắt đầu!")
