# AI Document Intelligence Engine

AI-powered document processing system for extracting insights, summaries, and structured data from PDF, DOCX, and text documents.

---

## 🚀 Features

- 📄 PDF / DOCX / TXT support
- 🧠 AI-powered summarization
- 🔑 Key points extraction
- 🧾 Keyword detection
- 📊 Structured insights (word count, complexity)
- 🔄 Fallback engine (no API required)
- ⚡ FastAPI backend (production-ready)

---

## 🧠 Architecture

User → FastAPI → Document Extractor → AI Processor → Structured Output

---

## 📦 API Endpoint

### Upload Document

```http
POST /upload-document