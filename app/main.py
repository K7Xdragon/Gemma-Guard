import sys
from pathlib import Path

# Add the project root to the path for imports
sys.path.append(str(Path(__file__).parent.parent))

from app.pattern_mapper import map_traits_to_behavioral_pattern, display_pattern_profile
from app.matcher import match_signal_to_profile
from app.gemma_inference import run_inference
from app.insight_generator import generate_insight

import os
import streamlit as st
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.signal_engine import get_current_signal, format_for_ollama_prompt
from app.utils_data import append_signal_log
from app.utils_format import summarize_signal_packet

# Import Ollama health check
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from private.llm_inference import check_ollama_health

SIGNAL_LOG_PATH = "data/signal_log.json"
os.makedirs("data", exist_ok=True)

# Configure Streamlit for healing tech vibe
st.set_page_config(
    page_title="GemmaGuard - Burnout Insight System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for healing tech aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2c3e50;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    .tagline {
        text-align: center;
        font-size: 1.3rem;
        color: #5a6c7d;
        font-weight: 400;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Card styling */
    .insight-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 15px;
        border: 2px solid #e1e8ed;
        background: rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        padding: 0.5rem;
        margin: 0.2rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        font-weight: 600;
    }
    
    /* Metric styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session page
if "page" not in st.session_state:
    st.session_state.page = 1

def go_to_page_2():
    st.session_state.page = 2

def go_to_page_3():
    st.session_state.page = 3

# Check Ollama status
@st.cache_data(ttl=60)  # Cache for 1 minute
def get_ollama_status():
    return check_ollama_health()

# Page 1 — Greeting & Introduction
if st.session_state.page == 1:
    # Hero Section
    st.markdown('<h1 class="main-header">GemmaGuard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Hello, welcome!</p>', unsafe_allow_html=True)
    
    # Main content in cards
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Status Display
        ollama_status = get_ollama_status()
        enable_ollama = os.getenv("ENABLE_OLLAMA_INTEGRATION", "false").lower() == "true"
        
        if enable_ollama:
            if ollama_status["status"] == "healthy" and ollama_status["gemma_available"]:
                st.success("🤖 Gemma 3n is ready via Ollama")
            elif ollama_status["status"] == "healthy":
                st.warning(f"⚠️ Ollama is running but Gemma model not found. Available: {', '.join(ollama_status['available_models'])}")
            else:
                st.error("🔧 Ollama connection failed - using simulation mode")
        else:
            st.info("🧪 Running in simulation mode (Ollama integration disabled)")
        
        # What is GemmaGuard
        st.markdown("""
        <div class="insight-card">
            <h2 style="text-align: center; color: #4a5568; margin-bottom: 1.5rem;">🧠 What is GemmaGuard</h2>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #5a6c7d; text-align: center;">
                GemmaGuard uses biometrics-inspired analytics to help you monitor stress levels, 
                burnout risk, and emotional fatigue. This app uses scientifically simulated signal data 
                paired with behavioral prompts to help you reflect, reset, and recharge.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Next button
        st.markdown('<div style="margin: 2rem 0; text-align: center;">', unsafe_allow_html=True)
        next_button_1 = st.button("➡️ Continue", key="next_button_1", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if next_button_1:
            go_to_page_2()
            st.rerun()

# Page 2 — What Makes GemmaGuard Work
elif st.session_state.page == 2:
    # Header
    st.markdown('<h1 class="main-header">How GemmaGuard Works</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Advanced AI technology combined with behavioral pattern analysis</p>', unsafe_allow_html=True)
    
    # Main content in cards
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # How GemmaGuard Works
        st.markdown("""
        <div class="insight-card">
            <h2 style="text-align: center; color: #4a5568; margin-bottom: 1.5rem;">🧠 The Science Behind GemmaGuard</h2>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #5a6c7d; text-align: center;">
                GemmaGuard combines temporal pattern analysis with modern AI to create your personal burnout prevention system. 
                We analyze behavioral timestamps, simulate biometric responses, and use advanced Gemma AI to understand your unique stress signatures—delivering insights that feel personally crafted for you.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Benefits Section
        st.markdown("""
        <div class="insight-card">
            <h2 style="text-align: center; color: #4a5568; margin-bottom: 1.5rem;">✨ What Makes GemmaGuard Unique</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Benefits in columns
        benefit_col1, benefit_col2 = st.columns(2)
        
        with benefit_col1:
            st.markdown("""
            <div class="insight-card">
                <h3 style="color: #667eea;">🎯 Personal Pattern Analysis</h3>
                <p style="color: #5a6c7d; line-height: 1.6;">
                    Unlike generic wellness apps, we analyze your unique behavioral patterns and temporal signatures to understand your natural rhythms and stress vulnerabilities.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-card">
                <h3 style="color: #667eea;">🤖 AI-Powered Insights</h3>
                <p style="color: #5a6c7d; line-height: 1.6;">
                    Gemma AI processes your unique patterns to deliver personalized recommendations that evolve with your changing stress levels.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with benefit_col2:
            st.markdown("""
            <div class="insight-card">
                <h3 style="color: #667eea;">📊 Real-Time Biometric Simulation</h3>
                <p style="color: #5a6c7d; line-height: 1.6;">
                    Experience scientifically-modeled stress responses that help you understand your body's signals before burnout strikes.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-card">
                <h3 style="color: #667eea;">🔮 Predictive Timing</h3>
                <p style="color: #5a6c7d; line-height: 1.6;">
                    Know your high-risk periods in advance and plan recovery times—something no other wellness app can offer.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Privacy info
        st.markdown("""
        <div class="insight-card">
            <h3 style="text-align: center; color: #4a5568;">🔒 Your Privacy, Protected</h3>
            <p style="color: #5a6c7d; line-height: 1.6; text-align: center;">
                All analysis happens locally. Your personal data never leaves your device, ensuring complete privacy while delivering powerful insights.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Next button
        st.markdown('<div style="margin: 2rem 0; text-align: center;">', unsafe_allow_html=True)
        next_button_2 = st.button("➡️ Next", key="next_button_2", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if next_button_2:
            go_to_page_3()
            st.rerun()

# Page 3 — System Status & Terms
elif st.session_state.page == 3:
    # Header
    st.markdown('<h1 class="main-header">Ready to Begin</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">System status and terms before we start your analysis</p>', unsafe_allow_html=True)
    
    # Main content in cards
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # System Status
        st.markdown("""
        <div class="insight-card">
            <h2 style="text-align: center; color: #4a5568; margin-bottom: 1.5rem;">🤖 System Status</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Display Ollama status with styled cards
        ollama_status = get_ollama_status()
        enable_ollama = os.getenv("ENABLE_OLLAMA_INTEGRATION", "false").lower() == "true"
        
        if enable_ollama:
            if ollama_status["status"] == "healthy" and ollama_status["gemma_available"]:
                st.markdown("""
                <div class="insight-card">
                    <p style="text-align: center; color: #38a169; font-weight: 600;">
                        ✅ Gemma AI is ready and optimized for your analysis
                    </p>
                </div>
                """, unsafe_allow_html=True)
            elif ollama_status["status"] == "healthy":
                st.markdown(f"""
                <div class="insight-card">
                    <p style="text-align: center; color: #d69e2e; font-weight: 600;">
                        ⚠️ Ollama is running but Gemma model not found. Available: {', '.join(ollama_status['available_models'])}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="insight-card">
                    <p style="text-align: center; color: #e53e3e; font-weight: 600;">
                        🔧 Ollama connection failed - using simulation mode
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-card">
                <p style="text-align: center; color: #4a5568; font-weight: 600;">
                    🧪 Running in simulation mode for demonstration
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Terms and Conditions
        st.markdown("""
        <div class="insight-card">
            <h2 style="text-align: center; color: #4a5568; margin-bottom: 1.5rem;">� Terms & Conditions</h2>
            <p style="color: #5a6c7d; line-height: 1.6; text-align: center;">
                This app values your privacy. All data remains local or anonymized, and is only used for internal analysis. 
                By proceeding, you acknowledge that this is a wellness tool for informational purposes and should not replace professional medical advice.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Consent checkbox with styling
        st.markdown('<div style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
        agree = st.checkbox("I agree to the Terms & Conditions and Privacy Policy", key="consent_checkbox")
        
        # CTA Button
        st.markdown('<div style="margin: 1.5rem 0; text-align: center;">', unsafe_allow_html=True)
        start_button = st.button("🚀 Start My Insight", disabled=not agree, key="start_button")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if start_button:
            st.session_state.page = 4
            st.rerun()

# Page 4 — User Input & Analysis
elif st.session_state.page == 4:
    # Header
    st.markdown('<h1 class="main-header">Your Personal Insight Journey</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Tell us about yourself to unlock your unique burnout prevention insights</p>', unsafe_allow_html=True)
    
    # Form in centered column
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Personal Information Card
        st.markdown("""
        <div class="insight-card">
            <h2 style="text-align: center; color: #4a5568; margin-bottom: 1.5rem;">✨ Personal Information</h2>
        </div>
        """, unsafe_allow_html=True)
        
        nickname = st.text_input("Your Nickname", placeholder="What should we call you?")
        dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        location = st.text_input("Location", placeholder="City, Country")
        status = st.radio(
            "Current Status", 
            ["Student", "Working", "Not Employed", "Retired", "Self-Employed", "Part-time", "Career Break", "Other"],
            horizontal=True
        )
        
        # Symptoms Card
        st.markdown("""
        <div class="insight-card">
            <h2 style="text-align: center; color: #4a5568; margin-bottom: 1.5rem;">🔍 Current Symptoms</h2>
            <p style="text-align: center; color: #5a6c7d; margin-bottom: 1rem;">Select any symptoms you're currently experiencing:</p>
        </div>
        """, unsafe_allow_html=True)
        
        symptoms = [
            "Feeling tired or drained",
            "Frequent headaches or muscle pain", 
            "Difficulty concentrating",
            "Loss of motivation",
            "Changes in sleep habits",
            "Negative or cynical outlook",
            "Feeling trapped or helpless"
        ]
        
        selected_symptoms = []
        symptom_cols = st.columns(2)
        for i, symptom in enumerate(symptoms):
            with symptom_cols[i % 2]:
                if st.checkbox(symptom, key=f"symptom_{i}"):
                    selected_symptoms.append(symptom)
        
        # Analysis Mode Card
        st.markdown("""
        <div class="insight-card">
            <h2 style="text-align: center; color: #4a5568; margin-bottom: 1.5rem;">🎯 Choose Your Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
        
        analysis_mode = st.radio(
            "",
            ["Full Analysis (with biometric simulation)", "Temporal Pattern Analysis (signature-based)"],
            help="Full analysis includes simulated biometric data. Temporal Pattern analysis uses your timestamp signatures for pure behavioral pattern analysis."
        )
        
        # Analyze button
        st.markdown('<div style="margin: 2rem 0; text-align: center;">', unsafe_allow_html=True)
        analyze_button = st.button("🔬 Begin Analysis", key="analyze_button", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if analyze_button:
            # Store analysis parameters in session state
            st.session_state.run_analysis = True
            st.session_state.analysis_mode = analysis_mode
            st.session_state.nickname = nickname
            st.session_state.dob = dob
            st.session_state.selected_symptoms = selected_symptoms

    # Run analysis if triggered
    if st.session_state.get("run_analysis", False):
        if st.session_state.analysis_mode == "Temporal Pattern Analysis (signature-based)":
            # Pure temporal pattern analysis without biometrics
            st.subheader("🔬 Temporal Pattern Analysis")
            
            # Progress indicator for Pattern analysis
            with st.spinner("🧠 Analyzing your behavioral pattern signatures..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Import and setup
                status_text.text("📊 Loading pattern analysis engine...")
                progress_bar.progress(20)
                from private.chrono_decoder import get_chrono_profile_without_biometrics
                
                # Step 2: Format date
                status_text.text("📅 Processing timestamp information...")
                progress_bar.progress(40)
                dob_formatted = st.session_state.dob.strftime("%d/%m/%Y")
                
                # Step 3: Run analysis
                status_text.text("🔍 Computing behavioral signature patterns...")
                progress_bar.progress(70)
                chrono_result = get_chrono_profile_without_biometrics(dob_formatted)
                
                # Step 4: Generate insights
                status_text.text("💡 Generating personalized insights...")
                progress_bar.progress(90)
                
                # Complete
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
            
            if "error" in chrono_result:
                st.error(f"Analysis failed: {chrono_result['error']}")
                if "fallback_advice" in chrono_result:
                    st.info(chrono_result["fallback_advice"])
            else:
                st.markdown(f"Hi **{st.session_state.nickname}**, based on your Temporal Pattern analysis:")
                
                # Display pattern profile with detailed trait analysis
                st.markdown("🔍 **Your Behavioral Signature Profile**")
                
                # Get the signature name for internal reference
                signature_name = chrono_result['chrono_signature']
                
                # Create detailed trait explanation based on signature
                trait_explanations = {
                    "Ji-Chou": """You are naturally stable, loyal, and practical, with a humble nature that often leads you to support others from behind the scenes. There's something deeply reliable about you that people instinctively trust. However, you sometimes tend to bottle up your emotions, overthink situations, and silently strive for perfection, which can create internal turbulence even when you appear calm on the surface.

Your tendency toward emotional suppression means you rarely show anger openly, instead holding it in until it builds up. This can be both a strength and a challenge - while others see you as steady and composed, you may be wrestling with unexpressed feelings internally.

The downside of this personality pattern is that you may feel particularly drained when you lack clear direction or purpose in life. You might find yourself falling into cycles of overthinking, especially when the environment around you feels uncertain or unstable. There's also a potential for you to become overly passive during stressful periods, waiting for things to settle rather than taking decisive action.""",
                    
                    "Jia-Zi": """You possess an innovative and pioneering spirit that naturally positions you as a leader. There's an independence about you that drives strong initiative, and you tend to approach life with confidence and ambition, always seeking new opportunities and challenges to conquer.

Your natural inclination is toward impatience when it comes to seeing results. You often want immediate outcomes and may find yourself rushing into decisions without fully considering all the implications. This drive for quick action can be both your greatest asset and your biggest challenge.

When stress builds up, you might notice yourself becoming overly aggressive or domineering with others. You may struggle with delegation, preferring to handle things yourself rather than trust others to meet your standards. Criticism or feedback from others can be particularly difficult for you to accept, as it conflicts with your natural confidence and self-reliance.""",
                    
                    "Yi-Chou": """You have a naturally nurturing and flexible disposition, combined with strong emotional intelligence that allows you to understand others' needs intuitively. There's a diplomatic quality about you that helps you adapt to different situations with grace and patience, making you someone others feel comfortable turning to for support.

Your instinct is often to prioritize harmony and avoid conflict, sometimes at the expense of your own needs. You may find yourself saying yes when you'd rather say no, or adjusting your preferences to accommodate others' comfort.

This people-pleasing tendency can lead to difficulty making decisions when important choices arise, especially when those decisions might disappoint someone. You might struggle with setting clear boundaries, and there's a risk of internalizing others' emotions to the point where external stress becomes overwhelming for you personally.""",
                    
                    "Bing-Yin": """You carry a passionate and creative energy that naturally draws others to you through your charisma and enthusiasm. There's an intuitive quality about you that allows you to inspire and motivate people, often becoming the spark that ignites action in group settings.

Your emotional intensity can be both magnetic and challenging - you experience feelings deeply and may have dramatic reactions that others sometimes perceive as temperamental or unpredictable. This intensity fuels your creativity but can also make your emotional landscape feel turbulent.

The challenge with this vibrant energy is that you may burn out quickly from overcommitting yourself to too many projects or causes. Consistency in long-term endeavors can be difficult when your passion shifts or wanes. When you're not receiving the attention or recognition you desire, there's a risk of becoming manipulative in your attempts to regain that spotlight."""
                }
                
                # Get the detailed explanation or provide a generic one
                if signature_name in trait_explanations:
                    explanation = trait_explanations[signature_name]
                    profile_summary = f"{explanation}\n\n**Your Pattern Tags:**\n{', '.join(chrono_result['pattern_tags'])}"
                else:
                    # Fallback for unknown signatures - provide detailed human-centered explanations
                    profile_summary = f"""
**Your Chronotype Profile:** Based on your birth date analysis

**Pattern Tags:** {', '.join(chrono_result['pattern_tags'])}
"""
                    
                    # Transform technical details into human-centered explanations
                    detailed_explanations = []
                    chronotype_preferences = ""
                    
                    for rationale in chrono_result['rationale']:
                        if rationale.startswith("Chronotype Analysis Preferences:"):
                            chronotype_preferences = rationale.split(": ")[1]
                        elif rationale.startswith("Primary element influence:"):
                            element = rationale.split(": ")[1]
                            if "Fire" in element:
                                detailed_explanations.append("Your inner energy burns bright and passionate. You're someone who feels things intensely and approaches life with enthusiasm, but this same passion that drives your creativity can sometimes lead to burnout if you don't pace yourself. You thrive on excitement and new challenges, yet you need to remember to nurture your energy rather than let it consume you.")
                            elif "Earth" in element:
                                detailed_explanations.append("There's a grounding, stabilizing quality about you that others find deeply comforting. You have this natural ability to remain steady during storms, to be the rock that others lean on. However, this same stability can sometimes make you feel stuck or resistant to change. You process things slowly and thoroughly, which is a strength, but remember that growth sometimes requires stepping out of your comfort zone.")
                            elif "Water" in element:
                                detailed_explanations.append("You flow with an intuitive understanding of emotions - both your own and others'. There's a depth to you that runs much deeper than what people see on the surface. You adapt naturally to different situations, taking the shape that's needed in each moment. This emotional intelligence is your gift, but be careful not to absorb everyone else's feelings to the point where you lose touch with your own needs.")
                            elif "Metal" in element:
                                detailed_explanations.append("You have a sharp, analytical mind that cuts through confusion to find clarity. There's a precision about the way you think and approach problems that others admire. You value structure, quality, and doing things the right way. However, this same clarity can sometimes make you overly critical - of yourself and others. Remember that perfection isn't always necessary, and sometimes 'good enough' really is enough.")
                            elif "Wood" in element:
                                detailed_explanations.append("You're naturally growth-oriented, always reaching toward something better, constantly stretching toward new possibilities. There's an optimistic, forward-thinking quality about you that inspires others. You see potential everywhere and have this wonderful ability to help things flourish. Just remember that even the strongest growth needs seasons of rest - constant expansion without pause can lead to exhaustion.")
                        
                        elif rationale.startswith("Current burnout risk level:"):
                            risk_level = rationale.split(": ")[1]
                            if "High" in risk_level:
                                detailed_explanations.append("Right now, your system is sending clear signals that you're running on empty. This isn't a judgment - it's your body and mind's way of asking for care. High burnout risk means you've been giving so much of yourself that your reserves are depleted. Think of it like a phone battery that's been running intensive apps all day - you need to plug in and recharge, not just for a few minutes, but for real restoration.")
                            elif "Medium" in risk_level:
                                detailed_explanations.append("You're in that yellow zone where things are manageable, but you can feel the strain building. It's like when you're carrying groceries and they're not too heavy yet, but you can sense that your arms are getting tired. This is actually the perfect time to make adjustments - before you reach that overwhelming point. Your awareness of this moderate stress level shows you're tuned into your own needs.")
                            elif "Low" in risk_level:
                                detailed_explanations.append("You're in a good space right now - your energy levels are sustainable and you're managing life's demands without feeling overwhelmed. This is what balance feels like, though it's not static. Think of it as sailing with favorable winds - enjoy this period while staying aware that conditions can change, and use this time to build healthy habits that will support you when things get more challenging.")
                        
                        elif rationale.startswith("Cognitive processing style:"):
                            style = rationale.split(": ")[1]
                            if "Analytical" in style:
                                detailed_explanations.append("Understanding your analytical nature helps explain why you need time to process information thoroughly before making decisions. You're not slow - you're thorough. This is why rushed decisions often feel uncomfortable for you, and why you perform best when given space to think things through. In a world that often demands quick responses, knowing this about yourself means you can advocate for the time you need to do your best work.")
                            elif "Intuitive" in style:
                                detailed_explanations.append("Your intuitive processing style means you often 'know' things before you can explain why. This isn't mystical - it's your brain rapidly processing patterns and information below conscious awareness. Understanding this helps you trust those gut feelings and also explains why you might struggle in environments that demand only logical, step-by-step reasoning. Your intuition is a powerful tool when you learn to balance it with practical considerations.")
                            elif "Creative" in style:
                                detailed_explanations.append("Your creative processing style means your brain makes connections that others might miss, finding novel solutions and seeing possibilities where others see problems. This is why routine, repetitive tasks can feel especially draining for you - your mind craves variety and creative challenge. Knowing this helps you understand why you need creative outlets and mental stimulation to feel fulfilled and energized.")
                            elif "Practical" in style:
                                detailed_explanations.append("Your practical processing style means you naturally focus on what works, what's useful, and what produces real results. You're not interested in theory for theory's sake - you want to know how things apply to real life. This makes you incredibly valuable in teams and relationships because you help turn ideas into reality. Understanding this helps you appreciate your gift for keeping things grounded and actionable.")
                        
                        elif rationale.startswith("Recommended focus:"):
                            advice = rationale.split(": ")[1]
                            # Make the advice more personal and supportive
                            if "rest" in advice.lower() or "sleep" in advice.lower():
                                detailed_explanations.append("Listen, I know you might feel like resting is giving up or being lazy, but that's not true. Your body and mind are asking for restoration because you've been working hard - and that's something to honor, not push through. Think of rest not as stopping, but as the pause that makes the next movement possible. You deserve this care, and taking it doesn't make you weak - it makes you wise.")
                            elif "balance" in advice.lower():
                                detailed_explanations.append("Balance isn't about perfect equilibrium every single day - it's about the rhythm of giving and receiving, effort and ease, over time. Right now, you might need to consciously tip the scales toward self-care because you've been leaning heavily into giving. This isn't selfish; it's necessary. You can't pour from an empty cup, and the people who truly care about you want you to be well.")
                            elif "boundaries" in advice.lower():
                                detailed_explanations.append("Setting boundaries might feel uncomfortable at first, especially if you're used to saying yes to everything. But boundaries aren't walls - they're like the banks of a river that help your energy flow in a sustainable direction. You're not being mean when you protect your time and energy; you're being responsible to yourself and ultimately more available to the people and things that truly matter.")
                            elif "support" in advice.lower():
                                detailed_explanations.append("I know asking for help can feel vulnerable, like admitting you can't handle everything alone. But here's the truth - you were never meant to handle everything alone. Reaching out for support isn't failure; it's wisdom. The people who care about you want to help, and letting them do so actually strengthens your relationships. You've probably been there for others countless times - it's okay to let others be there for you too.")
                            else:
                                detailed_explanations.append(f"Here's what I want you to focus on: {advice}. This isn't just generic advice - it's specifically what your current situation is calling for. Trust that this guidance comes from understanding your unique patterns and needs. You have the wisdom within you to know what feels right; sometimes you just need permission to honor what you already know.")
                        
                        elif not any(skip in rationale for skip in ["Element profile:", "Primary element influence:", "Current burnout risk level:", "Cognitive processing style:", "Recommended focus:", "Chronotype Analysis Preferences:"]):
                            # Keep other rationale items that aren't technical
                            detailed_explanations.append(rationale)
                    
                    # Add chronotype preferences at the beginning if available
                    if chronotype_preferences:
                        profile_summary += f"\n**Chronotype Analysis Preferences**\n{chronotype_preferences}\n\n"
                    
                    # Add the detailed explanations to the profile summary
                    for explanation in detailed_explanations:
                        if explanation.startswith("•"):
                            profile_summary += f"{explanation}\n"
                        else:
                            profile_summary += f"• {explanation}\n\n"
                
                st.info(profile_summary)
                
                # Burnout timing analysis
                st.markdown("⏰ **Possible Burn Risk Timing**")
                st.markdown("*Personalized Calendar of Risk and Recovery Possibilities*")
                st.caption("📋 Based on energy possibility patterns, not dynamically calculated")
                timing_info = chrono_result['burnout_timing']
                
                if timing_info['current_risk'] == "High":
                    st.warning(f"🚨 Current Risk Level: **{timing_info['current_risk']}**")
                elif timing_info['current_risk'] == "Low":
                    st.success(f"✅ Current Risk Level: **{timing_info['current_risk']}**")
                else:
                    st.info(f"📊 Current Risk Level: **{timing_info['current_risk']}**")
                
                st.markdown(f"**Next High-Risk Month:** {timing_info['next_high_risk_month']}")
                st.markdown(f"**Recovery Months:** {', '.join(map(str, timing_info['recovery_months']))}")
                
                # Recovery strategies
                st.markdown("💡 **Personalized Recovery Strategies**")
                recommendations = chrono_result['recommendations']
                for strategy, advice in recommendations.items():
                    st.markdown(f"**{strategy.replace('_', ' ').title()}:** {advice}")
                
                # Symptoms consideration
                if st.session_state.selected_symptoms:
                    st.warning("⚠️ Symptoms suggest elevated stress. Consider the timing recommendations above for optimal recovery planning.")
                else:
                    st.success("✅ No symptoms selected — use the chronotype insights for preventive wellness planning.")
                
                # Add reset button
                st.markdown('<div style="margin: 2rem 0; text-align: center;">', unsafe_allow_html=True)
                if st.button("🔄 Run New Analysis", key="reset_button_temporal"):
                    # Clear analysis state
                    st.session_state.run_analysis = False
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # Full analysis with biometric simulation (existing flow)
            st.subheader("🔬 Full Behavioral & Biometric Analysis")

            # Progress indicator for Full Analysis
            with st.spinner("🧠 Running comprehensive biometric and behavioral pattern analysis..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Generate signal data
                status_text.text("📡 Generating biometric signal data...")
                progress_bar.progress(15)
                signal_packet = get_current_signal()
                summary = summarize_signal_packet(signal_packet)
                
                # Step 2: Log signal data
                status_text.text("💾 Logging signal data...")
                progress_bar.progress(25)
                append_signal_log(signal_packet, SIGNAL_LOG_PATH)

                # Step 3: Process behavioral patterns
                status_text.text("🔍 Analyzing behavioral signature patterns...")
                progress_bar.progress(40)
                dob_str = st.session_state.dob.strftime("%Y-%m-%d")
                mapped_profile = map_traits_to_behavioral_pattern(dob_str)
                pattern_tags = mapped_profile["pattern_tags"]

                # Step 4: Run AI inference
                status_text.text("🤖 Running Gemma AI inference...")
                progress_bar.progress(65)
                inference_result = run_inference(pattern_tags, signal_packet)
                
                # Step 5: Match signals to profile
                status_text.text("🎯 Matching signals to behavioral profile...")
                progress_bar.progress(80)
                match_result = match_signal_to_profile(signal_packet, pattern_tags)
                
                # Step 6: Generate final insights
                status_text.text("💡 Generating personalized insights...")
                progress_bar.progress(95)
                final_insight = generate_insight(match_result, inference_result["inference"])
                prompt_text = format_for_ollama_prompt(signal_packet)
                
                # Create pattern summary for technical display
                pattern_summary = f"""Pattern Tags: {pattern_tags}
Mapped Profile: {mapped_profile}
Signal Strength: {signal_packet.get('signal_strength', 'N/A')}
Timestamp: {signal_packet.get('timestamp', 'N/A')}"""
                
                # Complete
                progress_bar.progress(100)
                status_text.text("✅ Comprehensive analysis complete!")
            
            st.markdown(f"Hi **{st.session_state.nickname}**, based on your Behavioral Signature and real-time signal data:")
            
            # Add detailed behavioral signature personality analysis (same as Pattern analysis mode)
            st.markdown("🔍 **Your Behavioral Signature Profile**")
            
            # Get the signature name for detailed personality analysis
            dob_str_formatted = st.session_state.dob.strftime("%d/%m/%Y")
            from private.chrono_decoder import get_chrono_profile_without_biometrics
            chrono_result = get_chrono_profile_without_biometrics(dob_str_formatted)
            
            if "error" not in chrono_result:
                # Get the signature name for internal reference (but don't show Chinese name to user)
                signature_name = chrono_result['chrono_signature']
                
                # Create detailed trait explanation based on signature
                trait_explanations = {
                    "Ji-Chou": """You are naturally stable, loyal, and practical, with a humble nature that often leads you to support others from behind the scenes. There's something deeply reliable about you that people instinctively trust. However, you sometimes tend to bottle up your emotions, overthink situations, and silently strive for perfection, which can create internal turbulence even when you appear calm on the surface.

Your tendency toward emotional suppression means you rarely show anger openly, instead holding it in until it builds up. This can be both a strength and a challenge - while others see you as steady and composed, you may be wrestling with unexpressed feelings internally.

The downside of this personality pattern is that you may feel particularly drained when you lack clear direction or purpose in life. You might find yourself falling into cycles of overthinking, especially when the environment around you feels uncertain or unstable. There's also a potential for you to become overly passive during stressful periods, waiting for things to settle rather than taking decisive action.""",
                    
                    "Jia-Zi": """You possess an innovative and pioneering spirit that naturally positions you as a leader. There's an independence about you that drives strong initiative, and you tend to approach life with confidence and ambition, always seeking new opportunities and challenges to conquer.

Your natural inclination is toward impatience when it comes to seeing results. You often want immediate outcomes and may find yourself rushing into decisions without fully considering all the implications. This drive for quick action can be both your greatest asset and your biggest challenge.

When stress builds up, you might notice yourself becoming overly aggressive or domineering with others. You may struggle with delegation, preferring to handle things yourself rather than trust others to meet your standards. Criticism or feedback from others can be particularly difficult for you to accept, as it conflicts with your natural confidence and self-reliance.""",
                    
                    "Yi-Chou": """You have a naturally nurturing and flexible disposition, combined with strong emotional intelligence that allows you to understand others' needs intuitively. There's a diplomatic quality about you that helps you adapt to different situations with grace and patience, making you someone others feel comfortable turning to for support.

Your instinct is often to prioritize harmony and avoid conflict, sometimes at the expense of your own needs. You may find yourself saying yes when you'd rather say no, or adjusting your preferences to accommodate others' comfort.

This people-pleasing tendency can lead to difficulty making decisions when important choices arise, especially when those decisions might disappoint someone. You might struggle with setting clear boundaries, and there's a risk of internalizing others' emotions to the point where external stress becomes overwhelming for you personally.""",
                    
                    "Bing-Yin": """You carry a passionate and creative energy that naturally draws others to you through your charisma and enthusiasm. There's an intuitive quality about you that allows you to inspire and motivate people, often becoming the spark that ignites action in group settings.

Your emotional intensity can be both magnetic and challenging - you experience feelings deeply and may have dramatic reactions that others sometimes perceive as temperamental or unpredictable. This intensity fuels your creativity but can also make your emotional landscape feel turbulent.

The challenge with this vibrant energy is that you may burn out quickly from overcommitting yourself to too many projects or causes. Consistency in long-term endeavors can be difficult when your passion shifts or wanes. When you're not receiving the attention or recognition you desire, there's a risk of becoming manipulative in your attempts to regain that spotlight."""
                }
                
                # Get the detailed explanation or provide a comprehensive fallback
                if signature_name in trait_explanations:
                    explanation = trait_explanations[signature_name]
                    profile_summary = f"{explanation}\n\n**Your Pattern Tags:**\n{', '.join(chrono_result['pattern_tags'])}"
                else:
                    # Fallback for unknown signatures - provide detailed human-centered explanations
                    profile_summary = f"""**Your Behavioral Profile:** Based on your temporal pattern analysis

**Pattern Tags:** {', '.join(chrono_result['pattern_tags'])}

"""
                    
                    # Transform technical details into human-centered explanations
                    detailed_explanations = []
                    chronotype_preferences = ""
                    
                    for rationale in chrono_result['rationale']:
                        # Don't show technical element names, show detailed explanations instead
                        if rationale.startswith("Chronotype Analysis Preferences:"):
                            chronotype_preferences = rationale.split(": ")[1]
                        elif rationale.startswith("Primary element influence:"):
                            element = rationale.split(": ")[1]
                            if "Fire" in element:
                                detailed_explanations.append("Your inner energy burns bright and passionate. You're someone who feels things intensely and approaches life with enthusiasm, but this same passion that drives your creativity can sometimes lead to burnout if you don't pace yourself. You thrive on excitement and new challenges, yet you need to remember to nurture your energy rather than let it consume you.")
                            elif "Earth" in element:
                                detailed_explanations.append("There's a grounding, stabilizing quality about you that others find deeply comforting. You have this natural ability to remain steady during storms, to be the rock that others lean on. However, this same stability can sometimes make you feel stuck or resistant to change. You process things slowly and thoroughly, which is a strength, but remember that growth sometimes requires stepping out of your comfort zone.")
                            elif "Water" in element:
                                detailed_explanations.append("You flow with an intuitive understanding of emotions - both your own and others'. There's a depth to you that runs much deeper than what people see on the surface. You adapt naturally to different situations, taking the shape that's needed in each moment. This emotional intelligence is your gift, but be careful not to absorb everyone else's feelings to the point where you lose touch with your own needs.")
                            elif "Metal" in element:
                                detailed_explanations.append("You have a sharp, analytical mind that cuts through confusion to find clarity. There's a precision about the way you think and approach problems that others admire. You value structure, quality, and doing things the right way. However, this same clarity can sometimes make you overly critical - of yourself and others. Remember that perfection isn't always necessary, and sometimes 'good enough' really is enough.")
                            elif "Wood" in element:
                                detailed_explanations.append("You're naturally growth-oriented, always reaching toward something better, constantly stretching toward new possibilities. There's an optimistic, forward-thinking quality about you that inspires others. You see potential everywhere and have this wonderful ability to help things flourish. Just remember that even the strongest growth needs seasons of rest - constant expansion without pause can lead to exhaustion.")
                        
                        elif rationale.startswith("Current burnout risk level:"):
                            risk_level = rationale.split(": ")[1]
                            if "High" in risk_level:
                                detailed_explanations.append("Right now, your system is sending clear signals that you're running on empty. This isn't a judgment - it's your body and mind's way of asking for care. High burnout risk means you've been giving so much of yourself that your reserves are depleted. Think of it like a phone battery that's been running intensive apps all day - you need to plug in and recharge, not just for a few minutes, but for real restoration.")
                            elif "Medium" in risk_level:
                                detailed_explanations.append("You're in that yellow zone where things are manageable, but you can feel the strain building. It's like when you're carrying groceries and they're not too heavy yet, but you can sense that your arms are getting tired. This is actually the perfect time to make adjustments - before you reach that overwhelming point. Your awareness of this moderate stress level shows you're tuned into your own needs.")
                            elif "Low" in risk_level:
                                detailed_explanations.append("You're in a good space right now - your energy levels are sustainable and you're managing life's demands without feeling overwhelmed. This is what balance feels like, though it's not static. Think of it as sailing with favorable winds - enjoy this period while staying aware that conditions can change, and use this time to build healthy habits that will support you when things get more challenging.")
                        
                        elif rationale.startswith("Cognitive processing style:"):
                            style = rationale.split(": ")[1]
                            if "Analytical" in style:
                                detailed_explanations.append("Understanding your analytical nature helps explain why you need time to process information thoroughly before making decisions. You're not slow - you're thorough. This is why rushed decisions often feel uncomfortable for you, and why you perform best when given space to think things through. In a world that often demands quick responses, knowing this about yourself means you can advocate for the time you need to do your best work.")
                            elif "Intuitive" in style:
                                detailed_explanations.append("Your intuitive processing style means you often 'know' things before you can explain why. This isn't mystical - it's your brain rapidly processing patterns and information below conscious awareness. Understanding this helps you trust those gut feelings and also explains why you might struggle in environments that demand only logical, step-by-step reasoning. Your intuition is a powerful tool when you learn to balance it with practical considerations.")
                            elif "Creative" in style:
                                detailed_explanations.append("Your creative processing style means your brain makes connections that others might miss, finding novel solutions and seeing possibilities where others see problems. This is why routine, repetitive tasks can feel especially draining for you - your mind craves variety and creative challenge. Knowing this helps you understand why you need creative outlets and mental stimulation to feel fulfilled and energized.")
                            elif "Practical" in style:
                                detailed_explanations.append("Your practical processing style means you naturally focus on what works, what's useful, and what produces real results. You're not interested in theory for theory's sake - you want to know how things apply to real life. This makes you incredibly valuable in teams and relationships because you help turn ideas into reality. Understanding this helps you appreciate your gift for keeping things grounded and actionable.")
                        
                        elif rationale.startswith("Recommended focus:"):
                            advice = rationale.split(": ")[1]
                            # Make the advice more personal and supportive
                            if "rest" in advice.lower() or "sleep" in advice.lower():
                                detailed_explanations.append("Listen, I know you might feel like resting is giving up or being lazy, but that's not true. Your body and mind are asking for restoration because you've been working hard - and that's something to honor, not push through. Think of rest not as stopping, but as the pause that makes the next movement possible. You deserve this care, and taking it doesn't make you weak - it makes you wise.")
                            elif "balance" in advice.lower():
                                detailed_explanations.append("Balance isn't about perfect equilibrium every single day - it's about the rhythm of giving and receiving, effort and ease, over time. Right now, you might need to consciously tip the scales toward self-care because you've been leaning heavily into giving. This isn't selfish; it's necessary. You can't pour from an empty cup, and the people who truly care about you want you to be well.")
                            elif "boundaries" in advice.lower():
                                detailed_explanations.append("Setting boundaries might feel uncomfortable at first, especially if you're used to saying yes to everything. But boundaries aren't walls - they're like the banks of a river that help your energy flow in a sustainable direction. You're not being mean when you protect your time and energy; you're being responsible to yourself and ultimately more available to the people and things that truly matter.")
                            elif "support" in advice.lower():
                                detailed_explanations.append("I know asking for help can feel vulnerable, like admitting you can't handle everything alone. But here's the truth - you were never meant to handle everything alone. Reaching out for support isn't failure; it's wisdom. The people who care about you want to help, and letting them do so actually strengthens your relationships. You've probably been there for others countless times - it's okay to let others be there for you too.")
                            else:
                                detailed_explanations.append(f"Here's what I want you to focus on: {advice}. This isn't just generic advice - it's specifically what your current situation is calling for. Trust that this guidance comes from understanding your unique patterns and needs. You have the wisdom within you to know what feels right; sometimes you just need permission to honor what you already know.")
                        
                        elif not any(skip in rationale for skip in ["Element profile:", "Primary element influence:", "Current burnout risk level:", "Cognitive processing style:", "Recommended focus:", "Chronotype Analysis Preferences:"]):
                            # Keep other rationale items that aren't technical
                            detailed_explanations.append(rationale)
                    
                    # Add chronotype preferences at the beginning if available
                    if chronotype_preferences:
                        profile_summary += f"\n**Chronotype Analysis Preferences**\n{chronotype_preferences}\n\n"
                    
                    # Add the detailed explanations to the profile summary
                    for explanation in detailed_explanations:
                        if explanation.startswith("•"):
                            profile_summary += f"{explanation}\n"
                        else:
                            profile_summary += f"• {explanation}\n\n"
                
                st.info(profile_summary)
                
                # Add Burnout timing analysis from temporal pattern analysis
                st.markdown("⏰ **Possible Burn Risk Timing Analysis**")
                st.markdown("*Personalized Calendar of Risk and Recovery Possibilities*")
                st.caption("📋 Based on energy possibility patterns, not dynamically calculated")
                timing_info = chrono_result['burnout_timing']
                
                if timing_info['current_risk'] == "High":
                    st.warning(f"🚨 Current Risk Level: **{timing_info['current_risk']}**")
                elif timing_info['current_risk'] == "Low":
                    st.success(f"✅ Current Risk Level: **{timing_info['current_risk']}**")
                else:
                    st.info(f"📊 Current Risk Level: **{timing_info['current_risk']}**")
                
                st.markdown(f"**Next High-Risk Month:** {timing_info['next_high_risk_month']}")
                st.markdown(f"**Recovery Months:** {', '.join(map(str, timing_info['recovery_months']))}")
                
                # Recovery strategies from temporal analysis
                st.markdown("💡 **Personalized Recovery Strategies**")
                recommendations = chrono_result['recommendations']
                for strategy, advice in recommendations.items():
                    st.markdown(f"**{strategy.replace('_', ' ').title()}:** {advice}")
            
            st.markdown("---")
            st.markdown("📊 **Biometric Signal Analysis**")
            st.code(summary)
            
            # Add EDA Level Visualization
            st.markdown("⚡ **Electrodermal Activity (EDA) Level**")
            
            # Extract EDA value from signal packet
            current_eda = signal_packet.get('skin_conductance', 0)
            
            # Define EDA ranges and status
            eda_min = 0.5
            eda_max = 6.0
            eda_ranges = {
                "Very Low": (0.5, 1.5, "🟢"),     # Green - Relaxed
                "Low": (1.5, 2.5, "🟡"),          # Yellow - Normal
                "Moderate": (2.5, 3.5, "🟠"),     # Orange - Engaged  
                "High": (3.5, 4.5, "🔴"),         # Red - Stressed
                "Very High": (4.5, 6.0, "🚨")     # Alert - High stress
            }
            
            # Determine current status
            current_status = "Unknown"
            current_color = "⚪"
            for status, (min_val, max_val, color) in eda_ranges.items():
                if min_val <= current_eda <= max_val:
                    current_status = status
                    current_color = color
                    break
            
            # Create visual representation
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Progress bar showing current position
                progress_value = (current_eda - eda_min) / (eda_max - eda_min)
                st.progress(progress_value)
                
                # EDA range indicators
                st.markdown("**EDA Range Guide:**")
                for status, (min_val, max_val, color) in eda_ranges.items():
                    range_text = f"{color} **{status}**: {min_val} - {max_val} µS"
                    if status == current_status:
                        st.markdown(f"👉 {range_text} ← **Your current level**")
                    else:
                        st.markdown(f"   {range_text}")
            
            with col2:
                # Current reading display
                st.metric(
                    label="Current EDA",
                    value=f"{current_eda} µS",
                    delta=None
                )
                
                # Status indicator
                if current_status in ["Very Low", "Low"]:
                    st.success(f"{current_color} {current_status} - Relaxed state")
                elif current_status == "Moderate":
                    st.info(f"{current_color} {current_status} - Normal engagement")
                elif current_status == "High":
                    st.warning(f"{current_color} {current_status} - Elevated stress")
                else:  # Very High
                    st.error(f"{current_color} {current_status} - High stress alert")
            
            # Educational legend for EDA levels
            st.markdown("📚 **Understanding EDA Stress Levels:**")
            
            # Create expandable information about each level
            with st.expander("ℹ️ Detailed EDA Level Information"):
                st.markdown("""
**🟢 Very Low (0.5-1.5 µS):** Deep relaxation state
- Your body is in a calm, restful condition
- Low sympathetic nervous system activity
- Ideal for recovery, meditation, or peaceful activities
- May indicate you're well-rested and stress-free

**🟡 Low (1.5-2.5 µS):** Normal baseline state  
- Typical everyday relaxed awareness
- Balanced autonomic nervous system
- Good for routine tasks and casual social interaction
- Indicates healthy stress management

**🟠 Moderate (2.5-3.5 µS):** Engaged and alert state
- Active concentration and mental engagement
- Normal response to interesting or challenging tasks
- Heightened awareness without distress
- Optimal for learning and productive work

**🔴 High (3.5-4.5 µS):** Elevated stress response
- Your body is responding to perceived pressure or demands
- Increased sympathetic nervous system activation
- May indicate anxiety, frustration, or mental strain
- Time to consider stress management techniques

**🚨 Very High (4.5-6.0 µS):** High stress alert
- Significant physiological stress response
- Fight-or-flight system highly activated
- May indicate overwhelming pressure or acute stress
- Immediate attention to stress reduction recommended
                """)
                
                st.info("💡 **Remember:** EDA levels naturally fluctuate throughout the day. These readings help you understand your current stress state and make informed decisions about rest, activity, and self-care.")
            
            st.markdown("---")

            # Hidden from user interface - Technical profile kept for internal use
            # st.markdown("🧬 **Technical Chrono-Signature Profile**")
            # st.code(pattern_summary)

            if st.session_state.selected_symptoms:
                st.warning("⚠️ Symptoms suggest elevated stress or burnout risk.")
            else:
                st.success("✅ No symptoms selected — baseline stress indicators appear stable.")

            st.markdown("📊 **Gemma Insight Summary**")
            st.info(final_insight["summary"])
            st.success(final_insight["recommendation"])

            # Hidden from user interface - Technical debugging kept for internal use
            # st.markdown("🧪 **Generated Prompt to Ollama** (for LLM integration)")
            # st.code(prompt_text)
            
            # 🧬 Metadata Footer
            
            with st.expander("🔧 Technical Details"):
                st.markdown(f"🔗 Signal Source: `{signal_packet.get('signal_id', 'N/A')}`")
                st.markdown(f"🧬 Model Reference: `{inference_result.get('llm_model', 'Unknown Model')}`")
            
            # Add reset button
            st.markdown('<div style="margin: 2rem 0; text-align: center;">', unsafe_allow_html=True)
            if st.button("🔄 Run New Analysis", key="reset_button"):
                # Clear analysis state
                st.session_state.run_analysis = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
