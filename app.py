
import os
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

import pandas as pd
import streamlit as st
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ScamLens | Message Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

# =========================================================
# 2. PREMIUM DARK UI
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #080d18;
        --panel: #101827;
        --panel2: #131e30;
        --border: rgba(148, 163, 184, 0.15);
        --cyan: #45e6d2;
        --blue: #60a5fa;
        --muted: #91a0b7;
        --text: #eef4ff;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, rgba(20,184,166,.10), transparent 32%),
            radial-gradient(ellipse at 90% 10%, rgba(59,130,246,.10), transparent 30%),
            var(--bg);
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.6px;
    }

    [data-testid="stSidebar"] {
        background: #0b1220;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] p {
        color: #c4d0e3;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .brand {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 29px;
        font-weight: 700;
        letter-spacing: -1.4px;
        color: #f8fbff;
    }

    .brand span { color: var(--cyan); }

    .eyebrow {
        color: var(--cyan);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero {
        padding: 30px;
        border: 1px solid rgba(69,230,210,.22);
        border-radius: 24px;
        background:
            radial-gradient(circle at 90% 15%, rgba(69,230,210,.14), transparent 28%),
            linear-gradient(135deg, #111d2d 0%, #101827 55%, #0d1928 100%);
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: clamp(30px, 4vw, 47px);
        line-height: 1.1;
        margin: 5px 0 13px 0;
        color: #f4f8ff;
    }

    .hero p {
        color: #a9b8ce;
        max-width: 700px;
        line-height: 1.7;
        font-size: 15px;
    }

    .hero-chip {
        display: inline-block;
        padding: 6px 11px;
        margin-bottom: 12px;
        border: 1px solid rgba(69,230,210,.3);
        border-radius: 99px;
        background: rgba(69,230,210,.08);
        color: var(--cyan);
        font-size: 11px;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .metric {
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 19px;
        min-height: 132px;
        background: linear-gradient(145deg, rgba(20,31,49,.98), rgba(12,21,35,.98));
    }

    .metric-label {
        color: #9eacc1;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        color: #f4f8ff;
        font-size: 32px;
        font-weight: 700;
    }

    .metric-foot {
        color: var(--cyan);
        font-size: 11px;
        margin-top: 8px;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 21px;
        font-weight: 600;
        margin: 12px 0 5px 0;
        color: #f2f6ff;
    }

    .section-subtitle {
        color: #91a0b7;
        font-size: 13px;
        margin-bottom: 17px;
    }

    .signal {
        padding: 13px 15px;
        border-radius: 12px;
        background: rgba(69,230,210,.055);
        border: 1px solid rgba(69,230,210,.17);
        margin: 8px 0;
        color: #d9e8f5;
        font-size: 13px;
    }

    .signal-dot {
        color: var(--cyan);
        font-weight: 700;
        margin-right: 8px;
    }

    .risk-box {
        padding: 22px;
        border-radius: 18px;
        border: 1px solid var(--border);
        background: #101827;
        text-align: center;
    }

    .risk-number {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 48px;
        line-height: 1.2;
        font-weight: 700;
    }

    .risk-caption {
        color: #91a0b7;
        font-size: 12px;
        margin-top: 6px;
    }

    .stTextArea textarea, .stTextInput input {
        background: #0b1422 !important;
        color: #eef4ff !important;
        border-color: #26364b !important;
        border-radius: 12px !important;
    }

    .stSelectbox > div > div {
        background: #0d1726;
        border-color: #26364b;
        border-radius: 10px;
    }

    .stButton > button {
        border-radius: 11px;
        border: 1px solid rgba(69,230,210,.35);
        background: linear-gradient(100deg, #45e6d2, #67d8f2);
        color: #06141b;
        font-weight: 700;
        padding: 10px 17px;
        transition: all .18s ease;
    }

    .stButton > button:hover {
        border-color: #9efff2;
        box-shadow: 0 0 22px rgba(69,230,210,.16);
        color: #06141b;
        transform: translateY(-1px);
    }

    div[data-testid="stForm"] {
        border: 1px solid var(--border);
        border-radius: 17px;
        padding: 20px;
        background: rgba(16,24,39,.65);
    }

    hr { border-color: var(--border); }

    .footer {
        color: #718199;
        font-size: 11px;
        padding-top: 28px;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 3. MONGODB CONNECTION + COLLECTION VALIDATION
# =========================================================

VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "message",
            "risk_score",
            "risk_level",
            "signals",
            "analyzed_at",
        ],
        "properties": {
            "message": {
                "bsonType": "string",
                "minLength": 1,
            },
            "risk_score": {
                "bsonType": ["int", "long"],
                "minimum": 0,
                "maximum": 100,
            },
            "risk_level": {
                "bsonType": "string",
                "enum": ["Low", "Medium", "High"],
            },
            "signals": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
            },
            "analyzed_at": {"bsonType": "date"},
            "review_status": {
                "bsonType": "string",
                "enum": ["Pending", "Reviewed", "Needs Follow-up"],
            },
            "analyst_note": {"bsonType": "string"},
        },
    }
}


@st.cache_resource
def connect_database(uri):
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")

    db = client["scamlens_db"]

    if "analyses" not in db.list_collection_names():
        db.create_collection(
            "analyses",
            validator=VALIDATOR,
            validationLevel="strict",
            validationAction="error",
        )
    else:
        db.command({
            "collMod": "analyses",
            "validator": VALIDATOR,
            "validationLevel": "strict",
            "validationAction": "error",
        })

    collection = db["analyses"]

    # Indexes support common filtering and sorting operations.
    collection.create_index("analyzed_at")
    collection.create_index("risk_level")
    collection.create_index("risk_score")

    return client, collection


# Read the connection string from Streamlit Community Cloud Secrets first,
# then fall back to the local .env/environment variable for development.
try:
    mongo_uri = str(st.secrets.get("MONGODB_URI", "") or "").strip()
except Exception:
    # st.secrets may be unavailable when running locally without secrets.toml.
    mongo_uri = ""

if not mongo_uri:
    mongo_uri = os.getenv("MONGODB_URI", "").strip()

if not mongo_uri:
    st.error(
        "MongoDB URI is missing. For local development, add MONGODB_URI "
        "to your .env file. For Streamlit Community Cloud, add MONGODB_URI "
        "under the app's Settings → Secrets, then reboot the app."
    )
    st.stop()

try:
    client, analyses = connect_database(mongo_uri)
    # Keep the database handle available to custom-pattern loading below.
    db = client["scamlens_db"]
except Exception as exc:
    st.error(
        "Could not connect to MongoDB. Check your Atlas URI, database "
        "user, password, and Network Access settings."
    )
    with st.expander("Technical details"):
        st.code(str(exc))
    st.stop()


# =========================================================
# 4. RULE-BASED MESSAGE ANALYZER
# =========================================================
RULES = [
    # 1. OTP, passwords, and account credentials
    ("OTP or verification code request", 35,
     r"\b(?:otp|one[\s-]?time password|verification code|security code)\b.{0,100}\b(?:share|send|tell|provide|enter|reply|forward|confirm)\b|\b(?:share|send|tell|provide|forward)\b.{0,80}\b(?:otp|verification code|one[\s-]?time password)\b"),
    ("Password or PIN request", 35,
     r"\b(?:share|send|tell|reveal|provide|confirm)\b.{0,70}\b(?:password|passcode|upi pin|atm pin|debit card pin|credit card pin|cvv|security answer)\b|\b(?:password|upi pin|atm pin|cvv)\b.{0,60}\b(?:required|needed|verify|confirm)\b"),
    ("Sensitive banking information request", 30,
     r"\b(?:bank details|card details|account number|card number|cvv|expiry date|net banking credentials)\b.{0,70}\b(?:send|share|provide|submit|verify|update)\b"),

    # 2. Bank, KYC, and account suspension
    ("KYC or bank verification pressure", 20,
     r"\b(?:kyc|re-?kyc|know your customer|bank verification|account verification)\b.{0,100}\b(?:expire|expired|pending|suspend|block|update|complete|verify|fail|deactivat)\w*\b|\b(?:update|complete|verify)\b.{0,60}\bkyc\b"),
    ("Account blocking or suspension threat", 20,
     r"\b(?:account|bank account|upi|sim|card|wallet)\b.{0,100}\b(?:will be|has been|is being|shall be)?\s*(?:blocked|suspended|frozen|deactivated|closed|disabled)\b|\b(?:avoid|prevent)\b.{0,50}\b(?:account block|account suspension|account closure)\b"),
    ("Bank or government impersonation", 20,
     r"\b(?:rbi|reserve bank|income tax department|cyber cell|police department|government officer|bank official|customs officer)\b.{0,100}\b(?:verify|pay|transfer|click|share|submit|urgent|fine|penalty|account)\b"),
    ("Fake customer support or helpline", 20,
     r"\b(?:customer care|customer support|helpline|toll[\s-]?free|support executive)\b.{0,100}\b(?:call this number|whatsapp|share otp|install|remote access|refund fee|verification fee)\b"),

    # 3. UPI, QR codes, and payment fraud
    ("UPI payment or PIN manipulation", 30,
     r"\b(?:upi pin|upi collect|collect request|payment request|qr code|scan (?:the )?qr|receive money|receive your refund)\b"),
    ("Advance payment or processing fee", 25,
     r"\b(?:pay|deposit|transfer|send|submit)\b.{0,70}\b(?:registration fee|processing fee|release fee|activation fee|refundable fee|security deposit|verification fee|customs fee|delivery fee|advance fee|joining fee|gst fee)\b|\b(?:pay|deposit|transfer)\b.{0,40}\b(?:first|in advance|to receive|to unlock|to release)\b"),
    ("Unexpected payment or money transfer", 20,
     r"\b(?:transfer money|send money|pay immediately|make payment now|deposit funds|send the amount|pay to unlock|pay to withdraw)\b"),
    ("Fake refund or failed transaction", 20,
     r"\b(?:refund pending|refund failed|claim your refund|receive your refund|refund processing|failed transaction|reversal pending|cashback pending)\b"),

    # 4. Urgency and threats
    ("Urgent action pressure", 15,
     r"\b(?:immediately|urgent|urgently|right now|within \d+ minutes?|within \d+ hours?|act now|last warning|final notice|time sensitive|today only|expires today)\b"),
    ("Threats, penalties, or legal action", 20,
     r"\b(?:legal action|arrest warrant|police case|account will be blocked|account will be closed|fine will be imposed|penalty will apply|you will be arrested|service will be disconnected|electricity will be cut|sim will be blocked)\b"),
    ("Fear-based service disconnection", 20,
     r"\b(?:electricity connection|power supply|mobile connection|sim card|gas connection|water supply)\b.{0,100}\b(?:disconnect|cut off|terminate|suspend|block)\w*\b"),

    # 5. Prize, lottery, and giveaway fraud
    ("Lottery or prize bait", 25,
     r"\b(?:you have won|you are a winner|winner selected|lucky winner|congratulations.{0,40}(?:won|winner|prize)|lottery winner|claim your prize|prize money|cash prize|won ₹|won rs\.?|won inr)\b"),
    ("Fake giveaway or reward", 20,
     r"\b(?:free iphone|free smartphone|gift voucher|claim your reward|exclusive reward|free gift|special reward|reward points.{0,50}(?:expire|claim|redeem)|lucky draw)\b"),
    ("Prize release payment", 25,
     r"\b(?:claim|release|unlock|receive)\b.{0,70}\b(?:prize|lottery|winnings|reward|gift|cash award)\b.{0,80}\b(?:pay|fee|tax|deposit|transfer)\b"),

    # 6. Job, task, and employment scams
    ("Suspicious job or work-from-home offer", 15,
     r"\b(?:work from home|part[\s-]?time job|easy online job|daily income|earn money online|data entry job|telegram job|whatsapp job|typing job)\b"),
    ("Job registration or joining fee", 25,
     r"\b(?:job|employment|joining|interview|offer letter|work from home)\b.{0,100}\b(?:registration fee|joining fee|training fee|security deposit|pay to apply|payment required)\b"),
    ("Guaranteed earnings or unrealistic returns", 20,
     r"\b(?:guaranteed income|guaranteed profit|earn ₹?\s?\d[\d,]*\s*(?:daily|per day|every day)|double your money|no work required|risk[\s-]?free returns|100% guaranteed returns)\b"),

    # 7. Investment, trading, and crypto fraud
    ("Unrealistic investment promises", 25,
     r"\b(?:guaranteed returns|double your investment|instant profit|risk free investment|assured profit|daily profit|fixed daily returns|100% returns|huge returns)\b"),
    ("Suspicious crypto or trading scheme", 20,
     r"\b(?:crypto investment|bitcoin investment|trading signals|investment group|crypto doubling|forex signals|recover your trading losses|investment plan)\b"),

    # 8. Delivery, parcel, and customs scams
    ("Delivery or parcel payment warning", 15,
     r"\b(?:parcel|package|courier|shipment|delivery)\b.{0,100}\b(?:on hold|held|failed|pending|address issue|pay|fee|customs|redelivery|undelivered)\b"),
    ("Suspicious address confirmation request", 15,
     r"\b(?:confirm|update|verify)\b.{0,60}\b(?:delivery address|shipping address|parcel address|delivery details)\b"),

    # 9. Phishing links and suspicious websites
    ("Link detected", 10,
     r"https?://[^\s<>]+|www\.[^\s<>]+"),
    ("URL uses an IP address", 25,
     r"https?://(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?"),
    ("URL contains an at-sign or deceptive structure", 25,
     r"https?://[^/\s]*@"),
    ("URL contains suspicious wording", 15,
     r"https?://[^\s<>]*(?:verify-account|login-secure|claim-prize|free-reward|kyc-update|account-unlock|bank-verify|urgent-payment)[^\s<>]*"),
    ("URL uses an internationalized domain", 20,
     r"https?://(?:xn--|[^/\s]*\.xn--)[^\s/]*"),

    # 10. Remote access and malicious app installation
    ("Remote access or screen-sharing request", 35,
     r"\b(?:install|download)\b.{0,80}\b(?:anydesk|teamviewer|quick.?support|remote access app|screen.?sharing app|remote control app)\b|\b(?:give|grant|enable)\b.{0,60}\b(?:remote access|screen sharing|accessibility permission)\b"),
    ("Suspicious APK or unknown app installation", 25,
     r"\b(?:install this apk|download this apk|install unknown app|install this application to receive|enable unknown sources)\b"),

    # 11. Impersonation and account recovery
    ("Friend or family emergency money request", 20,
     r"\b(?:i lost my phone|new number|my phone is broken|urgent help needed|emergency money|send me money urgently|please transfer money)\b"),
    ("Fake parcel, bank, or account verification link", 20,
     r"\b(?:verify your account|confirm your bank account|reactivate your account|unlock your account|update your banking details)\b"),
    ("Request to keep transaction secret", 20,
     r"\b(?:keep this confidential|do not tell anyone|don't tell anyone|secret transaction|keep it secret|do not share this with anyone)\b"),

    # 12. Common Indian-language / Hinglish indicators
    ("Hinglish OTP or PIN request", 35,
     r"\b(?:otp batao|otp bhejo|otp share karo|pin batao|upi pin dalo|otp forward karo|password bhejo|otp dena padega)\b"),
    ("Hinglish payment pressure", 20,
     r"\b(?:abhi paise bhejo|turant payment karo|pehle paise jama karo|registration ke paise|reward lene ke liye pay|account band ho jayega|sim band ho jayega)\b"),
    ("Hinglish KYC or account threat", 20,
     r"\b(?:kyc update karo|kyc nahi kiya|account block ho jayega|bank account band|aapka account band|bijli connection kat jayega)\b"),
    ("Hindi prize or lottery bait", 20,
     r"\b(?:aapne inaam jeeta|lottery jeet gaye|inaam prapt karein|inaam lene ke liye|lakh rupaye jeete|muft gift mila)\b"),

    # 13. Other social engineering patterns
    ("Identity document request", 20,
     r"\b(?:send|share|upload|submit)\b.{0,60}\b(?:aadhaar|aadhar|pan card|passport|identity proof|id proof)\b.{0,80}\b(?:whatsapp|personal number|urgent|verify|claim|receive|unlock)?\b"),
    ("Suspicious payment through gift cards", 25,
     r"\b(?:gift card|itunes card|google play card|voucher code)\b.{0,80}\b(?:payment|pay|send the code|transfer|fee|tax)\b"),
    ("Unsolicited account recovery service", 20,
     r"\b(?:recover your account|recover hacked account|unblock your account|restore your account)\b.{0,80}\b(?:pay|fee|send otp|share password|deposit)\b"),
]


def get_mongodb_custom_rules():
    """
    Load extra rules from the MongoDB collection named scam_patterns.

    Expected document:
    {
        "signal": "Custom scam phrase",
        "pattern": "exact phrase or regex",
        "weight": 25,
        "active": True
    }

    If the collection is empty or unavailable, built-in rules still work.
    """
    custom_rules = []

    try:
        # Uses the existing global MongoDB database variable named `db`.
        collection = db["scam_patterns"]

        for item in collection.find({"active": True}):
            signal = str(item.get("signal", "Custom warning pattern"))
            pattern = str(item.get("pattern", ""))
            weight = int(item.get("weight", 20))

            if pattern and 1 <= weight <= 40:
                try:
                    re.compile(pattern, flags=re.IGNORECASE)
                    custom_rules.append((signal, weight, pattern))
                except re.error:
                    # Ignore invalid patterns instead of breaking the scanner.
                    continue

    except Exception:
        # Keep the scanner usable if the custom collection is not yet available.
        pass

    return custom_rules


def analyze_message(message):
    text = str(message or "").strip()

    if not text:
        return {
            "risk_score": 0,
            "risk_level": "Low",
            "signals": [],
            "explanation": (
                "No message was provided. Enter a message to analyze."
            ),
        }

    signals = []
    matched_categories = set()
    score = 0

    # Combine built-in rules with additional rules stored in MongoDB.
    all_rules = RULES + get_mongodb_custom_rules()

    for signal, weight, pattern in all_rules:
        try:
            matched = re.search(
                pattern,
                text,
                flags=re.IGNORECASE | re.DOTALL
            )
        except re.error:
            matched = None

        if matched and signal not in matched_categories:
            matched_categories.add(signal)
            signals.append(signal)
            score += weight

    # Additional URL structure checks.
    urls = re.findall(
        r"https?://[^\s<>\"']+|www\.[^\s<>\"']+",
        text,
        flags=re.IGNORECASE
    )

    for url in urls:
        clean_url = url.rstrip(".,!?;:)")
        candidate = (
            clean_url
            if clean_url.lower().startswith(("http://", "https://"))
            else "https://" + clean_url
        )

        try:
            parsed = urlparse(candidate)
            host = (parsed.hostname or "").lower()

            if not host or "." not in host:
                signal = "Unusual or unclear URL structure"
                weight = 20
            elif host.startswith("xn--") or ".xn--" in host:
                signal = "Internationalized domain requiring extra scrutiny"
                weight = 20
            else:
                # A link alone is not enough to classify a message as a scam.
                signal = "Link detected — verify the destination independently"
                weight = 10

            if signal not in matched_categories:
                matched_categories.add(signal)
                signals.append(signal)
                score += weight

        except ValueError:
            signal = "URL could not be parsed"
            if signal not in matched_categories:
                matched_categories.add(signal)
                signals.append(signal)
                score += 20

    score = min(score, 100)

    # Preserve the existing Low / Medium / High values for dashboard
    # compatibility. A Low score does not mean the message is safe.
    if score >= 60:
        risk_level = "High"
    elif score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    if not signals:
        explanation = (
            "Unclassified: no known warning patterns matched. "
            "This is not proof that the message is legitimate. "
            "Verify the sender independently, especially before sending "
            "money, sharing credentials, or opening links."
        )
    else:
        explanation = (
            "The score is based on matched built-in and MongoDB-stored "
            "warning patterns. It is a rule-based screening score, not a "
            "verified probability of fraud. Review the matched signals "
            "and independently verify the sender before taking action."
        )

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "signals": signals,
        "explanation": explanation,
    }

