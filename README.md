# 🤖 Resume Analyzer API

[![Python Version](https://img.shields.io/badge/python-3.10-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional AI-powered resume analysis API built with **FastAPI** and **Groq LLM**.

## ✨ Features

- 📄 **Resume Analysis** - Analyze text resumes (Persian & English)
- 📎 **File Upload** - Upload PDF and DOCX files
- 🎯 **Match Score** - Calculate how well a resume matches a job
- 🔍 **Missing Skills** - Identify skills that need improvement
- 📊 **Career Level Detection** - Junior, Mid, Senior, Lead
- 📚 **Full Swagger Documentation** - Interactive API documentation
- ✅ **Input Validation** - Robust validation with clear error messages
- 📝 **Comprehensive Logging** - Track all API activities
- 🌐 **CORS Ready** - Ready for frontend integration

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | API Framework |
| Groq | AI/LLM Inference |
| Pydantic | Data Validation |
| Uvicorn | ASGI Server |
| Python-Multipart | File Upload Handling |

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/mohammad3599/resume-analyzer-clean.git
cd resume-analyzer-clean

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py