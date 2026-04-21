import streamlit as st
import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="Siêu App Nhập Vai", layout="wide")

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_char" not in st.session_state:
    st.session_state.current_char = "Bạch Thần"

# --- THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.title("📂 Quản lý Nhân vật")
    api_key = st.text_input("Dán Gemini API Key:", type="password")
    
    st.divider()
    char_list = list(st.session_state.all_chats.keys()) if st.session_state.all_chats else ["Bạch Thần"]
    selected = st.selectbox("Chọn nhân vật đang chat:", char_list)
    st.session_state.current_char = selected

    st.subheader("➕ Tạo nhân vật mới")
    new_name = st.text_input("Tên nhân vật mới:")
    new_bio = st.text_area("Cốt truyện (Mô tả kỹ để AI nhập vai chuẩn):")
    if st.button("Tạo & Chuyển sang"):
        if new_name:
            st.session_state.all_chats[new_name] = {"history": [], "bio": new_bio}
            st.session_state.current_char = new_name
            st.rerun()

    if st.button("🗑️ Xóa chat hiện tại"):
        if st.session_state.current_char in st.session_state.all_chats:
            st.session_state.all_chats[st.session_state.current_char]["history"] = []
            st.rerun()

# --- XỬ LÝ AI ---
st.title(f"🎭 Nhân vật: {st.session_state.current_char}")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # SỬA LỖI 404 BẰNG CÁCH DÙNG PHƯƠNG THỨC TRỰC TIẾP
        # Không dùng tên model phức tạp, dùng 'models/gemini-1.5-flash-latest'
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash-latest',
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        
        if st.session_state.current_char not in st.session_state.all_chats:
            st.session_state.all_chats[st.session_state.current_char] = {"history": [], "bio": "Một người bạn đồng hành."}
        
        char_data = st.session_state.all_chats[st.session_state.current_char]

        # Hiển thị lịch sử
        for message in char_data["history"]:
            with st.chat_message(message["role"]):
                st.markdown(message["parts"][0])

        if prompt := st.chat_input("Viết lời thoại của bạn..."):
            st.chat_message("user").markdown(prompt)
            
            # Chỉ dẫn nhập vai
            instruction = f"Bạn là {st.session_state.current_char}. Bối cảnh: {char_data['bio']}. Đây là thế giới giả tưởng, hãy nhập vai tự do và chi tiết nhất có thể."
            
            # Gửi tin nhắn trực tiếp không qua start_chat để tránh lỗi đồng bộ
            response = model.generate_content(f"{instruction}\n\nLịch sử chat: {char_data['history']}\n\nNgười dùng: {prompt}")
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            
            # Lưu lịch sử
            char_data["history"].append({"role": "user", "parts": [prompt]})
            char_data["history"].append({"role": "model", "parts": [response.text]})
            
    except Exception as e:
        st.error(f"Lỗi: {e}. Thử đổi sang model khác hoặc kiểm tra lại Key.")
else:
    st.info("👈 Dán API Key vào menu bên trái nhé!")