# =========================================================
# 5. DATABASE FUNCTIONS — CRUD + AGGREGATION
# =========================================================

def save_analysis(message, result):
    document = {
        "message": message.strip(),
        "risk_score": int(result["risk_score"]),
        "risk_level": result["risk_level"],
        "signals": result["signals"],
        "analyzed_at": datetime.now(timezone.utc),
        "review_status": "Pending",
        "analyst_note": "",
    }
    return analyses.insert_one(document)


def get_recent_analyses(limit=500):
    return list(
        analyses.find().sort("analyzed_at", -1).limit(limit)
    )


def update_review(record_id, status, note):
    return analyses.update_one(
        {"_id": ObjectId(record_id)},
        {
            "$set": {
                "review_status": status,
                "analyst_note": note,
            }
        },
    )


def delete_analysis(record_id):
    return analyses.delete_one({"_id": ObjectId(record_id)})


def get_risk_summary():
    return list(
        analyses.aggregate([
            {
                "$group": {
                    "_id": "$risk_level",
                    "total": {"$sum": 1},
                    "average_score": {"$avg": "$risk_score"},
                }
            },
            {"$sort": {"total": -1}},
        ])
    )


def get_signal_summary():
    return list(
        analyses.aggregate([
            {"$unwind": "$signals"},
            {
                "$group": {
                    "_id": "$signals",
                    "total": {"$sum": 1},
                }
            },
            {"$sort": {"total": -1}},
            {"$limit": 10},
        ])
    )


