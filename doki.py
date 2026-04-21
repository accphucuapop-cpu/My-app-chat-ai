import streamlit as st
from groq import Groq
import json

# 1. Cấu hình trang
st.set_page_config(page_title="Doki Ultra - Bạch Thần", layout="wide")

# CSS làm đẹp giao diện
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ececec; }
    [data-testid="stChatMessage"] { border-radius: 10px; border-left: 3px solid #ff4b4b; background-color: #1a1a1a; }
    .stButton>button { width: 100%; background-color: #262626; color: #ff4b4b; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# 2. Khởi tạo dữ liệu
if "history" not in st.session_state:
    st.session_state.history = []

# Thông tin nhân vật (Cố định theo ý ông)
bio = """Bạch Thần (22t, 1m92): Quái vật thí nghiệm bị xích từ bé. Giết cha mẹ trốn thoát. 
8 múi, thô lỗ, tàn nhẫn, mạnh gấp 5 lần người thường. Hạ Lạc (20t, 1m5): Loli trắng nõn, răng thỏ."""
rules = "Dùng *: hành động, /: suy nghĩ, (): ngoài lời, []: tin nhắn. Luôn nhắc Địa điểm ở đầu."

# --- SIDEBAR ---
with st.sidebar:
    st.title("⛓️ DOKI CONTROL")
    api_key = st.text_input("🔑 Nhập GROQ Key:", type="password")
    loc = st.text_input("📍 Địa điểm:", value="Căn hẻm tối tăm")
    
    st.divider()
    st.subheader("🛠️ Công cụ")
    if st.button("🔄 Làm lại câu AI"):
        if len(st.session_state.history) >= 2:
            st.session_state.history.pop() # Xóa câu AI
            st.session_state.retry = True
            st.rerun()

    if st.button("🗑️ Xóa cặp cuối"):
        if len(st.session_state.history) >= 2:
            st.session_state.history = st.session_state.history[:-2]
            st.rerun()

    with st.expander("✏️ Sửa lời Hạ Lạc"):
        if len(st.session_state.history) >= 2:
            new_text = st.text_area("Nội dung mới:", value=st.session_state.history[-2]["content"])
            if st.button("Cập nhật & Diễn tiếp"):
                st.session_state.history = st.session_state.history[:-2]
                st.session_state.retry_prompt = new_text
                st.rerun()

    st.divider()
    # Nút Lưu/Backup
    data_str = json.dumps(st.session_state.history, ensure_ascii=False)
    st.download_button("📥 Tải Backup Chat", data_str, file_name="chat_backup.json")

# --- HÀM GỌI AI ---
def ask_ai(prompt):
    if not api_key: return "Nhập Key bên trái đã ông ơi!"
    try:
        client = Groq(api_key=api_key)
        sys_msg = f"Bạn là Bạch Thần. {bio} Địa điểm: {loc}. {rules} Nhập vai 18+ bạo, trần trụi, thô lỗ."
        msgs = [{"role": "system", "content": sys_msg}]
        msgs.extend(st.session_state.history)
        msgs.append({"role": "user", "content": prompt})
        
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, temperature=1.0)
        return res.choices[0].message.content
    except Exception as e: return f"Lỗi: {str(e)}"

# --- HIỂN THỊ KHUNG CHAT ---
st.header("🐉 Bạch Thần x Hạ Lạc")

# Hiển thị tin nhắn cũ
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý khi nhấn Làm lại hoặc Sửa
if "retry" in st.session_state:
    del st.session_state.retry
    last_p = st.session_state.history.pop()["content"]
    with st.chat_message("assistant"):
        a = ask_ai(last_p)
        st.markdown(a)
    st.session_state.history.append({"role": "user", "content": last_p})
    st.session_state.history.append({"role": "assistant", "content": a})

if "retry_prompt" in st.session_state:
    p = st.session_state.pop("retry_prompt")
    st.chat_message("user").markdown(p)
    with st.chat_message("assistant"):
        a = ask_ai(p)
        st.markdown(a)
    st.session_state.history.append({"role": "user", "content": p})
    st.session_state.history.append({"role": "assistant", "content": a})

# Ô nhập tin nhắn mới (KHUNG CHAT CHÍNH Ở ĐÂY)
if prompt := st.chat_input("Hạ Lạc nói gì đó..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        ans = ask_ai(prompt)
        st.markdown(ans)
    st.session_state.history.append({"role": "user", "content": prompt})
    st.session_state.history.append({"role": "assistant", "content": ans})
