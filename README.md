# 🎓 ANITS Campus Info Chatbot

An AI-powered campus information assistant built for **Anil Neerukonda Institute of Technology and Sciences (ANITS), Visakhapatnam**.

The chatbot provides instant, intelligent, and accurate answers related to:

* Departments
* Placements
* Faculty contacts
* Clubs & events
* Campus facilities
* Academic procedures
* Student services

Built using **RAG (Retrieval-Augmented Generation)** architecture with semantic search, vector embeddings, and LLM-powered responses.

---

## 🚀 Live Demo

| Service             | URL                                                                              |
| ------------------- | -------------------------------------------------------------------------------- |
| Frontend            | https://campusinfo.vercel.app                                               |
| Backend API         | https://anits-campus-api-fvfaghdxgrdvd4ae.centralindia-01.azurewebsites.net      |
| API Docs            | https://anits-campus-api-fvfaghdxgrdvd4ae.centralindia-01.azurewebsites.net/docs |
| Analytics Dashboard | https://campusinfo.vercel.app/analytics                                     |

---

## 🛠️ Tech Stack

| Layer        | Technology                        |
| ------------ | --------------------------------- |
| Frontend     | Next.js 14 + React + Tailwind CSS |
| Backend      | FastAPI + Uvicorn                 |
| Database     | MongoDB Atlas                     |
| AI Framework | LangChain LCEL                    |
| Vector Store | FAISS                             |
| Embeddings   | HuggingFace all-MiniLM-L6-v2      |
| LLM          | Groq Llama 3.3 70B                |
| Scraping     | BeautifulSoup4                    |
| Deployment   | Azure App Service + Vercel        |

---

# ✨ Features

## ✅ Core Features

* Multi-source knowledge base (PDF + CSV + JSON + Web)
* Semantic search using FAISS vector database
* AI-powered responses using Groq Llama 3.3 70B
* Category-based intelligent filtering
* Persistent chat history using MongoDB
* FastAPI REST API architecture

---

## 🚀 Advanced Features

* Personalized greetings based on user history
* Intelligent recommendation engine
* Predictive suggestions using academic calendar
* Background scheduler for automated scraping
* Content freshness monitoring
* Response caching system
* API rate limiting for security
* Analytics dashboard with usage insights
* Export chat history functionality

---

# 🏗️ System Architecture

```text
Student Question
        ↓
Next.js Frontend (Vercel)
        ↓
FastAPI Backend (Azure)
        ↓
Category Detection & Query Filtering
        ↓
FAISS Semantic Search
        ↓
HuggingFace Embeddings
        ↓
Groq Llama 3.3 70B
        ↓
MongoDB Atlas (History Storage)
        ↓
AI Response to User
```

---

# 📂 Project Structure

```text
campusinfo/
│
├── src/                          # AI Core
│   ├── agent.py
│   ├── vector_store.py
│   ├── scraper.py
│   ├── ingest.py
│   ├── freshness.py
│   ├── recommendations.py
│   ├── analytics.py
│   ├── personalization.py
│   ├── scheduler.py
│   └── cache.py
│
├── backend/                      # FastAPI Backend
│   ├── main.py
│   ├── routes/
│   └── models/
│
├── frontend/                     # Next.js Frontend
│   └── app/
│       ├── components/
│       └── analytics/
│
├── data/                         # Knowledge Base
│   ├── contacts/
│   ├── events/
│   ├── locations/
│   ├── academic_calendar/
│   ├── procedures/
│   ├── clubs/
│   ├── scraped/
│   └── vector_store/
│
└── requirements.txt
```

---

# ⚙️ Local Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/SaiSandeep10/campusinfo.git
cd campusinfo
```

---

## 2️⃣ Create Python Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
MONGODB_URL=your_mongodb_connection_string
```

---

## 4️⃣ Build Knowledge Base

```bash
python src/scraper.py
python src/ingest.py
python src/vector_store.py
```

---

## 5️⃣ Run Backend Server

```bash
uvicorn backend.main:app --reload --port 8000
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

## 6️⃣ Setup Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env.local`

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Run frontend:

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:3000
```

---

# 📡 API Endpoints

| Method | Endpoint                           | Description               |
| ------ | ---------------------------------- | ------------------------- |
| GET    | `/`                                | Health Check              |
| GET    | `/health`                          | Agent Status              |
| POST   | `/api/ask`                         | Basic Chat                |
| POST   | `/api/search`                      | Advanced Search           |
| GET    | `/api/history`                     | Chat History              |
| GET    | `/api/categories`                  | Categories List           |
| GET    | `/api/freshness`                   | Content Freshness         |
| GET    | `/api/analytics`                   | Usage Analytics           |
| GET    | `/api/personalization/greeting`    | Personalized Greeting     |
| GET    | `/api/personalization/predictions` | Predictive Suggestions    |
| GET    | `/api/cache/stats`                 | Cache Statistics          |
| GET    | `/docs`                            | Swagger API Documentation |

---

# 📊 Data Sources

| Source             | Format       | Content                             |
| ------------------ | ------------ | ----------------------------------- |
| ANITS Website      | Web Scraping | Departments, placements, facilities |
| College Handbook   | PDF          | Regulations & policies              |
| Faculty Directory  | CSV          | Staff contacts                      |
| Events Database    | CSV          | Campus events                       |
| Campus Map         | JSON         | Locations & directions              |
| Academic Calendar  | CSV          | Semester schedules                  |
| Student Procedures | CSV          | Administrative procedures           |
| Clubs Database     | CSV          | Student clubs & societies           |

---

# ☁️ Deployment

## Backend Deployment — Azure App Service

### Environment Variables

```env
GROQ_API_KEY=your_key
MONGODB_URL=your_mongodb_url
PYTHONPATH=/home/site/wwwroot
```

### Startup Command

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

---

## Frontend Deployment — Vercel

### Environment Variable

```env
NEXT_PUBLIC_API_URL=https://your-azure-url.azurewebsites.net
```

### Configuration

```text
Framework Preset : Next.js
Root Directory   : frontend
```

---

# 📈 Performance Metrics

| Metric                | Value               |
| --------------------- | ------------------- |
| Vector Chunks         | 308                 |
| Knowledge Base Size   | 129,000+ characters |
| Cache TTL             | 60 minutes          |
| Rate Limit            | 30 requests/minute  |
| Average Response Time | 2–4 seconds         |
| Supported Categories  | 6                   |

---

# 👥 Team

| Name          | Role                            |
| ------------- | ------------------------------- |
| Sai Sandeep   | Team Lead, Frontend, Deployment |
| Sai Dinesh    | Data Processing, PDF Ingestion  |
| Niranjan Raju | Web Scraping, Student Services  |
| Chethris      | MongoDB, Search Routes          |

### Institution

**ANITS — Anil Neerukonda Institute of Technology and Sciences**

### Project Duration

**8 Weeks**

### Track

**Track B (Advanced)**

---

# 🎓 Learning Outcomes

* Retrieval-Augmented Generation (RAG)
* Semantic Search Systems
* Vector Databases with FAISS
* Full Stack Development
* FastAPI Backend Development
* MongoDB Integration
* Cloud Deployment using Azure & Vercel
* AI Personalization & Analytics
* Automated Data Pipelines

---

# 📝 License

This project was developed for educational purposes as part of the **AI Agent Development Course at ANITS**.

---

# ❤️ Acknowledgements

Special thanks to:

* ANITS Faculty & Mentors
* Groq
* HuggingFace
* LangChain
* FastAPI Community
* Open Source Contributors

---

<div align="center">

### ⭐ Built with passion by Team ANITS Campus Assistant ⭐

</div>
