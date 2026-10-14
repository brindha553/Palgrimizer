# Palgrimizer AI - Enterprise Document Correction Platform

## Overview
Palgrimizer is a premium AI-powered document correction SaaS application built with Python Flask, SQLite, and a custom modern glassmorphism UI design system.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```

Access at: **http://127.0.0.1:5000**

## Project Structure
```
Palgrimizer_mca1/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── models/              # SQLAlchemy models (User, Document, Report, Correction)
│   ├── services/            # AI NLP Engine, Doc Parser, Exporter, OCR, AI Chat
│   ├── routes/              # Flask Blueprints (auth, dashboard, document, history, api)
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JavaScript, assets
├── uploads/                 # Uploaded document storage
├── instance/                # SQLite database (auto-created)
├── run.py                   # Entry point
└── requirements.txt
```

## Key Features
- **14+ AI Detection Categories**: Grammar, Spelling, Punctuation, Alignment, Typography, Readability, Passive Voice, Duplicate Content, etc.
- **Interactive Correction Studio**: Side-by-Side & Inline Diff views with Accept/Reject individual suggestions
- **Multi-format Support**: PDF, DOCX, TXT, RTF upload and export
- **OCR Image Scanning**: Extract text from PNG/JPG images
- **Voice Dictation**: Web Speech API integration
- **AI Assistant**: Floating chat drawer with contextual prompts
- **Dark/Light Theme**: Auto-detection + manual toggle
- **Dashboard**: Stats, activity timeline, analytics charts

## Default Test Credentials
Register any new account on the Register page — a sample welcome document is auto-created.
