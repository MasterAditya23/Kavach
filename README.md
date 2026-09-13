# KAVACH — Multi-Vector Fraud Detection Platform

Kavach is a web-based cybersecurity platform designed to detect suspicious digital-fraud indicators before a user interacts with potentially dangerous content.

The MVP analyzes three common digital-fraud attack vectors:

- QR codes
- APK files
- Suspicious messages and call transcripts

Kavach combines technical evidence, rule-based analysis, Gemini AI reasoning, and a risk engine to produce an explainable security result.

> **Three attack vectors. One shield.**

---

## Project Overview

Digital scams increasingly use QR codes, malicious or suspicious mobile applications, and social-engineering messages to trick users into taking harmful actions.

Kavach follows a **pre-interaction protection** approach: instead of waiting for a user to open a suspicious link, install an application, or respond to a scam message, the platform analyzes the content first and provides a risk assessment.

The system follows this general flow:

```text
User Input
    ↓
Kavach Web App
    ↓
Technical / Rule-Based Analysis
    ↓
Evidence Extraction
    ↓
Gemini AI Reasoning
    ↓
Risk Engine
    ↓
Structured Security Result

---

## Features

### 1. QR Scanner

Users can upload a QR-code image.

Kavach:

1. Decodes the QR code using a real QR decoder.
2. Extracts the encoded URL or data.
3. Performs basic technical URL checks.
4. Uses Gemini AI for classification and explanation when available.
5. Returns a structured security result.

The QR scanner checks indicators such as:

- HTTP instead of HTTPS
- IP-address-based URLs
- Punycode domains
- Excessive subdomains
- Other basic URL anomalies

Gemini is used for reasoning and explanation, not for decoding the QR image.

### 2. APK Scanner

Users can upload a suspicious APK without installing it.

Kavach extracts:

- Package name
- Android permissions
- Rule-based permission findings

The system checks for potentially sensitive permissions such as:

- SMS access
- Call-log access
- Contacts access
- Microphone access
- Camera access
- Overlay permissions
- Package-installation permissions

Gemini can explain the technical evidence and classify the potential risk.

The MVP focuses on manifest and permission analysis. It is not a full antivirus or reverse-engineering system.

### 3. Chat / Transcript Scanner

Users can paste:

- SMS messages
- WhatsApp messages
- Suspicious text
- Call transcripts

Kavach analyzes the content for social-engineering indicators such as:

- Authority impersonation
- Urgency and pressure
- Fear or threats
- Payment requests
- Fake KYC or bank claims
- Suspicious links
- OTP requests
- Requests for passwords, PINs, or sensitive information

The scanner returns:

- Risk level
- Scam category
- Key findings
- Explanation
- Recommended action

---

## Technologies Used

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Pydantic

### Security and Analysis

- OpenCV QRCodeDetector
- Python URL parsing
- Androguard
- Rule-based security checks

### AI

- Google Gemini API

### Development

- Git
- GitHub
- VS Code

---

## AI Tools and Models

### Google Gemini

Kavach uses the Google Gemini API for AI-based reasoning and explanation.

Gemini is used after technical evidence has been extracted.

Its purpose includes:

- Classifying suspicious content
- Explaining detected indicators
- Identifying social-engineering tactics
- Interpreting APK permission evidence
- Providing human-readable recommendations

Kavach does not simply send raw input to an AI model and ask it to invent a risk score.

The intended architecture is:

```text
Input
  ↓
Technical Analysis / Rules
  ↓
Evidence
  ↓
Gemini AI
  ↓
Structured Result
  ↓
Risk Engine