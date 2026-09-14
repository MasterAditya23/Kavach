from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from models.analysis import AnalysisRequest
from services.gemini import ask_gemini
from services.qr_service import decode_qr
from services.url_service import analyze_url
from services.apk_service import analyze_apk
import json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://kavach-pi-seven.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Kavach API is running"}


@app.post("/api/analyze/chat")
def analyze_chat(request: AnalysisRequest):
    prompt = f"""
You are the Chat Scanner of Kavach, a cybersecurity and fraud detection platform.

Analyze the following SMS, WhatsApp message, or call transcript for
digital fraud and social-engineering indicators.

Look for indicators such as:
- Authority impersonation
- Urgency or pressure
- Fear or threats
- Payment requests
- Fake KYC or bank claims
- Suspicious links or requests
- Requests for OTP, PIN, passwords, or sensitive information
- Other scam or social-engineering tactics

Message:
{request.message}

Return ONLY valid JSON using exactly this structure:

{{
    "risk_level": "Low | Medium | High",
    "category": "string",
    "key_findings": ["string", "string", "string"],
    "explanation": "string",
    "recommended_action": "string"
}}

Do not use Markdown.
Do not invent facts that are not supported by the message.
"""

    try:
        result = ask_gemini(prompt)
        analysis = json.loads(result)

    except Exception:
        message_lower = request.message.lower()

        fallback_findings = []

        if "urgent" in message_lower or "immediately" in message_lower:
            fallback_findings.append(
                "Uses urgency or pressure to encourage immediate action"
            )

        if "otp" in message_lower:
            fallback_findings.append(
                "Requests or references an OTP, which is sensitive information"
            )

        if "kyc" in message_lower:
            fallback_findings.append(
                "Uses a KYC or account-verification claim"
            )

        if "bank" in message_lower or "account" in message_lower:
            fallback_findings.append(
                "Uses a banking or account-related claim"
            )

        if "blocked" in message_lower or "block" in message_lower:
            fallback_findings.append(
                "Uses a threat or fear of account blockage"
            )

        if not fallback_findings:
            fallback_findings.append(
                "AI analysis is temporarily unavailable; manual verification is recommended"
            )

        analysis = {
            "risk_level": "Medium",
            "category": "Potential Social Engineering",
            "key_findings": fallback_findings[:3],
            "explanation": (
                "The message was received and checked for basic "
                "social-engineering indicators, but AI analysis is "
                "temporarily unavailable."
            ),
            "recommended_action": (
                "Do not click suspicious links or share OTPs, PINs, "
                "passwords, or other sensitive information until the "
                "message has been independently verified."
            ),
        }

    return {
        "analysis": analysis
    }
@app.post("/api/analyze/qr")
async def analyze_qr(file: UploadFile = File(...)):
    image_bytes = await file.read()

    decoded_data = decode_qr(image_bytes)
    url_analysis = analyze_url(decoded_data)

    prompt = f"""
You are the QR Scanner of Kavach, a cybersecurity and fraud detection platform.

Analyze the decoded QR content using the technical evidence provided below.

Decoded QR data:
{decoded_data}

Technical URL findings:
{url_analysis["findings"]}

Classify the QR content for potential digital fraud.

Return ONLY valid JSON using exactly this structure:

{{
    "risk_level": "Low | Medium | High",
    "category": "string",
    "key_findings": ["string", "string", "string"],
    "explanation": "string",
    "recommended_action": "string"
}}

Do not use Markdown.
Do not invent facts that are not supported by the decoded data or technical findings.
"""

    try:
        result = ask_gemini(prompt)
        analysis = json.loads(result)

    except Exception:
        analysis = {
            "risk_level": "Medium",
            "category": "QR Code Requires Review",
            "key_findings": url_analysis["findings"],
            "explanation": "The QR code was successfully decoded and technically analyzed, but AI analysis is temporarily unavailable.",
            "recommended_action": "Do not open the decoded link until it has been verified."
        }

    return {
        "decoded_data": decoded_data,
        "url_analysis": url_analysis,
        "analysis": analysis
    }

@app.post("/api/analyze/apk")
async def analyze_apk_endpoint(file: UploadFile = File(...)):

    apk_bytes = await file.read()

    with open("uploaded.apk", "wb") as f:
        f.write(apk_bytes)

    result = analyze_apk("uploaded.apk")

    return result