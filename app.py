import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from io import BytesIO
from datetime import datetime
import html

# ============================================================
# AUTOVALUE AI — PREMIUM AUTOMOTIVE EXPERIENCE
# ============================================================

st.set_page_config(
    page_title="AutoValue AI | Future of Car Valuation",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "used_car_price_model.pkl"

# KEEP THE ORIGINAL MODEL FEATURE ORDER
FEATURES = [
    "engine-size",
    "horsepower",
    "highway-mpg",
    "curb-weight",
    "make",
    "fuel-type",
    "body-style",
    "drive-wheels"
]

MAKES = [
    "alfa-romero", "audi", "bmw", "chevrolet", "dodge",
    "honda", "isuzu", "jaguar", "mazda", "mercedes-benz",
    "mercury", "mitsubishi", "nissan", "peugot", "plymouth",
    "porsche", "renault", "saab", "subaru", "toyota",
    "volkswagen", "volvo"
]

FUEL_TYPES = ["gas", "diesel"]
BODY_STYLES = [
    "convertible", "hardtop", "hatchback", "sedan", "wagon"
]
DRIVE_WHEELS = ["4wd", "fwd", "rwd"]

# ============================================================
# CINEMATIC AUTOMOTIVE BACKGROUNDS
# These are automotive photographs, not exact model photographs.
# Each brand uses a working fallback image from this collection.
# ============================================================

CAR_IMAGES = {
    "home": (
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70"
        "?auto=format&fit=crop&w=2400&q=90"
    ),
    "sports": (
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d"
        "?auto=format&fit=crop&w=2400&q=90"
    ),
    "luxury": (
        "https://images.unsplash.com/photo-1563720223185-11003d516935"
        "?auto=format&fit=crop&w=2400&q=90"
    ),
    "modern": (
        "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7"
        "?auto=format&fit=crop&w=2400&q=90"
    ),
    "road": (
        "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2"
        "?auto=format&fit=crop&w=2400&q=90"
    )
}

MAKE_IMAGE_MAP = {
    "alfa-romero": "sports",
    "audi": "luxury",
    "bmw": "sports",
    "chevrolet": "sports",
    "dodge": "sports",
    "honda": "modern",
    "isuzu": "road",
    "jaguar": "luxury",
    "mazda": "modern",
    "mercedes-benz": "luxury",
    "mercury": "modern",
    "mitsubishi": "road",
    "nissan": "modern",
    "peugot": "luxury",
    "plymouth": "sports",
    "porsche": "sports",
    "renault": "modern",
    "saab": "luxury",
    "subaru": "road",
    "toyota": "modern",
    "volkswagen": "modern",
    "volvo": "luxury"
}

# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_CAR = {
    "engine-size": 130,
    "horsepower": 100,
    "highway-mpg": 30,
    "curb-weight": 2500,
    "make": "toyota",
    "fuel-type": "gas",
    "body-style": "sedan",
    "drive-wheels": "fwd"
}

if "step" not in st.session_state:
    st.session_state.step = 0

if "car_data" not in st.session_state:
    st.session_state.car_data = DEFAULT_CAR.copy()

if "prediction" not in st.session_state:
    st.session_state.prediction = None

# ============================================================
# MODEL LOADING
# ============================================================

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
    model_error = None
except Exception as error:
    model = None
    model_error = str(error)

# ============================================================
# BACKGROUND SELECTION
# ============================================================

selected_make = st.session_state.car_data["make"]

image_category = MAKE_IMAGE_MAP.get(selected_make, "home")
background_image = CAR_IMAGES.get(
    image_category,
    CAR_IMAGES["home"]
)

# ============================================================
# PREMIUM DESIGN
# ============================================================

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --accent: #a6e8ff;
    --white: #ffffff;
    --muted: #c6d1dc;
}}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: #050a10;
    color: white;
}}

.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;

    background-image:
        linear-gradient(
            90deg,
            rgba(2,7,13,.94) 0%,
            rgba(2,7,13,.76) 40%,
            rgba(2,7,13,.28) 100%
        ),
        linear-gradient(
            0deg,
            rgba(2,7,13,.78) 0%,
            transparent 65%,
            rgba(2,7,13,.28) 100%
        ),
        url("{background_image}");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;

    animation: cinematic 1.1s ease-out;
}}

