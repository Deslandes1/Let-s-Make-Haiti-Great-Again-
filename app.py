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

# Custom CSS - Light Blue Theme
st.markdown("""
<style>
    /* Main background and text */
    .stApp {
        background: linear-gradient(145deg, #e6f3ff 0%, #cce4f7 100%);
        color: #1a2a3a;
    }
    [data-testid="stSidebar"] {
        background: #d4e9ff;
        border-right: 1px solid #a0c4e8;
    }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption {
        color: #1a2a3a !important;
    }
    h1, h2, h3, h4, h5, h6, p, li, .stMarkdown, .stCaption, label {
        color: #1a2a3a !important;
    }
    .main-header {
        text-align: center;
        font-size: 3rem;
        color: #0066cc;
        font-weight: bold;
        margin-bottom: 0;
        text-shadow: 0 0 30px rgba(0,102,204,0.15);
    }
    .sub-header {
        text-align: center;
        font-size: 1.2rem;
        color: #1a2a3a;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    .profile-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #0066cc;
        display: block;
        margin: 0 auto 8px auto;
        box-shadow: 0 4px 12px rgba(0,80,160,0.2);
    }
    .profile-name {
        color: #0066cc;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    .profile-title {
        color: #2a4a6a;
        text-align: center;
        font-size: 0.9rem;
        margin-top: 0;
    }
    .contact-info {
        background: rgba(255,255,255,0.6);
        border: 1px solid #88bce0;
        border-radius: 8px;
        padding: 12px;
        font-size: 0.85rem;
        color: #1a2a3a;
    }
    .contact-info strong {
        color: #0066cc;
    }
    .logo-container {
        text-align: center;
        margin: 10px 0;
    }
    .logo-text {
        font-size: 1.4rem;
        font-weight: bold;
        color: #0066cc;
        text-shadow: 0 0 20px rgba(0,102,204,0.2);
        margin-top: 6px;
    }
    .embed-container {
        position: relative;
        padding-bottom: 56.25%;
        height: 0;
        overflow: hidden;
        max-width: 100%;
        background: #000;
        border-radius: 12px;
    }
    .embed-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4da6ff, #0066cc) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0,80,160,0.2);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(0,80,160,0.4);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff !important;
        color: #1a2a3a !important;
        border: 1px solid #88bce0 !important;
        border-radius: 8px !important;
    }
    .footer {
        text-align: center;
        padding: 20px 0;
        border-top: 1px solid #88bce0;
        margin-top: 30px;
        color: #2a4a6a;
        font-size: 0.9rem;
    }
    .stAlert {
        padding: 6px 12px;
        margin-top: 4px;
        margin-bottom: 4px;
    }
    /* globe container */
    .globe-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 10px 0;
    }
    .globe-wrapper iframe {
        border: none;
        border-radius: 50%;
        box-shadow: 0 4px 20px rgba(0,102,204,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🇭🇹 Let\'s Make Haiti Great Again</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload your vision, speak your truth – powered by AI</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Profile Picture
    st.markdown("""
    <img src="https://raw.githubusercontent.com/Deslandes1/Let-s-Make-Haiti-Great-Again-/main/Gesner%20Deslandes.png" class="profile-img">
    <h3 class="profile-name">Gesner Deslandes</h3>
    <p class="profile-title">Founder, Let's Make Haiti Great Again</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Logo: Spinning Blue Globe
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    # Embed the globe animation (Three.js)
    globe_html = """
    <div class="globe-wrapper">
        <div id="globe-container" style="width:150px;height:150px;margin:0 auto;"></div>
        <div class="logo-text">🧤 Blue Glove Spinning</div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        (function() {
            var container = document.getElementById('globe-container');
            if (!container) return;
            var scene = new THREE.Scene();
            var camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
            camera.position.z = 3;
            var renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
            renderer.setSize(150, 150);
            renderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(renderer.domElement);

            // Blue sphere
            var geometry = new THREE.SphereGeometry(1, 48, 48);
            var material = new THREE.MeshPhongMaterial({
                color: 0x3388ff,
                emissive: 0x0044aa,
                emissiveIntensity: 0.3,
                shininess: 40,
                transparent: true,
                opacity: 0.95
            });
            var sphere = new THREE.Mesh(geometry, material);
            scene.add(sphere);

            // Rings (rotating)
            var ringGeo = new THREE.TorusGeometry(1.15, 0.025, 16, 32);
            var ringMat = new THREE.MeshBasicMaterial({color: 0x88ccff, transparent: true, opacity: 0.6});
            var ring1 = new THREE.Mesh(ringGeo, ringMat);
            ring1.rotation.x = Math.PI/2;
            scene.add(ring1);

            var ring2 = ring1.clone();
            ring2.rotation.z = Math.PI/3;
            scene.add(ring2);

            var ring3 = ring1.clone();
            ring3.rotation.z = -Math.PI/3;
            scene.add(ring3);

            // Lights
            var light1 = new THREE.DirectionalLight(0xffffff, 1);
            light1.position.set(1, 1, 1);
            scene.add(light1);
            var light2 = new THREE.DirectionalLight(0x88aaff, 0.6);
            light2.position.set(-1, 0.5, -1);
            scene.add(light2);
            var ambient = new THREE.AmbientLight(0x446688, 0.3);
            scene.add(ambient);

            function animate() {
                requestAnimationFrame(animate);
                sphere.rotation.y += 0.008;
                ring1.rotation.y += 0.008;
                ring2.rotation.y += 0.008;
                ring3.rotation.y += 0.008;
                renderer.render(scene, camera);
            }
            animate();
        })();
    </script>
    """
    st.components.v1.html(globe_html, height=220)

    st.markdown("---")

    # Contact Info
    st.markdown("""
    <div class="contact-info">
        <strong>📧 Email:</strong> deslandes78@gmail.com<br>
        <strong>📱 Phone:</strong> (509) 4738-5663<br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.header("📝 Your Message")
    script_text = st.text_area(
        "Paste your text (French or English)",
        height=200,
        placeholder="Écris ton message pour bâtir un Haïti meilleur..."
    )

    lang = st.selectbox("Language", ["fr", "en"], index=0)

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
        # Auto-detect YouTube and convert to embed
        if "youtube.com/watch?v=" in embed_url:
            video_id = embed_url.split("v=")[1].split("&")[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
        elif "youtu.be/" in embed_url:
            video_id = embed_url.split("youtu.be/")[1].split("?")[0]
            embed_url = f"https://www.youtube.com/embed/{video_id}"
        # Dropbox: change ?dl=0 to ?raw=1
        if "dropbox.com" in embed_url and "dl=0" in embed_url:
            embed_url = embed_url.replace("dl=0", "raw=1")
        # Display the embed
        st.markdown(f'<div class="embed-container"><iframe src="{embed_url}" frameborder="0" allowfullscreen></iframe></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Made with ❤️ by Gesner Deslandes | Let's Make Haiti Great Again 🇭🇹</p>
    <p style="font-size:0.8rem; color:#2a4a6a;">📧 deslandes78@gmail.com | 📱 (509) 4738-5663</p>
</div>
""", unsafe_allow_html=True)
