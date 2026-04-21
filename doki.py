import streamlit as st
from groq import Groq

# 1. Cấu hình & Giao diện
st.set_page_config(page_title="Doki Premium Chat", page_icon="💖", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1e1e2e 0%, #11111b 100%); color: #cdd6f4; }
    [data-testid="stSidebar"] { background-color: #181825 !important; }
    [data-testid="stChatMessage"]:nth-child(even) { background-color: #313244 !important; border-radius: 20px 20px 5px 20px !important; }
    [data-testid="stChatMessage"]:nth-child(odd) { background-color: #f5c2e7 !important; color: #11111b !important; border-radius: 20px 20px 20px 5px !important; }
    [data-testid="stChatMessage"]:nth-child(odd) p { color: #11111b !important; }
    .stButton>button { border-radius: 10px; background-color: #f5c2e7; color: #11111b; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Khởi tạo dữ liệu
if "all_chars" not in st.session_state:
    st.session_state.all_chars = {"Bạch Thần": {"history": [], "bio": "Tiên nhân lạnh lùng, chiếm hữu.", "avatar": "🐉"}}
if "active_char" not in st.session_state:
    st.session_state.active_char = "Bạch Thần"

char_info = st.session_state.all_chars[st.session_state.active_char]

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #f5c2e7;'>💖 Doki Chat</h1>", unsafe_allow_html=True)
    api_key = st.text_input("🔑 GROQ KEY:", type="password")
    
    st.divider()
    st.subheader("🛠️ Chỉnh sửa khúc này")
    
    if len(char_info["history"]) >= 2:
        if st.button("🔄 Thử lại câu này (Regen)", use_container_width=True):
            # Xóa câu trả lời cuối của AI, giữ lại câu của User để nó tự chạy lại
            char_info["history"].pop() 
            st.session_state.retry_trigger = True
            st.rerun()
            
        if st.button("❌ Xóa cặp cuối", use_container_width=True):
            char_info["history"] = char_info["history"][:-2]
            st.rerun()

    if st.button("🧹 Reset toàn bộ", use_container_width=True):
        char_info["history"] = []
        st.rerun()

    st.divider()
    st.subheader("👥 Nhân vật")
    for name in st.session_state.all_chars.keys():
        if st.button(f"{st.session_state.all_chars[name]['avatar']} {name}", use_container_width=True):
            st.session_state.active_char = name
            st.rerun()

# --- KHUNG CHAT ---
st.markdown(f"<h2 style='color: #f5c2e7;'>{char_info['avatar']} {st.session_state.active_char}</h2>", unsafe_allow_html=True)

def call_ai(prompt_input, history):
    try:
        client = Groq(api_key=api_key)
        messages = [{"role": "system", "content": f"Bạn là {st.session_state.active_char}. {char_info['bio']}. Nhập vai 18+, chi tiết."}]
        messages.extend(history)
        messages.append({"role": "user", "content": prompt_input})
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.9
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Lỗi: {e}"

# Hiển thị lịch sử
for msg in char_info["history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý khi nhấn "Thử lại câu này"
if st.session_state.get("retry_trigger") and len(char_info["history"]) > 0:
    last_user_prompt = char_info["history"].pop()["content"] # Lấy câu user ra
    st.session_state.retry_trigger = False
    with st.chat_message("assistant"):
        with st.spinner("Đang nghĩ câu khác..."):
            new_ans = call_ai(last_user_prompt, char_info["history"])
            st.markdown(new_ans)
            char_info["history"].append({"role": "user", "content": last_user_prompt})
            char_info["history"].append({"role": "assistant", "content": new_ans})
            st.rerun()

# Nhập tin nhắn mới
if prompt := st.chat_input("Viết lời thoại..."):
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        ans = call_ai(prompt, char_info["history"])
        st.markdown(ans)
    char_info["history"].append({"role": "user", "content": prompt})
    char_info["history"].append({"role": "assistant", "content": ans})
