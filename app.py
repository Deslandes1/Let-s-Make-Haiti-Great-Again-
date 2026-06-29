import streamlit as st
import tempfile
import os
from gtts import gTTS
import base64
import time

# Page config
st.set_page_config(
    page_title="Let's Make Haiti Great Again",
    layout="wide",
    page_icon="🇭🇹"
)

# Custom CSS for a motivational, patriotic look
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 3rem;
        color: #1a2a6c;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        font-size: 1.2rem;
        color: #2c3e50;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    .sidebar .sidebar-content {
        background: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🇭🇹 Let\'s Make Haiti Great Again</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload your vision, speak your truth – powered by AI</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📝 Your Message")
    script_text = st.text_area(
        "Paste your text (French or English)",
        height=200,
        placeholder="Écris ton message pour bâtir un Haïti meilleur..."
    )

    # TTS language selection (auto-detect or manual)
    lang = st.selectbox("Language", ["fr", "en"], index=0)

    # Female voice option (gTTS doesn't support gender, but we can use pyttsx3 fallback)
    use_female = st.checkbox("Female voice (prefer if available)", value=True)

    # Generate audio button
    if st.button("🔊 Generate & Play Audio"):
        if script_text.strip():
            with st.spinner("Generating voice..."):
                try:
                    # Use gTTS (fast, online)
                    tts = gTTS(text=script_text, lang=lang, slow=False)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                        tts.save(f.name)
                        audio_file = f.name
                    st.session_state['audio_file'] = audio_file
                    st.session_state['audio_text'] = script_text
                    st.success("✅ Voice generated!")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please paste some text first.")

    # Display audio if exists
    if 'audio_file' in st.session_state and os.path.exists(st.session_state['audio_file']):
        st.audio(st.session_state['audio_file'], format="audio/mp3", autoplay=True)
        st.caption(f"🔊 Speaking: {st.session_state['audio_text'][:100]}...")

    st.markdown("---")
    st.header("📺 Live TikTok Embed")
    tiktok_url = st.text_input("Paste TikTok Live URL", placeholder="https://www.tiktok.com/@username/live")
    if tiktok_url:
        st.markdown(f'<iframe src="{tiktok_url}" width="100%" height="400" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

# Main area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🖼️ Upload Media")
    uploaded_file = st.file_uploader("Choose an image or video", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])

    if uploaded_file is not None:
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.read())
            media_path = tmp.name

        # Display based on file type
        if uploaded_file.type.startswith("video"):
            st.video(media_path, format="video/mp4")
        else:
            st.image(media_path, use_column_width=True)
    else:
        st.info("👆 Upload an image or video to get started.")

with col2:
    st.subheader("🎯 Your Mission")
    st.markdown("""
    - **Upload** your media (a photo of a project, a video of a community effort).
    - **Write** a compelling message in the sidebar.
    - **Generate** the female AI voice and let it speak your words.
    - **Embed** your TikTok live stream to reach the world.

    Together, we build a new Haiti – with technology, passion, and unity.
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Gesner Deslandes | Let's Make Haiti Great Again 🇭🇹")
