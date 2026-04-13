import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import fitz  

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY not found. Please add it to your .env file.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;500;600&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    header[data-testid="stHeader"] { background: transparent; }
    h1 {
        font-family: 'Space Mono', monospace !important;
        color: #e0e0ff !important;
        text-align: center;
        letter-spacing: -1px;
        padding-bottom: 4px;
    }
    .subtitle {
        text-align: center;
        color: #7878aa;
        font-size: 0.85rem;
        margin-top: -12px;
        margin-bottom: 24px;
        font-family: 'Space Mono', monospace;
    }
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 16px !important;
        margin: 6px 0 !important;
        backdrop-filter: blur(8px);
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        border-left: 3px solid #6c63ff !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-left: 3px solid #00d4aa !important;
    }
    [data-testid="stChatInputTextArea"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(108,99,255,0.4) !important;
        border-radius: 12px !important;
        color: #e0e0ff !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 26, 0.8) !important;
        border-right: 1px solid rgba(255,255,255,0.07) !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p { color: #b0b0d0 !important; font-size: 0.85rem; }
    .stButton > button {
        background: rgba(108,99,255,0.2) !important;
        border: 1px solid rgba(108,99,255,0.5) !important;
        color: #c0b8ff !important;
        border-radius: 10px !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.8rem !important;
    }
    .stButton > button:hover {
        background: rgba(108,99,255,0.4) !important;
        border-color: #6c63ff !important;
    }
    [data-testid="stMarkdownContainer"] p { color: #d0d0ee; line-height: 1.65; }
    .token-badge {
        background: rgba(0, 212, 170, 0.1);
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 8px;
        padding: 4px 10px;
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #00d4aa;
        text-align: center;
        margin-top: 8px;
    }
    .file-badge {
        background: rgba(108,99,255,0.1);
        border: 1px solid rgba(108,99,255,0.3);
        border-radius: 8px;
        padding: 6px 12px;
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #a89fff;
        margin-bottom: 8px;
        display: inline-block;
    }
    hr { border-color: rgba(255,255,255,0.07) !important; }
</style>
""", unsafe_allow_html=True)


def extract_file_content(uploaded_file):
    """Returns (api_content_block, display_label, is_image)"""
    fname = uploaded_file.name
    ftype = uploaded_file.type
    raw = uploaded_file.read()

    if ftype.startswith("image/"):
        b64 = base64.b64encode(raw).decode("utf-8")
        return (
            {"type": "image_url", "image_url": {"url": f"data:{ftype};base64,{b64}"}},
            f"🖼️ {fname}",
            True,
        )

    if ftype == "application/pdf":
        try:
            doc = fitz.open(stream=raw, filetype="pdf")
            text = "\n\n".join(page.get_text() for page in doc)
            doc.close()
        except Exception:
            text = "[Could not extract PDF text]"
        return (
            {"type": "text", "text": f"[File: {fname}]\n\n{text}"},
            f"📄 {fname}",
            False,
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1", errors="replace")

    return (
        {"type": "text", "text": f"[File: {fname}]\n\n{text}"},
        f"📎 {fname}",
        False,
    )


with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0,
        help="gpt-4o-mini is fast & cheap. gpt-4o is more powerful.",
    )

    temperature = st.slider(
        "Temperature (creativity)",
        min_value=0.0, max_value=2.0, value=0.7, step=0.1,
    )

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, friendly, and concise AI assistant. Answer clearly and honestly.",
        height=100,
    )

    st.markdown("---")
    st.markdown("### 📁 Upload a File")

    uploaded_file = st.file_uploader(
        "Attach to your next message",
        type=["txt", "pdf", "py", "js", "ts", "csv", "md", "json",
              "png", "jpg", "jpeg", "gif", "webp"],
        help="Supports text, code, PDF, CSV, and images.",
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.75rem; color:#555577;'>Built with Streamlit + OpenAI</p>",
        unsafe_allow_html=True,
    )


# ── Main UI ───────────────────────────────────────────────────────────────────
st.markdown("# 💬 AI Chatbot")
st.markdown('<p class="subtitle">Chat freely — attach files too</p>', unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render existing messages ──────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("file_label"):
            st.markdown(
                f'<div class="file-badge">{msg["file_label"]}</div>',
                unsafe_allow_html=True,
            )
        content = msg["content"]
        if isinstance(content, str):
            st.markdown(content)
        else:
            for part in content:
                if part["type"] == "text":
                    st.markdown(part["text"])
                elif part["type"] == "image_url":
                    # Re-display the image from base64
                    url = part["image_url"]["url"]
                    st.image(url, width=260)

# ── File preview above chat input ─────────────────────────────────────────────
if uploaded_file:
    st.markdown(
        f'<div class="file-badge">📎 Ready to send: <b>{uploaded_file.name}</b></div>',
        unsafe_allow_html=True,
    )
    if uploaded_file.type.startswith("image/"):
        st.image(uploaded_file, width=240)

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your message here..."):

    # Build user content
    file_label = None
    if uploaded_file:
        uploaded_file.seek(0)
        api_block, file_label, is_image = extract_file_content(uploaded_file)
        if is_image:
            user_content = [{"type": "text", "text": prompt}, api_block]
        else:
            user_content = [api_block, {"type": "text", "text": prompt}]
    else:
        user_content = prompt

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_content,
        "file_label": file_label,
    })

    # Display user message
    with st.chat_message("user"):
        if file_label:
            st.markdown(
                f'<div class="file-badge">{file_label}</div>',
                unsafe_allow_html=True,
            )
        st.markdown(prompt)

    # API messages (strip display-only keys)
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # Call OpenAI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *api_messages,
                    ],
                )

                reply = response.choices[0].message.content
                usage = response.usage

                st.markdown(reply)
                st.markdown(
                    f'<div class="token-badge">🔢 '
                    f'prompt: {usage.prompt_tokens} · '
                    f'completion: {usage.completion_tokens} · '
                    f'total: {usage.total_tokens}</div>',
                    unsafe_allow_html=True,
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                })

            except Exception as e:
                st.error(f"❌ Error: {e}")