@keyframes cinematic {{
    from {{
        opacity: .3;
        transform: scale(1.06);
    }}
    to {{
        opacity: 1;
        transform: scale(1);
    }}
}}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
    background: transparent;
}}

[data-testid="stMain"] {{
    position: relative;
    z-index: 1;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

.block-container {{
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}}

h1, h2, h3, h4 {{
    font-family: 'Manrope', sans-serif;
    color: white;
    letter-spacing: -1.5px;
}}

p, label, span {{
    color: white;
}}

.top-nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 18px;
    border-bottom: 1px solid rgba(255,255,255,.22);
    margin-bottom: 55px;
}}

.logo {{
    font-family: 'Manrope', sans-serif;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 3px;
}}

.logo span {{
    color: var(--accent);
}}

.nav-caption {{
    font-size: 10px;
    letter-spacing: 3px;
    color: #d2e1ec;
}}

.eyebrow {{
    color: var(--accent);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
}}

.hero {{
    padding-top: 65px;
    padding-bottom: 30px;
    max-width: 850px;
}}

.hero h1 {{
    font-size: clamp(55px, 8vw, 105px);
    line-height: .98;
    font-weight: 800;
    margin-top: 22px;
    margin-bottom: 24px;
}}

.hero-description {{
    color: #d4e0eb;
    font-size: 18px;
    line-height: 1.8;
    max-width: 620px;
}}

.page-title {{
    font-size: clamp(38px, 5vw, 65px);
    font-weight: 800;
    line-height: 1.05;
    margin-top: 15px;
    margin-bottom: 15px;
}}

.page-description {{
    color: #d1dce6;
    font-size: 16px;
    line-height: 1.7;
}}

.step-caption {{
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 10px;
}}

.glass-line {{
    height: 1px;
    background: rgba(255,255,255,.23);
    margin: 30px 0;
}}

.glass-pill {{
    display: inline-block;
    padding: 10px 18px;
    border: 1px solid rgba(255,255,255,.38);
    border-radius: 50px;
    background: rgba(255,255,255,.06);
    backdrop-filter: blur(15px);
    font-size: 11px;
    letter-spacing: 2px;
    color: white;
    margin-right: 8px;
    margin-bottom: 8px;
}}

.spec-row {{
    display: flex;
    justify-content: space-between;
    padding: 15px 0;
    border-bottom: 1px solid rgba(255,255,255,.20);
    font-size: 14px;
}}

.spec-row span {{
    color: #c7d4df;
}}

.spec-row strong {{
    color: white;
}}

.price-label {{
    color: var(--accent);
    font-size: 12px;
    letter-spacing: 4px;
    font-weight: 700;
}}

.price-value {{
    font-family: 'Manrope', sans-serif;
    color: var(--accent);
    font-size: clamp(45px, 7vw, 85px);
    font-weight: 800;
    letter-spacing: -4px;
    line-height: 1.1;
    margin-top: 12px;
}}

.stButton > button,
.stDownloadButton > button {{
    border-radius: 50px !important;
    background: white !important;
    color: #07111b !important;
    border: 1px solid white !important;
    font-weight: 800 !important;
    letter-spacing: 1px;
    padding: 14px 25px !important;
    min-height: 48px;
    transition: all .25s ease;
}}

.stButton > button:hover,
.stDownloadButton > button:hover {{
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    transform: translateY(-3px);
}}

.stButton > button p,
.stDownloadButton > button p {{
    color: #07111b !important;
}}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {{
    background: rgba(5,13,22,.78) !important;
    border: 1px solid rgba(255,255,255,.40) !important;
    border-radius: 12px !important;
}}

div[data-baseweb="select"] *,
div[data-baseweb="popover"] * {{
    color: white !important;
}}

.stNumberInput input,
[data-testid="stNumberInput"] input {{
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    background-color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    caret-color: #111111 !important;
}}

[data-testid="stNumberInput"] button {{
    color: #111111 !important;
}}

[data-testid="stNumberInput"] button svg {{
    fill: #111111 !important;
    color: #111111 !important;
}}

