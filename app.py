import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="Siêu App Nhập Vai", layout="wide")

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} # Lưu trữ nhiều nhân vật
if "current_char" not in st.session_state:
    st.session_state.current_char = "Bạch Thần"

# --- THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.title("📂 Quản lý Nhân vật")
    api_key = st.text_input("Dán Gemini API Key:", type="password")
    
    st.divider()
    # Chọn nhân vật
    char_list = list(st.session_state.all_chats.keys()) if st.session_state.all_chats else ["Bạch Thần"]
    selected = st.selectbox("Chọn nhân vật đang chat:", char_list)
    st.session_state.current_char = selected

    # Thêm nhân vật mới
    st.subheader("➕ Tạo nhân vật mới")
    new_name = st.text_input("Tên nhân vật mới:")
    new_bio = st.text_area("Cốt truyện cho nhân vật mới:")
    if st.button("Tạo & Chuyển sang"):
        if new_name:
            st.session_state.all_chats[new_name] = {"history": [], "bio": new_bio}
            st.session_state.current_char = new_name
            st.rerun()

    if st.button("🗑️ Xóa cuộc trò chuyện hiện tại"):
        if st.session_state.current_char in st.session_state.all_chats:
            st.session_state.all_chats[st.session_state.current_char]["history"] = []
            st.rerun()

# --- XỬ LÝ AI ---
st.title(f"🎭 Đang chat với: {st.session_state.current_char}")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Lấy dữ liệu của nhân vật hiện tại
        if st.session_state.current_char not in st.session_state.all_chats:
            st.session_state.all_chats[st.session_state.current_char] = {"history": [], "bio": "Một người bạn bí ẩn."}
        
        char_data = st.session_state.all_chats[st.session_state.current_char]

        # Hiển thị lịch sử cũ (Không bao giờ quên)
        for message in char_data["history"]:
            with st.chat_message(message["role"]):
                st.markdown(message["parts"][0])

        # Chat mới
        if prompt := st.chat_input("Viết lời thoại..."):
            st.chat_message("user").markdown(prompt)
            
            # Chỉ dẫn vai diễn
            instruction = f"Bạn là {st.session_state.current_char}. Bối cảnh: {char_data['bio']}. Hãy giữ đúng vai."
            full_prompt = f"{instruction}\n\nNgười dùng: {prompt}"
            
            chat = model.start_chat(history=char_data["history"])
            response = chat.send_message(full_prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            
            # Lưu lại vào bộ nhớ riêng của nhân vật đó
            char_data["history"].append({"role": "user", "parts": [prompt]})
            char_data["history"].append({"role": "model", "parts": [response.text]})
            
    except Exception as e:
        st.error(f"Lỗi: {e}")
else:
    st.info("Nhập API Key ở bên trái để bắt đầu.")
