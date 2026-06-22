import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

from fraud_detector.scam_classifier import analyze_text, analyze_image
from graph_engine.fraud_graph import draw_fraud_graph
from geospatial.heatmap import generate_heatmap
from chatbot.rag import get_copilot_response
from streamlit_folium import st_folium
from PIL import Image

# ── Page config
st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS — United24 brutalist style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

    html, body, [class*="css"], .stApp, .stMarkdown, p, div, span, label {
        font-family: 'Barlow', sans-serif !important;
    }

    /* ── Base */
    .stApp { background-color: #000000 !important; color: #ffffff; }
    .stSidebar { background-color: #0a0a0a !important; border-right: 1px solid #222 !important; }
    .stSidebar > div { background-color: #0a0a0a !important; }

    /* ── Metric cards — hard border, no radius */
    .metric-card {
        background: #000;
        border: 1px solid #333;
        border-top: 3px solid #fff;
        border-radius: 0;
        padding: 24px 20px;
        text-align: left;
        margin-bottom: 0;
    }
    .metric-card .value {
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 2.6rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        line-height: 1;
    }
    .metric-card .value.yellow { color: #FFD700; }
    .metric-card .value.red    { color: #ff4444; }
    .metric-card .label {
        font-size: 0.72rem;
        color: #666;
        margin-top: 8px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-family: 'Barlow', sans-serif !important;
    }

    /* ── Risk levels — brutalist flat */
    .risk-critical { background:#1a0000; border-left:4px solid #ff2222; border-radius:0; padding:16px; margin:8px 0; }
    .risk-high     { background:#1a0a00; border-left:4px solid #ff7700; border-radius:0; padding:16px; margin:8px 0; }
    .risk-medium   { background:#111100; border-left:4px solid #FFD700; border-radius:0; padding:16px; margin:8px 0; }
    .risk-low      { background:#001a00; border-left:4px solid #33ff55; border-radius:0; padding:16px; margin:8px 0; }

    /* ── Tags — sharp pill replaced by hard badge */
    .tag {
        display: inline-block;
        background: #111;
        border: 1px solid #333;
        border-radius: 0;
        padding: 2px 10px;
        margin: 2px;
        font-size: 0.68rem;
        color: #aaa;
        font-family: 'Barlow', sans-serif !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* ── Section titles */
    .section-title {
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 2.4rem;
        font-weight: 800;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid #222;
        padding-bottom: 12px;
        margin-bottom: 24px;
    }

    /* ── Chat bubbles */
    .chat-user {
        background: #111;
        border: 1px solid #333;
        border-radius: 0;
        padding: 12px 16px;
        margin: 6px 0;
        max-width: 80%;
        margin-left: auto;
        color: #fff;
        font-size: 0.9rem;
    }
    .chat-ai {
        background: #0a0a0a;
        border: 1px solid #222;
        border-left: 3px solid #FFD700;
        border-radius: 0;
        padding: 12px 16px;
        margin: 6px 0;
        max-width: 85%;
        color: #ddd;
        font-size: 0.9rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* ── Buttons — yellow CTA like U24 DONATE */
    .stButton > button {
        background: #FFD700 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 10px 28px !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        transition: background 0.15s ease !important;
    }
    .stButton > button:hover {
        background: #ffe94d !important;
    }

    /* ── Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #555 !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        border-radius: 0 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #fff !important;
        border-bottom-color: #FFD700 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid #222 !important;
        background: #000 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #FFD700 !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        background-color: #222 !important;
    }

    /* ── Inputs */
    .stTextArea textarea, .stTextInput input {
        background: #0a0a0a !important;
        border: 1px solid #333 !important;
        border-radius: 0 !important;
        color: #fff !important;
        font-family: 'Barlow', sans-serif !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #FFD700 !important;
        box-shadow: none !important;
    }
    .stSelectbox > div > div {
        background: #0a0a0a !important;
        border: 1px solid #333 !important;
        border-radius: 0 !important;
        color: #fff !important;
    }

    /* ── Native Streamlit metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: 0 !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.7rem !important;
        color: #555 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }

    /* ── HR */
    hr { border-color: #1a1a1a !important; margin: 20px 0 !important; }

    /* ── Sidebar radio nav */
    .stRadio label {
        color: #aaa !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    .stRadio [data-testid="stMarkdownContainer"] p {
        color: #aaa !important;
    }

    /* ── Spinner */
    .stSpinner > div { border-top-color: #FFD700 !important; }

    /* ── Alerts */
    .stSuccess { background: rgba(51,255,85,0.08) !important; border-left: 3px solid #33ff55 !important; border-radius: 0 !important; color: #33ff55 !important; }
    .stError   { background: rgba(255,34,34,0.08) !important; border-left: 3px solid #ff2222 !important; border-radius: 0 !important; }
    .stWarning { background: rgba(255,215,0,0.08) !important;  border-left: 3px solid #FFD700 !important; border-radius: 0 !important; }

    /* ── File uploader */
    [data-testid="stFileUploader"] {
        border: 1px dashed #333 !important;
        border-radius: 0 !important;
        background: #0a0a0a !important;
    }

    /* ── Heading overrides inside markdown */
    h1, h2, h3 {
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color: #fff !important;
    }
</style>
""", unsafe_allow_html=True)


# ── HELPER FUNCTION
def display_result(result):
    risk = result.get("risk_level", "Low")
    score = result.get("risk_score", 0)
    is_scam = result.get("is_scam", False)
    scam_type = result.get("scam_type", "Unknown")
    patterns = result.get("detected_patterns", [])
    explanation = result.get("explanation", "")
    actions = result.get("recommended_actions", [])

    risk_class = {"Critical": "risk-critical", "High": "risk-high",
                  "Medium": "risk-medium", "Low": "risk-low"}.get(risk, "risk-low")
    risk_icon = {"Critical": "⚠ CRITICAL", "High": "▲ HIGH",
                 "Medium": "◆ MEDIUM", "Low": "✓ LOW"}.get(risk, "LOW")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div style='font-family:Barlow Condensed,sans-serif;font-size:1.4rem;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#fff;border-bottom:1px solid #222;padding-bottom:8px;margin-bottom:16px'>Analysis Result</div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Risk Score", f"{score}%")
    with col2:
        st.metric("Risk Level", risk_icon)
    with col3:
        st.metric("Verdict", "SCAM DETECTED" if is_scam else "✓ SAFE")

    st.markdown(f"<div class='{risk_class}'>", unsafe_allow_html=True)
    st.markdown(f"**Scam Type:** {scam_type}")
    if patterns:
        st.markdown("**Detected Patterns:**")
        for p in patterns:
            st.markdown(f"- {p}")
    st.markdown(f"**Explanation:** {explanation}")
    st.markdown("</div>", unsafe_allow_html=True)

    if actions:
        st.markdown("""<div style='font-family:Barlow Condensed,sans-serif;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#FFD700;margin:16px 0 8px'>Recommended Actions</div>""", unsafe_allow_html=True)
        for i, action in enumerate(actions, 1):
            st.markdown(f"**{i}.** {action}")

    if is_scam:
        st.error("DO NOT TRANSFER MONEY. Report at cybercrime.gov.in or call 1930.")
    else:
        st.success("This message appears safe. Stay vigilant.")


# ── Sidebar
with st.sidebar:
    st.markdown("""
    <div style='padding: 28px 4px 16px'>
        <div style='font-family: Barlow Condensed, sans-serif; font-size:2rem; font-weight:800; color:#fff; letter-spacing:2px; text-transform:uppercase; line-height:1'>SENTINEL<span style='color:#FFD700'>AI</span></div>
        <div style='font-size:0.65rem; color:#444; letter-spacing:3px; text-transform:uppercase; margin-top:4px; font-family: Barlow, sans-serif'>Digital Public Safety</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1a1a1a;margin:0 0 12px'>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Dashboard", "Citizen Fraud Shield", "Fraud Network Graph",
         "Crime Heatmap", "Law Enforcement Copilot"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#1a1a1a;margin:16px 0 12px'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#444; padding:4px 0; line-height:2; font-family:Barlow,sans-serif; letter-spacing:0.5px'>
        <div style='color:#FFD700; font-family:Barlow Condensed,sans-serif; font-weight:700; letter-spacing:2px; text-transform:uppercase; font-size:0.75rem; margin-bottom:4px'>Quick Stats 2024</div>
        1.14M cyber complaints<br>
        Rs 1,776 Cr lost to digital arrest<br>
        60% YoY increase<br>
        <div style='color:#FFD700; font-family:Barlow Condensed,sans-serif; font-weight:700; letter-spacing:2px; text-transform:uppercase; font-size:0.75rem; margin:10px 0 4px'>Report Fraud</div>
        cybercrime.gov.in<br>
        Helpline: 1930
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE 1 - DASHBOARD
# ══════════════════════════════════════════════════════════
if page == "Dashboard":
    st.markdown("""
    <div style='padding: 40px 0 16px; border-bottom: 1px solid #1a1a1a; margin-bottom: 32px'>
        <div style='font-family: Barlow Condensed, sans-serif; font-size:3.8rem; font-weight:800; color:#fff; text-transform:uppercase; letter-spacing:2px; line-height:1'>
            SENTINELAI<br><span style='color:#FFD700'>INTELLIGENCE PLATFORM</span>
        </div>
        <div style='color:#555; margin-top:12px; font-size:0.9rem; letter-spacing:1px; text-transform:uppercase; font-family:Barlow,sans-serif'>
            AI-powered Digital Public Safety &nbsp;·&nbsp; Citizens &nbsp;·&nbsp; Banks &nbsp;·&nbsp; Law Enforcement
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='metric-card'>
            <div class='value'>1.14M</div>
            <div class='label'>Cyber Complaints (2023)</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='metric-card'>
            <div class='value red'>Rs 1,776Cr</div>
            <div class='label'>Lost to Digital Arrest Scams</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='metric-card'>
            <div class='value yellow'>60%</div>
            <div class='label'>YoY Increase in Cybercrime</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class='metric-card'>
            <div class='value'>94.2%</div>
            <div class='label'>SentinelAI Detection Accuracy</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Platform Modules</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background:#000; border:1px solid #222; border-top:3px solid #FFD700; border-radius:0; padding:20px; margin-bottom:12px'>
            <div style='font-family:Barlow Condensed,sans-serif; font-weight:800; font-size:1.2rem; color:#fff; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px'>Citizen Fraud Shield</div>
            <div style='color:#555; font-size:0.85rem; line-height:1.6'>
                Paste suspicious messages or upload screenshots.
                AI instantly detects scam type, risk score, and recommended actions.
            </div>
            <div style='margin-top:14px'>
                <span class='tag'>Text Analysis</span>
                <span class='tag'>Image OCR</span>
                <span class='tag'>Gemini AI</span>
            </div>
        </div>
        <div style='background:#000; border:1px solid #222; border-top:3px solid #fff; border-radius:0; padding:20px; margin-bottom:12px'>
            <div style='font-family:Barlow Condensed,sans-serif; font-weight:800; font-size:1.2rem; color:#fff; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px'>Geospatial Crime Intelligence</div>
            <div style='color:#555; font-size:0.85rem; line-height:1.6'>
                Interactive India fraud heatmap showing cybercrime hotspots
                and city-level intelligence for patrol prioritisation.
            </div>
            <div style='margin-top:14px'>
                <span class='tag'>Folium Maps</span>
                <span class='tag'>Heatmap</span>
                <span class='tag'>City Analytics</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:#000; border:1px solid #222; border-top:3px solid #fff; border-radius:0; padding:20px; margin-bottom:12px'>
            <div style='font-family:Barlow Condensed,sans-serif; font-weight:800; font-size:1.2rem; color:#fff; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px'>Fraud Network Graph Intelligence</div>
            <div style='color:#555; font-size:0.85rem; line-height:1.6'>
                Graph AI maps coordinated fraud rings linking scammer phones,
                mule bank accounts, victims, and controllers.
            </div>
            <div style='margin-top:14px'>
                <span class='tag'>NetworkX</span>
                <span class='tag'>Graph AI</span>
                <span class='tag'>Ring Detection</span>
            </div>
        </div>
        <div style='background:#000; border:1px solid #222; border-top:3px solid #fff; border-radius:0; padding:20px; margin-bottom:12px'>
            <div style='font-family:Barlow Condensed,sans-serif; font-weight:800; font-size:1.2rem; color:#fff; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px'>Law Enforcement Copilot</div>
            <div style='color:#555; font-size:0.85rem; line-height:1.6'>
                AI assistant for investigators. Query fraud patterns,
                generate NCRP reports, and get real-time intelligence summaries.
            </div>
            <div style='margin-top:14px'>
                <span class='tag'>Gemini AI</span>
                <span class='tag'>Report Gen</span>
                <span class='tag'>Intelligence</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Future Roadmap</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#000; border:1px solid #222; border-left:4px solid #FFD700; border-radius:0; padding:20px'>
        <div style='color:#555; font-size:0.85rem; line-height:2.4; font-family:Barlow,sans-serif; letter-spacing:0.5px'>
            <span style='color:#fff; font-family:Barlow Condensed,sans-serif; font-weight:700; letter-spacing:1px; text-transform:uppercase'>Counterfeit Currency Detection</span> — CV model for Rs 500/2000 notes<br>
            <span style='color:#fff; font-family:Barlow Condensed,sans-serif; font-weight:700; letter-spacing:1px; text-transform:uppercase'>Voice Deepfake Detection</span> — Real-time AI voice spoofing alerts<br>
            <span style='color:#fff; font-family:Barlow Condensed,sans-serif; font-weight:700; letter-spacing:1px; text-transform:uppercase'>WhatsApp Integration</span> — Citizen reporting in 12 regional languages<br>
            <span style='color:#fff; font-family:Barlow Condensed,sans-serif; font-weight:700; letter-spacing:1px; text-transform:uppercase'>Telecom Integration</span> — Real-time scam call flagging
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE 2 - CITIZEN FRAUD SHIELD
# ══════════════════════════════════════════════════════════
elif page == "Citizen Fraud Shield":
    st.markdown("<div class='section-title'>Citizen Fraud Shield</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#555; margin-bottom:24px; letter-spacing:1px; text-transform:uppercase; font-size:0.78rem; font-family:Barlow,sans-serif'>Analyse suspicious messages, screenshots, or call transcripts instantly.</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Analyse Text / Message", "Analyse Screenshot"])

    with tab1:
        st.markdown("<div style='font-family:Barlow Condensed,sans-serif;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#aaa;font-size:0.85rem;margin-bottom:8px'>Paste the suspicious message, email, or call transcript below:</div>", unsafe_allow_html=True)

        examples = {
            "Select an example...": "",
            "Digital Arrest Scam": "This is Inspector Sharma from CBI Mumbai. Your Aadhaar number has been used in a money laundering case. You are under digital arrest. Do not leave your house or inform anyone. You must transfer Rs 2,50,000 to this account to clear your name: HDFC 9876543210. This is a court order.",
            "KYC Expiry Scam": "Dear Customer, Your SBI KYC has expired. Your account will be blocked in 24 hours. Click here to update: http://sbi-kyc-update.xyz and enter your account details and OTP to avoid suspension.",
            "Lottery Scam": "Congratulations! You have won Rs 45 Lakhs in the KBC Lucky Draw 2024. To claim your prize, pay Rs 5,000 processing fee via UPI to prizedesk@paytm. Contact us immediately or prize will expire.",
            "Safe Message": "Hey! Are you coming to the college fest this weekend? Rohan said it starts at 5 PM. Let me know!"
        }

        selected = st.selectbox("Or try an example:", list(examples.keys()))
        default_text = examples[selected]

        user_text = st.text_area(
            "Message content:",
            value=default_text,
            height=150,
            placeholder="Paste suspicious message here...",
            label_visibility="collapsed"
        )

        if st.button("Analyse for Fraud", key="analyze_text"):
            if user_text.strip():
                with st.spinner("Analysing with SentinelAI..."):
                    try:
                        result = analyze_text(user_text)
                        display_result(result)
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
            else:
                st.warning("Please enter a message to analyse.")

    with tab2:
        st.markdown("<div style='font-family:Barlow Condensed,sans-serif;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#aaa;font-size:0.85rem;margin-bottom:8px'>Upload a screenshot of the suspicious message:</div>", unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Upload screenshot",
            type=["png", "jpg", "jpeg", "webp"],
            label_visibility="collapsed"
        )

        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption="Uploaded Screenshot", use_container_width=True)

            if st.button("Analyse Screenshot", key="analyze_image"):
                with st.spinner("Analysing screenshot with SentinelAI..."):
                    try:
                        img_bytes = uploaded.getvalue()
                        mime = uploaded.type
                        result = analyze_image(img_bytes, mime)
                        display_result(result)
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")


# ══════════════════════════════════════════════════════════
# PAGE 3 - FRAUD NETWORK GRAPH
# ══════════════════════════════════════════════════════════
elif page == "Fraud Network Graph":
    st.markdown("<div class='section-title'>Fraud Network Intelligence Graph</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#555; margin-bottom:24px; letter-spacing:1px; text-transform:uppercase; font-size:0.78rem; font-family:Barlow,sans-serif'>
        SentinelAI maps coordinated fraud rings by linking scammer phones, mule accounts,
        victims, and controllers into actionable intelligence packages.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='metric-card'>
            <div class='value red'>1</div>
            <div class='label'>Fraud Ring Detected</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='metric-card'>
            <div class='value yellow'>3</div>
            <div class='label'>Scammer Numbers</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='metric-card'>
            <div class='value'>7</div>
            <div class='label'>Victims Identified</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class='metric-card'>
            <div class='value'>3</div>
            <div class='label'>Mule Accounts</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.spinner("Generating fraud network graph..."):
        fig = draw_fraud_graph()
        st.pyplot(fig)

    st.markdown("""
    <div style='background:#000; border:1px solid #222; border-left:4px solid #FFD700; border-radius:0; padding:16px; margin-top:16px'>
        <div style='font-family:Barlow Condensed,sans-serif;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FFD700;font-size:0.85rem;margin-bottom:6px'>SentinelAI Intelligence Summary</div>
        <div style='color:#aaa; font-size:0.88rem; line-height:1.6'>
        Identified a coordinated fraud ring with 1 controller node directing 3 scammer phones targeting 7 victims across Delhi and Mumbai.
        Total estimated fraud: Rs 18.4 Lakhs. Money laundered through 3 mule accounts.
        Intelligence package ready for NCRP submission.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE 4 - CRIME HEATMAP
# ══════════════════════════════════════════════════════════
elif page == "Crime Heatmap":
    st.markdown("<div class='section-title'>Geospatial Crime Intelligence</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#555; margin-bottom:24px; letter-spacing:1px; text-transform:uppercase; font-size:0.78rem; font-family:Barlow,sans-serif'>
        Real-time fraud hotspot mapping across India. Click on city markers for detailed intelligence.
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading crime intelligence map..."):
        fraud_map = generate_heatmap()
        st_folium(fraud_map, width=None, height=560)

    st.markdown("""
    <div style='background:#000; border:1px solid #222; border-left:4px solid #FFD700; border-radius:0; padding:16px; margin-top:16px'>
        <div style='font-family:Barlow Condensed,sans-serif;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FFD700;font-size:0.85rem;margin-bottom:6px'>Intelligence Summary</div>
        <div style='color:#aaa; font-size:0.88rem; line-height:1.6'>
        Delhi NCR leads with 12,450 reported cases dominated by Digital Arrest and KYC scams.
        Mumbai reports 9,870 cases with heavy Investment Fraud activity.
        Bangalore shows emerging Tech Support Scam clusters near IT corridors.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE 5 - LAW ENFORCEMENT COPILOT
# ══════════════════════════════════════════════════════════
elif page == "Law Enforcement Copilot":
    st.markdown("<div class='section-title'>Law Enforcement Copilot</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#555; margin-bottom:24px; letter-spacing:1px; text-transform:uppercase; font-size:0.78rem; font-family:Barlow,sans-serif'>
        AI intelligence assistant for investigators. Query fraud patterns, generate reports, analyse clusters.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-family:Barlow Condensed,sans-serif;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#FFD700;font-size:0.85rem;margin-bottom:12px'>Quick Queries</div>", unsafe_allow_html=True)
    quick_prompts = [
        "Show scam clusters in Delhi NCR",
        "What scam type increased most in 2024?",
        "Generate an NCRP report template for digital arrest scam",
        "How do digital arrest scams operate step by step?",
        "What are red flags for identifying mule bank accounts?",
    ]

    cols = st.columns(3)
    for i, prompt in enumerate(quick_prompts):
        with cols[i % 3]:
            if st.button(prompt, key=f"quick_{i}"):
                st.session_state.pending_prompt = prompt

    st.markdown("<hr style='border-color:#1a1a1a;margin:20px 0'>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'><span style='color:#FFD700;font-family:Barlow Condensed,sans-serif;font-size:0.7rem;letter-spacing:2px;text-transform:uppercase'>You</span><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'><span style='color:#FFD700;font-family:Barlow Condensed,sans-serif;font-size:0.7rem;letter-spacing:2px;text-transform:uppercase'>SentinelAI</span><br>{msg['content']}</div>", unsafe_allow_html=True)

    if "pending_prompt" in st.session_state:
        prompt = st.session_state.pop("pending_prompt")
        with st.spinner("SentinelAI analysing..."):
            try:
                response = get_copilot_response(prompt, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    user_input = st.chat_input("Ask about fraud patterns, request reports, query intelligence...")
    if user_input:
        with st.spinner("SentinelAI analysing..."):
            try:
                response = get_copilot_response(user_input, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.get("chat_history"):
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
            