/* CUSTOM CIRCULAR CURSOR — clean ring with a small centre dot */
html, body, .stApp, .stApp * {{
    cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='10' fill='none' stroke='%23a6e8ff' stroke-width='2.5'/%3E%3Ccircle cx='16' cy='16' r='2' fill='%23ffffff'/%3E%3C/svg%3E") 16 16, auto !important;
}}

/* Smart hover cursor for buttons and selectable controls */
.stButton > button,
.stDownloadButton > button,
[data-baseweb="select"],
[data-baseweb="select"] *,
[data-testid="stNumberInput"] button,
input[type="checkbox"],
label[for] {{
    cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='36' height='36' viewBox='0 0 36 36'%3E%3Ccircle cx='18' cy='18' r='12' fill='%23a6e8ff' fill-opacity='.18' stroke='%23a6e8ff' stroke-width='2.5'/%3E%3Ccircle cx='18' cy='18' r='3' fill='%23ffffff'/%3E%3C/svg%3E") 18 18, pointer !important;
}}

/* Keep the normal text insertion cursor inside editable fields */
[data-testid="stNumberInput"] input,
[data-baseweb="input"] input,
textarea {{
    cursor: text !important;
}}

.stProgress > div > div > div > div {{
    background: var(--accent) !important;
}}

[data-testid="stProgressBar"] {{
    background: rgba(255,255,255,.22);
}}

[data-testid="stDataFrame"] {{
    background: rgba(4,12,20,.75);
}}

footer, #MainMenu {{
    visibility: hidden;
}}

@media(max-width: 768px) {{
    .top-nav {{
        margin-bottom: 25px;
    }}
    .hero {{
        padding-top: 20px;
    }}
    .hero h1 {{
        font-size: 53px;
    }}
}}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def navigate(step):
    st.session_state.step = step
    st.rerun()


def create_input_dataframe():
    data = st.session_state.car_data

    return pd.DataFrame([{
        "engine-size": data["engine-size"],
        "horsepower": data["horsepower"],
        "highway-mpg": data["highway-mpg"],
        "curb-weight": data["curb-weight"],
        "make": data["make"],
        "fuel-type": data["fuel-type"],
        "body-style": data["body-style"],
        "drive-wheels": data["drive-wheels"]
    }], columns=FEATURES)


def predict_price():
    if model is None:
        if model_error:
            st.error(f"Model loading error: {model_error}")
        else:
            st.error(
                "Model file not found. Keep used_car_price_model.pkl "
                "in the same folder as app.py."
            )
        return None

    try:
        result = model.predict(create_input_dataframe())
        return float(result[0])
    except Exception as error:
        st.error(f"Prediction failed: {error}")
        st.info(
            "Check that your saved model accepts these eight features "
            "with the original training categories."
        )
        return None


def create_pdf_report():
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        st.error("Install ReportLab using: pip install reportlab")
        return None

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    data = st.session_state.car_data
    prediction = st.session_state.prediction

    pdf.setFillColorRGB(0.025, 0.06, 0.10)
    pdf.rect(0, height - 125, width, 125, fill=1, stroke=0)

    pdf.setFillColorRGB(0.65, 0.91, 1)
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawString(45, height - 65, "AUTOVALUE AI")

    pdf.setFillColorRGB(.15, .2, .25)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(45, height - 155, "VEHICLE VALUATION REPORT")
    pdf.drawString(
        45, height - 178,
        datetime.now().strftime("Generated: %d %B %Y, %H:%M")
    )

    y = height - 225
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(45, y, "Vehicle Configuration")
    y -= 30

    pdf.setFont("Helvetica", 11)

    for feature in FEATURES:
        label = feature.replace("-", " ").title()
        pdf.drawString(55, y, f"{label}: {data[feature]}")
        y -= 24

    y -= 15
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(45, y, "MODEL ESTIMATED PRICE (USD)")

    y -= 40
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawString(45, y, f"${prediction:,.2f} USD")

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(
        45, 45,
        "Currency: USD ($), based on the source dataset. This is a machine-learning estimate, not a guaranteed selling price."
    )

    pdf.save()
    buffer.seek(0)
    return buffer


# ============================================================
# TOP NAVIGATION
# ============================================================

