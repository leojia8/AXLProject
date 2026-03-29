# 🎯 Family Feud AI

An AI-powered Family Feud web game that combines real crowd-sourced survey data with AI-generated boards and smart semantic answer matching.

Built for the AXL take-home assessment.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- A Google Gemini API key ([get one free](https://aistudio.google.com/apikey))

### Setup

```bash
# Clone the repo
git clone <repo-url>
cd AXLProject

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the app
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) to play.

## 🎮 How It Works

1. **Start a round** — A survey-style prompt appears: *"Name something students do right before an exam"*
2. **Type guesses** — Enter your best guesses for the top answers
3. **Smart matching** — AI understands that "phone" matches "check their phone"
4. **Score points** — Uncover the board before you run out of strikes
5. **Play again** — Get a new board from real data, AI, or trending topics

## 🤖 AI Features

| Feature | Description |
|---------|-------------|
| **Semantic Matching** | LLM judges whether your guess matches a board answer, allowing synonyms and shorthand |
| **Board Generation** | When real boards run out, AI generates realistic survey-style boards |
| **Trend-Based Boards** | Current trending topics seed dynamic board creation |
| **Source Transparency** | Each board shows whether it came from real data, AI, or hybrid sources |

## 📁 Project Structure

```
AXLProject/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py             # Centralized configuration
│   ├── routes/
│   │   ├── pages.py          # HTML page routes (/, /play)
│   │   └── api.py            # JSON API routes (/api/*)
│   ├── services/
│   │   ├── ai_service.py     # LLM integration (Gemini)
│   │   ├── board_service.py  # Board selection & generation
│   │   ├── matching_service.py # Layered guess matching
│   │   ├── game_service.py   # Round lifecycle management
│   │   └── cache_service.py  # Generated board caching
│   ├── models/
│   │   └── schemas.py        # Pydantic request/response models
│   ├── templates/            # Jinja2 HTML templates
│   └── static/               # CSS & JavaScript
├── data/
│   ├── real_boards.json      # 25 curated real-inspired boards
│   ├── trending_topics.json  # 20 trending topic seeds
│   └── generated_boards_cache.json
├── requirements.txt
├── Procfile                  # Render deployment
└── render.yaml               # Render blueprint
```

## 🏗️ Architecture

```
User Guess → Normalize → Exact Match → Containment → Fuzzy Match → LLM Semantic Match
                                                                         ↓
Board Request → Real JSON → Cached AI → Trend-Seeded AI → Pure AI Generation
```

## 🔧 Tech Stack

- **Backend:** FastAPI + Python
- **Frontend:** Vanilla JS + Jinja2 templates
- **AI:** Google Gemini API
- **Matching:** rapidfuzz + LLM semantic fallback
- **Deployment:** Render

## 📝 License

MIT