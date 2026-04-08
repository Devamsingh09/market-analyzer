## `README.md`

````markdown
# 🇮🇳 India Market Analyzer

A FastAPI-based service that analyzes Indian market sectors and returns structured trade opportunity reports powered by Groq's Llama 3.3 AI model.

---

## 📌 Features

- 🔐 JWT Guest Authentication — no signup needed, just hit `/auth/guest`
- ⚡ Async FastAPI with proper error handling
- 🤖 AI-powered analysis via Groq (Llama 3.3 70B Versatile)
- 🔍 DuckDuckGo search + web scraping for live market data
- 🧠 In-memory caching (30 min TTL) — same sector won't hit API twice
- 🚦 Sliding window rate limiting — 5 requests per minute per user
- 📄 Clean markdown reports with 6 structured sections
- 📚 Auto-generated API docs via Swagger UI

---

## 🏗️ Project Structure

```
market-analyzer/
│
├── main.py                  # FastAPI app — all routes live here
├── config.py                # Central config and environment variables
├── requirements.txt         # All dependencies
├── README.md
├── .env                     # API keys (not committed to git)
├── .gitignore
│
├── auth/
│   ├── __init__.py
│   └── jwt_handler.py       # Guest token generation and verification
│
├── middleware/
│   ├── __init__.py
│   └── rate_limiter.py      # Sliding window rate limiter
│
├── services/
│   ├── __init__.py
│   ├── scraper.py           # DuckDuckGo search + web scraping
│   ├── analyzer.py          # Groq LLM integration
│   └── report_builder.py    # Markdown report formatter
│
└── models/
    ├── __init__.py
    └── schemas.py           # Pydantic request/response models
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/market-analyzer.git
cd market-analyzer
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Create a `.env` file in the root folder with the following:

```
GROQ_API_KEY=your_groq_api_key_here
JWT_SECRET_KEY=any_random_secret_string_here
```

Getting your Groq API key:
- Go to [console.groq.com](https://console.groq.com)
- Sign up for free
- Navigate to API Keys → Create new key
- Paste it in `.env`

### 5. Run the server

```bash
uvicorn main:app --reload
```

Server will start at: `http://localhost:8000`

---

## 🚀 Usage

### Step 1 — Get a Guest Token

```
POST /auth/guest
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": "24 hours"
}
```

### Step 2 — Analyze a Sector

```
GET /analyze/{sector}
Authorization: Bearer <your_token>
```

Example:
```
GET /analyze/pharmaceuticals
GET /analyze/technology
GET /analyze/agriculture
GET /analyze/automobile
GET /analyze/banking
```

Response: A structured markdown report saved/displayed with these sections:

```
1. Sector Overview
2. Current Market Conditions
3. Key Players & Companies
4. Trade Opportunities
5. Risks & Challenges
6. Short-Term Outlook (Next 6 Months)
```

---

## 📡 API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/health` | ❌ | Check if server is running |
| `POST` | `/auth/guest` | ❌ | Get a guest JWT token |
| `GET` | `/analyze/{sector}` | ✅ | Get market analysis report |
| `GET` | `/docs` | ❌ | Swagger UI — interactive API docs |

---

## 🔐 Security

| Feature | Implementation |
|--------|----------------|
| Authentication | JWT Bearer tokens (24hr expiry) |
| Rate Limiting | Sliding window — 5 requests/minute per user |
| Input Validation | Regex pattern — only letters, spaces, hyphens (2-50 chars) |
| API Key Safety | Stored in `.env`, never hardcoded |
| Error Masking | Internal errors logged, generic messages returned to user |

---

## 🧠 How It Works

```
Request comes in
      ↓
JWT token verified
      ↓
Rate limit checked (sliding window)
      ↓
Input validated (sector name)
      ↓
Cache checked → Hit? Return instantly
      ↓
DuckDuckGo search → top 5 results
      ↓
Scrape page content (async)
      ↓
Feed data to Groq Llama 3.3
      ↓
Format into markdown report
      ↓
Cache for 30 minutes
      ↓
Return report ✅
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | FastAPI |
| AI Model | Groq — Llama 3.3 70B Versatile |
| Web Search | DuckDuckGo Search API |
| Scraping | httpx + BeautifulSoup4 |
| Auth | python-jose (JWT) |
| Validation | Pydantic v2 |
| Server | Uvicorn (ASGI) |
| Storage | In-memory (Python dict) |

---

## ⚠️ Notes

- DuckDuckGo may rate limit occasionally — the system falls back to Groq's training knowledge automatically in that case
- Reports are cached for 30 minutes — same sector request within that window returns instantly
- This is for informational purposes only, not financial advice

---

## 📄 License

MIT License — free to use and modify.
````

---