def load_demo_data():
    samples = [
        "Your account will be blocked. Share your OTP immediately.",
        "Congratulations! You have won a free gift. Claim your prize now.",
        "Pay the outstanding amount immediately to avoid service suspension.",
        "Hello, the meeting has been moved to 3 PM. Please confirm.",
        "Your package is waiting. Verify your details through this link.",
        "Please review the project notes before tomorrow's meeting.",
    ]

    documents = []

    for message in samples:
        result = analyze_message(message)
        documents.append({
            "message": message,
            "risk_score": int(result["risk_score"]),
            "risk_level": result["risk_level"],
            "signals": result["signals"],
            "analyzed_at": datetime.now(timezone.utc),
            "review_status": "Pending",
            "analyst_note": "Fictional demonstration record",
        })

    if documents:
        analyses.insert_many(documents)

    return len(documents)


# =========================================================
# 6. HELPER FUNCTIONS
# =========================================================

def format_time(value):
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y, %I:%M %p")
    return "—"


def metric_card(label, value, foot):
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_color(level):
    return {
        "High": "#fb7185",
        "Medium": "#fbbf24",
        "Low": "#45e6d2",
    }.get(level, "#91a0b7")


def page_header(kicker, title, description):
    st.markdown(
        f"""
        <div class="eyebrow">{kicker}</div>
        <h1 style="margin-top:0">{title}</h1>
        <p style="color:#91a0b7;margin-top:-5px;margin-bottom:25px">
            {description}
        </p>
        """,
        unsafe_allow_html=True,
    )

