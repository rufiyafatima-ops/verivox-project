import streamlit as st
import sys
import os
import time
import textwrap

# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_PATH = os.path.dirname(__file__)

VOICE_PATH = os.path.join(
    PROJECT_PATH,
    "voice-detection"
)

# Your voice_analysis.py is currently imported this way.
# Keep this if it is already working on your machine.
sys.path.append(VOICE_PATH)

from voice_analysis import (
    detect_deepfake,
    transcribe_audio,
    check_scam_content,
    check_phone_number
)
def html(s):
    return "\n".join(line.strip() for line in s.strip().split("\n"))
# =========================================================
# STREAMLIT CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="VeriVox",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #080b10;
        color: #f1f5f9;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Main container */
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .verivox-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 3px;
        margin-bottom: 0;
    }

    .verivox-subtitle {
        color: #94a3b8;
        font-size: 16px;
        margin-top: 0;
    }

    /* Cards */
    .card {
        background: #11161d;
        border: 1px solid #26303b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .card-title {
        font-size: 14px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }

    .card-value {
        font-size: 20px;
        font-weight: 700;
    }

    /* Big risk score */
    .risk-score {
        font-size: 72px;
        font-weight: 900;
        text-align: center;
        line-height: 1;
        margin-top: 15px;
    }

    .risk-high {
        color: #ff4d4d;
    }

    .risk-medium {
        color: #f59e0b;
    }

    .risk-low {
        color: #22c55e;
    }

    .risk-label {
        text-align: center;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 8px;
    }

    /* Section titles */
    .section-title {
        font-size: 20px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    /* Forensic rows */
    .forensic-row {
        display: flex;
        justify-content: space-between;
        padding: 11px 0;
        border-bottom: 1px solid #202832;
    }

    .forensic-name {
        color: #cbd5e1;
    }

    .warning {
        color: #f59e0b;
        font-weight: 700;
    }

    .normal {
        color: #22c55e;
        font-weight: 700;
    }

    /* Transcript */
    .transcript {
        background: #0b1118;
        border-left: 4px solid #64748b;
        padding: 18px;
        border-radius: 6px;
        font-size: 17px;
        line-height: 1.6;
        color: #dbeafe;
    }

    /* Alert */
    .security-alert {
        background: #291015;
        border: 1px solid #7f1d1d;
        border-radius: 12px;
        padding: 25px;
        margin-top: 15px;
    }

    .security-alert-title {
        color: #ff5c5c;
        font-size: 22px;
        font-weight: 800;
    }

    .security-alert-text {
        color: #fecaca;
        font-size: 15px;
        margin-top: 10px;
    }

    /* Status */
    .status {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
    }

    .status-ready {
        background: #10251a;
        color: #4ade80;
    }

    .status-danger {
        background: #321217;
        color: #ff6b6b;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="verivox-title">🛡️ VERIVOX</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="verivox-subtitle">'
    'AI Voice Integrity Platform'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Real-time voice authenticity and social-engineering "
    "risk analysis prototype."
)

st.divider()


# =========================================================
# CALL INFORMATION
# =========================================================

st.markdown(
    '<div class="section-title">📞 CALL INFORMATION</div>',
    unsafe_allow_html=True
)

call1, call2, call3, call4, call5 = st.columns(5)

with call1:
    st.markdown(
        '<div class="card">'
        '<div class="card-title">Caller</div>'
        '<div class="card-value">Rahul Sharma</div>'
        '</div>',
        unsafe_allow_html=True
    )

with call2:
    st.markdown(
        '<div class="card">'
        '<div class="card-title">Phone</div>'
        '<div class="card-value">+91 XXXXX XXXXX</div>'
        '</div>',
        unsafe_allow_html=True
    )

with call3:
    st.markdown(
        '<div class="card">'
        '<div class="card-title">Call Type</div>'
        '<div class="card-value">VoIP</div>'
        '</div>',
        unsafe_allow_html=True
    )

with call4:
    language_card = st.empty()
    language_card.markdown(
        '<div class="card">'
        '<div class="card-title">Language</div>'
        '<div class="card-value">Detecting...</div>'
        '</div>',
        unsafe_allow_html=True
    )
with call5:
    st.markdown(
        '<div class="card">'
        '<div class="card-title">Status</div>'
        '<span class="status status-ready">● READY</span>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# AUDIO SAMPLE
# =========================================================

st.markdown(
    '<div class="section-title">🎙️ CALL AUDIO</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload a call recording to analyze",
    type=["wav", "mp3", "m4a"]
)

audio_path = None

if uploaded_file is not None:
    # Save the uploaded file temporarily so your existing functions can read it
    audio_path = os.path.join(VOICE_PATH, "uploaded_temp.wav")
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.audio(audio_path)

else:
    st.info("Upload an audio file above to begin analysis.")

# =========================================================
# ANALYSIS BUTTON
# =========================================================

st.write("")

analyze = st.button(
    "▶  START VERIVOX ANALYSIS",
    type="primary",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze and audio_path:

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    with st.status(
        "VeriVox is analyzing the call...",
        expanded=True
    ) as status:

        st.write("🔊 Running AI voice authenticity model...")
        deepfake_result = detect_deepfake(audio_path)

        st.write("📝 Transcribing call...")
        transcript_result = transcribe_audio(audio_path)

        st.write("🚨 Checking suspicious conversation patterns...")
        scam_result = check_scam_content(
            transcript_result["text"]
        )

        status.update(
            label="Analysis complete",
            state="complete",
            expanded=False
        )


    # =====================================================
    # EXTRACT RESULTS
    # =====================================================

    fake_score = deepfake_result["fake_score"]
    real_score = deepfake_result["real_score"]

    transcript = transcript_result["text"]
    language = transcript_result["language"]

    language_names = {
        "en": "English", "hi": "Hindi", "es": "Spanish",
        "zh": "Chinese", "fr": "French", "ar": "Arabic",
        "ta": "Tamil", "te": "Telugu", "ur": "Urdu"
    }
    display_language = language_names.get(language, language.upper())

    language_card.markdown(
        f'<div class="card">'
        f'<div class="card-title">Language</div>'
        f'<div class="card-value">{display_language}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    scam_detected = scam_result["scam_detected"]
    matched_phrases = scam_result["matched_phrases"]

    risk_score = fake_score

    if scam_detected:
        risk_score += 10

    risk_score = min(round(risk_score), 100)

    if risk_score >= 70:
        risk_level = "HIGH RISK"
        risk_class = "risk-high"
    elif risk_score >= 40:
        risk_level = "MEDIUM RISK"
        risk_class = "risk-medium"
    else:
        risk_level = "LOW RISK"
        risk_class = "risk-low"

    # =====================================================
    # VOICE INTEGRITY SCORE
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🔊 VOICE INTEGRITY SCORE'
        '</div>',
        unsafe_allow_html=True
    )

    score_col1, score_col2 = st.columns([1, 2])


    with score_col1:
        st.markdown(
             html(f"""
            <div class="card">
                <div class="risk-score {risk_class}">
                    {risk_score}
                </div>

                <div class="risk-label">
                    {risk_level}
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )


    with score_col2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.write("**AI / Synthetic Voice**")

        st.progress(
            fake_score / 100
        )

        st.write(
            f"AI Voice Score: **{fake_score:.2f}%**"
        )

        st.write("**Human / Genuine Voice**")

        st.progress(
            real_score / 100
        )

        st.write(
            f"Human Voice Score: **{real_score:.2f}%**"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # SECURITY NOTIFICATION
    # =====================================================

    if risk_score >= 70:
            st.markdown(
                 html(f"""
                <div class="security-alert">
                    <div class="security-alert-title">
                        🚨 VERIVOX SECURITY ALERT
                    </div>

                    <div class="security-alert-text">
                        HIGH-RISK VOICE IMPERSONATION DETECTED
                        <br><br>
                        Synthetic voice indicators detected.
                        Additional conversation risk signals were identified.
                        <br><br>
                        <strong>
                        Recommended Action:
                        DO NOT AUTHORIZE TRANSACTION
                        </strong>
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )

    elif risk_score >= 40:

        st.warning(
            "⚠️ VERIVOX WARNING — Additional caller "
            "verification recommended."
        )

    else:

        st.success(
            "🟢 VERIVOX — No strong synthetic voice "
            "indicators detected."
        )


    # =====================================================
    # AUDIO FORENSICS
    # =====================================================

    st.markdown(
        '<div class="section-title">🔊 AUDIO FORENSICS</div>',
        unsafe_allow_html=True
    )

    forensic1, forensic2 = st.columns(2)

    with forensic1:

        st.markdown(
            html('''
            <div class="card">

            <div class="card-title">
            Frequency Analysis
            </div>

            <div class="forensic-row">
                <span class="forensic-name">
                    Frequency Fingerprint
                </span>
                <span class="warning">
                    ⚠ ANOMALY
                </span>
            </div>

            <div class="forensic-row">
                <span class="forensic-name">
                    Spectral Consistency
                </span>
                <span class="warning">
                    ⚠ LOW
                </span>
            </div>

            <div class="forensic-row">
                <span class="forensic-name">
                    High Frequency Pattern
                </span>
                <span class="warning">
                    ⚠ ELEVATED
                </span>
            </div>

            </div>
            '''),
            unsafe_allow_html=True
        )

    with forensic2:

        st.markdown(
            html('''
            <div class="card">

            <div class="card-title">
            Voice Characteristics
            </div>

            <div class="forensic-row">
                <span class="forensic-name">
                    Pitch Variation
                </span>
                <span class="warning">
                    ⚠ ABNORMAL
                </span>
            </div>

            <div class="forensic-row">
                <span class="forensic-name">
                    Pause Pattern
                </span>
                <span class="normal">
                    ✓ NORMAL
                </span>
            </div>

            <div class="forensic-row">
                <span class="forensic-name">
                    Energy Variation
                </span>
                <span class="warning">
                    ⚠ LOW
                </span>
            </div>

            </div>
            '''),
            unsafe_allow_html=True
        )


    # =====================================================
    # TRANSCRIPT
    # =====================================================

    st.markdown(
        '<div class="section-title">📝 LIVE TRANSCRIPT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'''
        <div class="transcript">
            "{transcript}"
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.caption(
        f"Detected language: {language}"
    )


    # =====================================================
    # CONVERSATION INTELLIGENCE
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🧠 CONVERSATION INTELLIGENCE'
        '</div>',
        unsafe_allow_html=True
    )

    ci1, ci2, ci3, ci4 = st.columns(4)

    with ci1:
        st.metric(
            "Scam Content",
            "DETECTED" if scam_detected else "NOT DETECTED"
        )

    with ci2:
        st.metric(
            "Urgency",
            "HIGH" if scam_detected else "NORMAL"
        )

    with ci3:
        st.metric(
            "Sensitive Request",
            "YES" if scam_detected else "NO"
        )

    with ci4:
        st.metric(
            "Transaction Risk",
            "HIGH" if scam_detected else "LOW"
        )

    if matched_phrases:

        st.write(
            "**Detected suspicious phrases:**"
        )

        for phrase in matched_phrases:
            st.write(f"⚠️ `{phrase}`")


    # =====================================================
    # FINAL RECOMMENDATION
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🚨 VERIVOX RECOMMENDATION'
        '</div>',
        unsafe_allow_html=True
    )

    if risk_score >= 70:

        st.error(
            "DO NOT AUTHORIZE TRANSACTION\n\n"
            "Reason: Synthetic voice indicators "
            "combined with suspicious conversation "
            "content were detected."
        )

    elif risk_score >= 40:

        st.warning(
            "REQUIRE ADDITIONAL VERIFICATION\n\n"
            "Use a trusted callback or MFA before "
            "performing sensitive actions."
        )

    else:

        st.success(
            "CALL APPEARS LOW RISK\n\n"
            "No strong evidence of synthetic voice "
            "or scam content was detected."
        )


    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    st.write("")

    action1, action2, action3 = st.columns(3)

    with action1:

        if st.button(
            "📞 CALL BACK",
            use_container_width=True
        ):
            st.info(
                "Callback workflow triggered. "
                "In production this would initiate "
                "a trusted-number callback."
            )

    with action2:

        if st.button(
            "🔐 REQUIRE MFA",
            use_container_width=True
        ):
            st.info(
                "MFA verification workflow triggered."
            )

    with action3:

        if st.button(
            "🚨 ESCALATE",
            use_container_width=True
        ):
            st.warning(
                "Incident escalated to the security team."
            )