st.markdown("""
<div class="top-nav">
    <div>
        <div class="logo">AUTO<span>VALUE</span> AI</div>
        <div class="nav-caption">INTELLIGENT AUTOMOTIVE VALUATION</div>
    </div>
    <div class="nav-caption">THE FUTURE OF VEHICLE PRICING</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# HOME — USE NATIVE STREAMLIT TEXT (NO HTML TAGS IN THE HERO)
# ============================================================

if st.session_state.step == 0:

    st.markdown(
        '<div class="eyebrow">THE NEXT GENERATION OF CAR VALUATION</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.title("Every car.")
    st.title("One intelligent value.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        "Discover the intelligence behind your vehicle's value. "
        "Configure your car, explore its specifications and get "
        "a machine-learning-powered price estimate."
    )

    if st.button("EXPLORE YOUR VEHICLE  →", key="start"):
        navigate(1)

    st.markdown('<div style="height:65px"></div>', unsafe_allow_html=True)

    st.markdown("""
<span class="glass-pill">8 MODEL FEATURES</span>
<span class="glass-pill">MACHINE LEARNING</span>
<span class="glass-pill">INSTANT VALUATION</span>
<span class="glass-pill">PDF REPORT</span>
""", unsafe_allow_html=True)

# ============================================================
# STEP 1 — BRAND
# ============================================================

elif st.session_state.step == 1:

    st.markdown(
        '<div class="page-title">Choose your marque.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-description">Select your vehicle manufacturer. '
        'The cinematic background changes with your selection.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div style="height:25px"></div>', unsafe_allow_html=True)

    current_index = MAKES.index(st.session_state.car_data["make"])

    selected = st.selectbox(
        "SELECT MANUFACTURER",
        MAKES,
        index=current_index,
        format_func=lambda value: value.replace("-", " ").title()
    )

    st.session_state.car_data["make"] = selected
    st.session_state.prediction = None

    st.markdown('<div class="glass-line"></div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="eyebrow">YOUR SELECTED MANUFACTURER</div>'
        f'<h2 style="font-size:45px;">'
        f'{html.escape(selected.replace("-", " ").title())}</h2>',
        unsafe_allow_html=True
    )

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    if st.button("CONTINUE TO PERFORMANCE  →"):
        navigate(2)

    if st.button("← BACK TO HOME"):
        navigate(0)

# ============================================================
# STEP 2 — PERFORMANCE
# ============================================================

elif st.session_state.step == 2:

    st.markdown(
        '<div class="page-title">Power meets precision.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-description">Enter the technical '
        'specifications of your vehicle.</div>',
        unsafe_allow_html=True
    )

    data = st.session_state.car_data

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        data["engine-size"] = st.number_input(
            "ENGINE SIZE",
            min_value=50,
            max_value=1000,
            value=int(data["engine-size"]),
            step=10
        )

        data["horsepower"] = st.number_input(
            "HORSEPOWER",
            min_value=30,
            max_value=500,
            value=int(data["horsepower"]),
            step=5
        )

    with right:
        data["highway-mpg"] = st.number_input(
            "HIGHWAY MPG",
            min_value=5,
            max_value=80,
            value=int(data["highway-mpg"]),
            step=1
        )

        data["curb-weight"] = st.number_input(
            "CURB WEIGHT",
            min_value=1000,
            max_value=6000,
            value=int(data["curb-weight"]),
            step=50
        )

    st.markdown('<div class="glass-line"></div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        if st.button("← PREVIOUS"):
            navigate(1)

    with right:
        if st.button("CONTINUE  →"):
            navigate(3)

# ============================================================
# STEP 3 — VEHICLE CONFIGURATION
# ============================================================

elif st.session_state.step == 3:

    st.markdown(
        '<div class="page-title">Define the details.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-description">Complete your vehicle profile '
        'with its fuel type, body style and drivetrain.</div>',
        unsafe_allow_html=True
    )

    data = st.session_state.car_data

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        data["fuel-type"] = st.selectbox(
            "FUEL TYPE",
            FUEL_TYPES,
            index=FUEL_TYPES.index(data["fuel-type"])
        )

        data["body-style"] = st.selectbox(
            "BODY STYLE",
            BODY_STYLES,
            index=BODY_STYLES.index(data["body-style"])
        )

    with right:
        data["drive-wheels"] = st.selectbox(
            "DRIVE WHEELS",
            DRIVE_WHEELS,
            index=DRIVE_WHEELS.index(data["drive-wheels"])
        )


    st.markdown('<div class="glass-line"></div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        if st.button("← PREVIOUS"):
            navigate(2)

    with right:
        if st.button("REVIEW VEHICLE  →"):
            navigate(4)

# ============================================================
# STEP 4 — REVIEW
# ============================================================

elif st.session_state.step == 4:

    data = st.session_state.car_data

    st.markdown(
        '<div class="page-title">Your vehicle. Your configuration.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-description">Review your specifications '
        'before generating the AI prediction.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown('<div class="eyebrow">SELECTED VEHICLE</div>', unsafe_allow_html=True)

        st.markdown(
            f'<h2 style="font-size:42px;">'
            f'{html.escape(data["make"].replace("-", " ").title())}</h2>',
            unsafe_allow_html=True
        )

        specifications = [
            ("Engine Size", data["engine-size"]),
            ("Horsepower", data["horsepower"]),
            ("Highway MPG", data["highway-mpg"]),
            ("Curb Weight", data["curb-weight"]),
            ("Fuel Type", data["fuel-type"].title()),
            ("Body Style", data["body-style"].title()),
            ("Drive Wheels", data["drive-wheels"].upper())
        ]

        for label, value in specifications:
            st.markdown(
                f'<div class="spec-row">'
                f'<span>{label}</span><strong>{value}</strong></div>',
                unsafe_allow_html=True
            )

    with right:
        st.markdown('<div style="height:35px"></div>', unsafe_allow_html=True)

        st.markdown(
            '<span class="glass-pill">READY FOR VALUATION</span>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<h2 style="font-size:40px;line-height:1.15;">'
            'Let the data<br>reveal the value.</h2>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<p class="page-description">'
            'Your eight vehicle features will be passed to the trained '
            'machine learning model in the original feature order.'
            '</p>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="glass-line"></div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        if st.button("← EDIT CONFIGURATION"):
            navigate(3)

    with right:
        if st.button("GENERATE AI VALUATION  ✦"):
            result = predict_price()

            if result is not None:
                st.session_state.prediction = result
                navigate(5)

# ============================================================
# STEP 5 — RESULT
# ============================================================

elif st.session_state.step == 5:

    data = st.session_state.car_data
    prediction = st.session_state.prediction

    st.markdown(
        '<div class="eyebrow">AUTOVALUE AI — VALUATION COMPLETE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-title">A value, backed by data.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="page-description">'
        f'{html.escape(data["make"].replace("-", " ").title())}'
        f' &nbsp; · &nbsp; {html.escape(data["body-style"].title())}'
        f' &nbsp; · &nbsp; {html.escape(data["fuel-type"].title())}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div style="height:35px"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="price-label">MODEL ESTIMATED PRICE · USD ($)</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="price-value">${prediction:,.2f} USD</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-description">'
        'Generated by your trained machine learning model using '
        'the configured vehicle specifications. Currency: USD ($), '
        'based on the source dataset.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass-line"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="eyebrow">YOUR VEHICLE PROFILE</div>',
        unsafe_allow_html=True
    )

    for feature in FEATURES:
        label = feature.replace("-", " ").title()
        value = data[feature]

        st.markdown(
            f'<div class="spec-row">'
            f'<span>{html.escape(label)}</span>'
            f'<strong>{html.escape(str(value))}</strong></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="glass-line"></div>', unsafe_allow_html=True)

    pdf_report = create_pdf_report()

    left, right = st.columns(2)

    with left:
        if pdf_report is not None:
            st.download_button(
                "DOWNLOAD PDF REPORT  ↓",
                data=pdf_report,
                file_name="AutoValue_AI_Report.pdf",
                mime="application/pdf"
            )

    with right:
        if st.button("START NEW VALUATION  ↗"):
            st.session_state.car_data = DEFAULT_CAR.copy()
            st.session_state.prediction = None
            navigate(0)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style="
    margin-top:80px;
    padding-top:20px;
    border-top:1px solid rgba(255,255,255,.2);
    color:#c6d1dc;
    font-size:10px;
    letter-spacing:3px;">
    AUTOVALUE AI &nbsp; / &nbsp; THE FUTURE OF VEHICLE VALUATION
</div>
""", unsafe_allow_html=True)