nav_options = [
    "Overview",
    "Message Scanner",
    "Analysis History",
    "Pattern Explorer",
    "About ScamLens",
]

nav_target = st.session_state.pop("navigation_target", "Overview")

# =========================================================
# 7. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">Scam<span>Lens</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("MESSAGE INTELLIGENCE PLATFORM")
    st.divider()

    page = st.radio(
    "NAVIGATION",
    nav_options,
    index=nav_options.index(nav_target)
    if nav_target in nav_options else 0,
    label_visibility="visible",
)

    st.divider()
    st.markdown("**SYSTEM STATUS**")
    st.success("MongoDB connected")

    total_saved = analyses.count_documents({})
    st.caption(f"{total_saved} saved analysis records")

    st.markdown("---")
    st.caption("SCAMLENS · RULE-BASED ANALYSIS")
    st.caption("Built with Python + MongoDB")


# =========================================================
# 8. OVERVIEW DASHBOARD
# =========================================================

if page == "Overview":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-chip">◉ MESSAGE INTELLIGENCE</div>
            <h1>See the warning signs.<br/>Understand the risk.</h1>
            <p>
                Analyze suspicious messages, understand the patterns
                behind each warning, and explore insights from your
                saved analyses — all in one workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    records = get_recent_analyses()
    total = analyses.count_documents({})
    high = analyses.count_documents({"risk_level": "High"})
    medium = analyses.count_documents({"risk_level": "Medium"})
    low = analyses.count_documents({"risk_level": "Low"})

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("TOTAL ANALYSES", total, "Saved in MongoDB")
    with c2:
        metric_card("HIGH RISK", high, "Heuristic classification")
    with c3:
        metric_card("MEDIUM RISK", medium, "Requires review")
    with c4:
        metric_card("LOW RISK", low, "Fewer matched rules")

    st.markdown("<br/>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1], gap="large")

    with left:
        st.markdown(
            '<div class="section-title">Risk distribution</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-subtitle">Saved records grouped by risk category</div>',
            unsafe_allow_html=True,
        )

        distribution = pd.DataFrame({
            "Risk level": ["High", "Medium", "Low"],
            "Analyses": [high, medium, low],
        }).set_index("Risk level")

        st.bar_chart(distribution, use_container_width=True)

    with right:
        st.markdown(
            '<div class="section-title">Quick actions</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-subtitle">Start scanning or explore your data</div>',
            unsafe_allow_html=True,
        )

        if st.button("＋  Analyze a message", use_container_width=True):
            st.session_state["navigation_target"] = "Message Scanner"
            st.rerun()

        if st.button("⌕  Explore saved patterns", use_container_width=True):
            st.session_state["navigation_target"] = "Pattern Explorer"
            st.rerun()

        if st.button("＋  Load fictional demo data", use_container_width=True):
            try:
                count = load_demo_data()
                st.success(f"Inserted {count} demonstration records.")
                st.rerun()
            except PyMongoError as exc:
                st.error(f"Could not load demo data: {exc}")

        st.info(
            "Demo records are fictional. You can use them to test "
            "the dashboard and aggregation queries."
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Latest analyses</div>',
        unsafe_allow_html=True,
    )

    if records:
        recent_rows = []
        for r in records[:6]:
            recent_rows.append({
                "Message": r["message"][:75],
                "Risk": r["risk_level"],
                "Score": r["risk_score"],
                "Warning signs": len(r.get("signals", [])),
                "Analyzed at": format_time(r.get("analyzed_at")),
            })
        st.dataframe(
            pd.DataFrame(recent_rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No analyses saved yet. Open Message Scanner to begin.")

# =========================================================
# 9. MESSAGE SCANNER
# =========================================================

elif page == "Message Scanner":
    page_header(
        "MESSAGE ANALYSIS",
        "Message Scanner",
        "Paste a message and inspect the warning signs matched by the rules.",
    )

    st.markdown(
        '<div class="section-title">Input message</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Do not paste real passwords, OTPs, or private financial information.</div>',
        unsafe_allow_html=True,
    )

    with st.form("scanner_form"):
        message = st.text_area(
            "Message to analyze",
            height=190,
            placeholder=(
                "Example: Your account will be blocked. "
                "Share your OTP immediately..."
            ),
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button(
            "✦  Analyze message",
            use_container_width=True,
        )

    if submitted:
        if not message.strip():
            st.warning("Please enter a message before analyzing.")
        elif len(message) > 10000:
            st.warning("Please keep the message under 10,000 characters.")
        else:
            result = analyze_message(message)
            st.session_state["last_analysis"] = {
                "message": message.strip(),
                **result,
            }

    result = st.session_state.get("last_analysis")

    if result:
        st.divider()
        st.markdown(
            '<div class="section-title">Analysis results</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-subtitle">The score is a rule-based indicator, not a fraud probability.</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([0.85, 1.5], gap="large")

        with col1:
            color = risk_color(result["risk_level"])
            st.markdown(
                f"""
                <div class="risk-box">
                    <div style="color:#91a0b7;font-size:12px">
                        HEURISTIC RISK SCORE
                    </div>
                    <div class="risk-number" style="color:{color}">
                        {result["risk_score"]}
                        <span style="font-size:19px;color:#91a0b7">/100</span>
                    </div>
                    <div style="margin-top:12px;color:{color};font-weight:700">
                        {result["risk_level"].upper()} RISK
                    </div>
                    <div class="risk-caption">
                        Based on configured pattern rules
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.progress(result["risk_score"] / 100)

            st.caption(result["explanation"])

        with col2:
            st.markdown("**Why this result?**")

            if result["signals"]:
                for signal in result["signals"]:
                    st.markdown(
                        f'<div class="signal"><span class="signal-dot">✦</span>{signal}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info(
                    "No predefined warning signs matched. "
                    "A low score does not establish that a message is safe."
                )

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("**Message preview**")
        st.code(result["message"], language=None)

        if st.button("Save analysis to MongoDB", use_container_width=True):
            try:
                saved = save_analysis(
                    result["message"],
                    result,
                )
                st.success(
                    f"Analysis saved successfully. Record ID: {saved.inserted_id}"
                )
                st.session_state.pop("last_analysis", None)
                st.rerun()
            except PyMongoError as exc:
                st.error(f"Could not save the analysis: {exc}")

        st.caption(
            "Safety note: Never share an OTP or password in response to "
            "an unverified message. Verify requests through an independently "
            "obtained official channel."
        )

# =========================================================
# 10. ANALYSIS HISTORY — READ, UPDATE, DELETE
# =========================================================

elif page == "Analysis History":
    page_header(
        "RECORD MANAGEMENT",
        "Analysis History",
        "Search saved messages, update review information, or remove records.",
    )

    search_text = st.text_input(
        "Search message text",
        placeholder="Search saved messages...",
    )

    f1, f2 = st.columns(2)
    with f1:
        selected_risk = st.selectbox(
            "Risk category",
            ["All", "High", "Medium", "Low"],
        )
    with f2:
        selected_status = st.selectbox(
            "Review status",
            ["All", "Pending", "Reviewed", "Needs Follow-up"],
        )

    query = {}

    if selected_risk != "All":
        query["risk_level"] = selected_risk

    if selected_status != "All":
        query["review_status"] = selected_status

    if search_text.strip():
        query["message"] = {
            "$regex": re.escape(search_text.strip()),
            "$options": "i",
        }

    records = list(
        analyses.find(query).sort("analyzed_at", -1).limit(500)
    )

    st.caption(f"{len(records)} matching record(s), up to 500 displayed")

    if records:
        rows = []
        for r in records:
            rows.append({
                "ID": str(r["_id"]),
                "Message": r["message"][:90],
                "Risk": r["risk_level"],
                "Score": r["risk_score"],
                "Signals": ", ".join(r.get("signals", [])),
                "Review": r.get("review_status", "Pending"),
                "Date": format_time(r.get("analyzed_at")),
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        st.markdown("### Manage a record")

        record_map = {str(r["_id"]): r for r in records}
        selected_id = st.selectbox(
            "Choose a record",
            list(record_map.keys()),
            format_func=lambda value: (
                f'{record_map[value]["risk_level"]} · '
                f'{record_map[value]["message"][:65]}'
            ),
        )

        selected_record = record_map[selected_id]

        with st.form("update_record_form"):
            new_status = st.selectbox(
                "Review status",
                ["Pending", "Reviewed", "Needs Follow-up"],
                index=[
                    "Pending", "Reviewed", "Needs Follow-up"
                ].index(
                    selected_record.get("review_status", "Pending")
                ),
            )
            new_note = st.text_area(
                "Analyst note",
                value=selected_record.get("analyst_note", ""),
                max_chars=1000,
            )
            update_clicked = st.form_submit_button(
                "Update review details"
            )

        if update_clicked:
            try:
                update_review(selected_id, new_status, new_note)
                st.success("Review details updated.")
                st.rerun()
            except (PyMongoError, ValueError) as exc:
                st.error(f"Update failed: {exc}")

        with st.expander("Delete selected record"):
            st.warning(
                "Deleting a record permanently removes that document "
                "from this collection."
            )
            confirm_delete = st.checkbox(
                "I confirm that I want to delete this record."
            )

            if st.button("Delete selected record", type="secondary"):
                if not confirm_delete:
                    st.warning("Please confirm deletion first.")
                else:
                    try:
                        delete_result = delete_analysis(selected_id)
                        if delete_result.deleted_count:
                            st.success("Record deleted.")
                            st.rerun()
                        else:
                            st.warning("The record was not found.")
                    except (PyMongoError, ValueError) as exc:
                        st.error(f"Delete failed: {exc}")

    else:
        st.info("No records match these filters.")

# =========================================================
# 11. PATTERN EXPLORER — AGGREGATION
# =========================================================

elif page == "Pattern Explorer":
    page_header(
        "MONGODB ANALYTICS",
        "Pattern Explorer",
        "Explore recurring warning signs across saved analysis documents.",
    )

    total = analyses.count_documents({})
    st.caption(f"Analysis collection contains {total} saved record(s).")

    if total == 0:
        st.info(
            "No saved records yet. Scan and save messages or load "
            "fictional demonstration data from the Overview page."
        )
    else:
        left, right = st.columns(2, gap="large")

        with left:
            st.markdown(
                '<div class="section-title">Risk category summary</div>',
                unsafe_allow_html=True,
            )

            risk_summary = get_risk_summary()

            if risk_summary:
                risk_df = pd.DataFrame([
                    {
                        "Risk level": item["_id"],
                        "Count": item["total"],
                        "Average score": round(item["average_score"], 1),
                    }
                    for item in risk_summary
                ])

                st.dataframe(
                    risk_df,
                    use_container_width=True,
                    hide_index=True,
                )

                st.bar_chart(
                    risk_df.set_index("Risk level")[["Count"]],
                    use_container_width=True,
                )

        with right:
            st.markdown(
                '<div class="section-title">Recurring warning signs</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="section-subtitle">Top signals counted with $unwind and $group</div>',
                unsafe_allow_html=True,
            )

            signal_summary = get_signal_summary()

            if signal_summary:
                signal_df = pd.DataFrame([
                    {
                        "Warning sign": item["_id"],
                        "Occurrences": item["total"],
                    }
                    for item in signal_summary
                ])

                st.dataframe(
                    signal_df,
                    use_container_width=True,
                    hide_index=True,
                )

                st.bar_chart(
                    signal_df.set_index("Warning sign"),
                    use_container_width=True,
                )
            else:
                st.info("No warning signs have been saved yet.")

        st.divider()
        st.markdown("### MongoDB aggregation pipeline")

        st.code(
            '''db.analyses.aggregate([
  { "$unwind": "$signals" },
  {
    "$group": {
      "_id": "$signals",
      "total": { "$sum": 1 }
    }
  },
  { "$sort": { "total": -1 } },
  { "$limit": 10 }
])''',
            language="javascript",
        )

        st.caption(
            "These counts describe the records saved in this database. "
            "They do not estimate scam prevalence across all messages."
        )

# =========================================================
# 12. ABOUT PAGE
# =========================================================

elif page == "About ScamLens":
    page_header(
        "PROJECT INFORMATION",
        "About ScamLens",
        "An explainable, database-backed suspicious message pattern explorer.",
    )

    st.markdown(
        """
        <div class="hero">
            <div class="hero-chip">PYTHON · STREAMLIT · MONGODB</div>
            <h1>Understand the signals.<br/>Not just the score.</h1>
            <p>
                ScamLens examines user-provided message text using
                predefined rules, explains the matched warning signs,
                and stores analyses for historical review and pattern
                exploration.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown("### What the system does")
        st.markdown(
            """
            - Detects selected suspicious text patterns.
            - Calculates a configurable heuristic risk score.
            - Explains the matched rules.
            - Stores and retrieves analyses using PyMongo.
            - Uses MongoDB aggregation to summarize saved patterns.
            - Supports review-status updates and record deletion.
            """
        )

    with c2:
        st.markdown("### What the system does not do")
        st.markdown(
            """
            - It does not guarantee scam detection.
            - It does not calculate a verified fraud probability.
            - It does not use a trained ML model in this version.
            - It does not automatically verify a URL or its owner.
            - It does not replace official security or fraud-reporting tools.
            """
        )

    st.info(
        "Use fictional or sanitized examples for demonstrations. "
        "Do not store real OTPs, passwords, or unnecessary private information."
    )

# =========================================================
# 13. FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        SCAMLENS · EXPLAINABLE MESSAGE PATTERN ANALYSIS<br/>
        A rule-based educational project powered by MongoDB.
    </div>
    """,
    unsafe_allow_html=True,
)
