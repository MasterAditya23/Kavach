from androguard.core.apk import APK
from services.gemini import ask_gemini
import json

SUSPICIOUS_PERMISSIONS = {
    "android.permission.READ_SMS": "Can read SMS messages",
    "android.permission.RECEIVE_SMS": "Can receive SMS messages",
    "android.permission.SEND_SMS": "Can send SMS messages",
    "android.permission.READ_CALL_LOG": "Can read call history",
    "android.permission.WRITE_CALL_LOG": "Can modify call history",
    "android.permission.READ_CONTACTS": "Can read contacts",
    "android.permission.RECORD_AUDIO": "Can record audio",
    "android.permission.CAMERA": "Can access the camera",
    "android.permission.SYSTEM_ALERT_WINDOW": "Can display overlays over other apps",
    "android.permission.REQUEST_INSTALL_PACKAGES": "Can request installation of other packages",
}


def analyze_apk(apk_path):
    apk = APK(apk_path)

    package_name = apk.get_package()
    permissions = apk.get_permissions()

    findings = []

    for permission in permissions:
        if permission in SUSPICIOUS_PERMISSIONS:
            findings.append(SUSPICIOUS_PERMISSIONS[permission])

    if not findings:
        findings.append("No high-risk permissions detected by the current rules")

    prompt = f"""
You are the APK Scanner of Kavach, a cybersecurity and fraud detection platform.

Analyze the APK using ONLY the technical evidence provided below.

Package name:
{package_name}

Permissions:
{permissions}

Rule-based findings:
{findings}

Return ONLY valid JSON using exactly this structure:

{{
    "risk_level": "Low | Medium | High",
    "category": "string",
    "key_findings": ["string", "string", "string"],
    "explanation": "string",
    "recommended_action": "string"
}}

Do not use Markdown.
Do not invent technical facts that are not supported by the evidence.
Do not claim that the APK is definitely malicious based only on permissions.
"""

    try:
        result = ask_gemini(prompt)
        analysis = json.loads(result)

    except Exception:
        analysis = {
            "risk_level": "Medium",
            "category": "APK Requires Review",
            "key_findings": findings,
            "explanation": (
                "The APK manifest and permissions were successfully extracted "
                "and technically analyzed, but AI analysis is temporarily unavailable."
            ),
            "recommended_action": (
                "Do not install the APK until it has been verified from a trusted source."
            ),
        }

    return {
        "package_name": package_name,
        "permissions": permissions,
        "findings": findings,
        "analysis": analysis,
    }