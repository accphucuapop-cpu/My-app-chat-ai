import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Siêu App Nhập Vai", page_icon="🧠")
st.title("🎭 Nhập Vai Với AI (Trí Nhớ Vĩnh Cửu)")

# --- KẾT NỐI BỘ NÃO AI ---
# Bạn dán cái API Key của bạn vào ô này trên giao diện web sau khi chạy
api_key = st.sidebar.text_input("Dán Gemini API Key vào đây:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # --- THIẾT LẬP NHÂN VẬT ---
    with st.sidebar:
        st.divider()
        char_name = st.text_input("Tên nhân vật:", "Tướng quân")
        char_setting = st.text_area("Cốt truyện & Tính cách (AI sẽ không bao giờ quên):", 
                                   "Bạn là một vị tướng quân thời xưa, dũng cảm, trung thành. Ngôn ngữ trang trọng.")
        
        if st.button("Xóa sạch trí nhớ"):
            st.session_state.chat_history = []
            st.rerun()

    # Khởi tạo lịch sử trò chuyện (Đây là nơi lưu trí nhớ)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Hiển thị các tin nhắn cũ
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"][0])

    # --- XỬ LÝ TRÒ CHUYỆN ---
    if prompt := st.chat_input("Nói gì đó với nhân vật..."):
        # Hiển thị tin nhắn người dùng
        st.chat_message("user").markdown(prompt)
        
        # Tạo chỉ dẫn hệ thống (System Instruction) để AI luôn nhớ vai
        system_instruction = f"HÃY NHỚ: Bạn là {char_name}. Bối cảnh của bạn: {char_setting}. Hãy luôn giữ đúng vai diễn này trong suốt cuộc trò chuyện."

        # Gửi toàn bộ lịch sử + cốt truyện cho AI
        try:
            # Gộp cốt truyện vào tin nhắn đầu tiên để AI luôn nhớ
            full_prompt = f"{system_instruction}\n\nNgười dùng nói: {prompt}"
            
            chat = model.start_chat(history=st.session_state.chat_history)
            response = chat.send_message(full_prompt)
            
            # Hiển thị phản hồi của AI
            with st.chat_message("assistant"):
                st.markdown(response.text)
            
            # Lưu vào lịch sử để lần sau AI đọc lại
            st.session_state.chat_history.append({"role": "user", "parts": [prompt]})
            st.session_state.chat_history.append({"role": "model", "parts": [response.text]})
            
        except Exception as e:
            st.error(f"Lỗi rồi đại ca ơi: {e}")
else:
    st.warning("👈 Bạn cần dán API Key vào thanh bên trái để bắt đầu trò chuyện nhé!")
