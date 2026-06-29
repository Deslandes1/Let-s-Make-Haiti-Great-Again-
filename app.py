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
    .embed-container {
        position: relative;
        padding-bottom: 56.25%; /* 16:9 */
        height: 0;
        overflow: hidden;
        max-width: 100%;
        background: #000;
    }
    .embed-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
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

    lang = st.selectbox("Language", ["fr", "en"], index=0)
    use_female = st.checkbox("Female voice (prefer if available)", value=True)

    if st.button("🔊 Generate & Play Audio"):
        if script_text.strip():
            with st.spinner("Generating voice..."):
                try:
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

    if 'audio_file' in st.session_state and os.path.exists(st.session_state['audio_file']):
        st.audio(st.session_state['audio_file'], format="audio/mp3", autoplay=True)
        st.caption(f"🔊 Speaking: {st.session_state['audio_text'][:100]}...")

    st.markdown("---")
    st.header("📺 Live TikTok Embed (optional)")
    tiktok_url = st.text_input("Paste TikTok Live URL", placeholder="https://www.tiktok.com/@username/live")
    if tiktok_url:
        st.markdown(f'<iframe src="{tiktok_url}" width="100%" height="400" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

# Main area – choose between Upload or Embed
tab1, tab2 = st.tabs(["📤 Upload Media", "🔗 Embed Link"])

with tab1:
    st.subheader("Upload an image or video")
    uploaded_file = st.file_uploader("Choose file", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.read())
            media_path = tmp.name

        if uploaded_file.type.startswith("video"):
            st.video(media_path, format="video/mp4")
        else:
            st.image(media_path, use_column_width=True)

with tab2:
    st.subheader("Paste an embed link (YouTube, Vimeo, Dropbox, etc.)")
    embed_url = st.text_input("URL", placeholder="https://www.youtube.com/embed/... or https://www.dropbox.com/s/...")
    if embed_url:
        # Try to auto-detect if it's a YouTube watch link and convert to embed
        if "youtube.com/watch?v=" in embed_url:
            video_id = embed_url.split("v=")[1].split("&")[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
        elif "youtu.be/" in embed_url:
            video_id = embed_url.split("youtu.be/")[1].split("?")[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
        # For Dropbox, change ?dl=0 to ?raw=1
        if "dropbox.com" in embed_url and "dl=0" in embed_url:
            embed_url = embed_url.replace("dl=0", "raw=1")
        # Display the embed
        st.markdown(f'<div class="embed-container"><iframe src="{embed_url}" frameborder="0" allowfullscreen></iframe></div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Gesner Deslandes | Let's Make Haiti Great Again 🇭🇹")
