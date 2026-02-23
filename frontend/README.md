# TrustCheck AI

**AI-Powered Multi-Layer Cybersecurity Threat Detection Engine**

TrustCheck AI is an enterprise-grade, AI-assisted cybersecurity intelligence system that analyzes suspicious content across text, URLs, images, and files in real time. It combines rule-based threat detection, heuristic analysis, OCR scanning, deepfake detection, and URL intelligence into a unified risk scoring engine.

## Core Features

### 1. Text Threat Detection
- Phishing detection
- Brand impersonation detection
- Urgency manipulation detection
- OTP/password scam detection
- UPI / payment fraud detection
- Cryptocurrency scam patterns
- Social engineering pattern analysis

### 2. URL Intelligence Engine
- Suspicious domain detection
- Typosquatting detection
- Reverse DNS validation
- Brand impersonation domain matching
- Malicious pattern analysis
- TLD anomaly detection

### 3. Image Security Analysis
- SHA256 file hashing
- VirusTotal hash lookup (optional API)
- OCR text extraction (Tesseract)
- Financial keyword detection inside images
- AI-generated deepfake detection (ResNet-based)
- Face artifact blur detection
- Unified image risk scoring

### 4. OCR-Based Scam Detection
Extracts text from uploaded screenshots and detects:
- OTP codes
- Payment instructions
- Urgency patterns
- Financial manipulation signals

### 5. AI-Generated Image Detection
- Pretrained ResNet18 model
- Probability-based synthetic image scoring
- Escalation logic for high AI confidence
- Integrated with unified risk engine

### 6. Security Middleware Layer
- API Key protection
- Rate limiting
- Secure HTTP headers
- CORS control
- Global exception handling
- Content Security Policy enforcement

## Risk Scoring System

All signals are merged into a weighted threat scoring model.

### Risk Levels

| Score Range | Risk Level |
|---|---|
| ≥ 80 | HIGH |
| 45–79 | MEDIUM |
| < 45 | LOW |

Each scan returns:
- Risk Level
- Numerical Score
- Confidence %
- Category
- Explanation
- Detected Indicators
- Safety Recommendations

## Backend Architecture

The backend is modular and layered:

backend/
│
├── app/
│   ├── routes/
│   │   ├── unified_scan.py
│   │   └── url_scan.py
│   │
│   ├── services/
│   │   ├── action_intent_detector.py
│   │   ├── app_checker.py
│   │   ├── attack_pattern_detector.py
│   │   ├── auth_service.py
│   │   ├── background_tasks.py
│   │   ├── behaviour_engine.py
│   │   ├── brand_impersonation.py
│   │   ├── cache.py
│   │   ├── cors_checker.py
│   │   ├── domain_intelligence.py
│   │   ├── explanation_engine.py
│   │   ├── file_scanner.py
│   │   ├── greeting_filter.py
│   │   ├── image_engine.py
│   │   ├── image_scanner.py
│   │   ├── image_security_engine.py
│   │   ├── intent_classifier.py
│   │   ├── ollama_service.py
│   │   ├── payment_detector.py
│   │   ├── phishing_detector.py
│   │   ├── qr_scanner.py
│   │   ├── response_formatter.py
│   │   ├── scam_detector.py
│   │   ├── security_logger.py
│   │   ├── telemetry.py
│   │   ├── typosquat_detector.py
│   │   ├── url_analyzer.py
│   │   ├── url_trust_engine.py
│   │   └── xss_detector.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   └── __init__.py
│   │
│   ├── config.py
│   └── main.py
│
├── requirements.txt
└── run.py
## Unified Scan API

**Endpoint:** `POST /api/scan`

**Request Body:**
```json
{
  "message": "optional text message",
  "image_base64": "optional base64 image",
  "history": []
}
```

**Response Example:**
```json
{
  "risk": "HIGH",
  "score": 90,
  "confidence": 88,
  "category": "Threat Detection",
  "explanation": "Brand impersonation attempt detected.",
  "signals": {
    "rule_hits": ["verify", "otp"],
    "url_signals": ["http://fake-sbi-login.com"]
  },
  "tips": [
    "Do not share OTP.",
    "Verify links independently."
  ]
}
```
## Security Design

TrustCheck AI follows a secure backend architecture:

- Stateless processing (no behavioral memory)
- API Key enforcement
- Rate limiting middleware
- CSP headers
- XSS protection
- Structured error handling
- Modular service isolation
- Input validation with Pydantic

## Technologies Used

**Backend:**
- FastAPI
- Python
- Pydantic
- PyTesseract
- OpenCV
- Torch / TorchVision
- Requests

**AI & Machine Learning:**
- ResNet18 pretrained model
- Heuristic scoring engine
- Rule-based phishing detection

## Performance

- Text scan: < 2 seconds
- Image scan: < 5 seconds
- Fully stateless
- No database dependency
- Lightweight API architecture

## Use Cases

- Banking fraud detection
- Scam message verification
- Screenshot scam detection
- Deepfake detection
- URL phishing analysis
- Educational cybersecurity assistant

## Running the Backend

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run server:**
```bash
python -m uvicorn app.main:app --reload
```

3. **Access API:**
```
http://127.0.0.1:8000/docs
```
## Design Philosophy

TrustCheck AI is built as a stateless, modular, AI-powered cybersecurity threat intelligence engine.

It prioritizes:
- Security
- Performance
- Modularity
- Clean architecture
- Production readiness

## Project Strengths

- Multi-layer detection (Text + URL + Image)
- AI-assisted deepfake detection
- OCR-based screenshot scanning
- Secure middleware architecture
- Modular, extensible backend
- Clean unified API design

## Future Enhancements

- DNS reputation scoring
- Domain age lookup
- Real deepfake CNN training
- JWT authentication
- Redis caching
- Cloud deployment
- Threat intelligence API integration