# 🎓 ANITS Campus Assistant

> An AI-powered chatbot that answers questions about Anil Neerukonda Institute of Technology and Sciences (ANITS), Visakhapatnam.



---

## 📌 What is This?

ANITS Campus Assistant is an AI chatbot that helps students, freshers, and visitors get instant answers about:

- 🏫 Departments and courses
- 🏢 Campus facilities (library, hostel, canteen, labs)
- 💼 Placement cell and internships
- 🎭 Clubs and events
- 📋 Admission procedures
- 📞 Faculty and department contacts

---

## 🚀 Live Demo

👉 **[Click here to try the chatbot](https://campusinfo-b2brexg6m6qgv6q24wj5bf.streamlit.app/)**

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI Model | Groq (Llama 3.3 70B) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Database | FAISS |
| LLM Framework | LangChain LCEL |
| Web Scraping | BeautifulSoup4 |
| PDF Processing | PyPDF |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure

```
campus-chatbot/
├── data/
│   ├── handbooks/          # College PDF handbooks
│   ├── scraped/            # Scraped website content
│   │   ├── website.txt     # ANITS website text
│   │   └── chunks.txt      # PDF text chunks
│   └── vector_store/       # FAISS index files
├── src/
│   ├── ingest.py           # PDF processing
│   ├── scraper.py          # Website scraping
│   ├── vector_store.py     # Embeddings + FAISS
│   ├── agent.py            # LangChain AI agent
│   
├── app.py                  # Streamlit chat interface
├── requirements.txt        # Python dependencies
├── .env                    # API keys (never commit!)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## ⚙️ How It Works

```
College PDF + ANITS Website
          ↓
   ingest.py + scraper.py     ← collect data
          ↓
   vector_store.py            ← store as embeddings in FAISS
          ↓
   agent.py                   ← find relevant chunks + ask Groq AI
          ↓
   app.py                     ← display answer in chat UI
```

---

## 🏃 Setup Instructions

### Prerequisites
- Python 3.11
- Git
- A free Groq API key from [console.groq.com](https://console.groq.com)

---

### Step 1 — Clone the Repository
```bash
git clone https://github.com/SaiSandeep10/campusinfo.git
cd campusinfo
```

### Step 2 — Create Virtual Environment
```bash
py -3.11 -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set Up API Key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key from [console.groq.com](https://console.groq.com)

### Step 5 — Add College Data
Place your college handbook PDF in:
```
data/handbooks/handbook.pdf
```

### Step 6 — Build the Knowledge Base
Run these commands in order:
```bash
python src/ingest.py        # Process PDF
python src/scraper.py       # Scrape website
python src/vector_store.py  # Build FAISS index
```

### Step 7 — Run the App
```bash
streamlit run app.py
```

Open your browser and go to: **http://localhost:8501**

---

## 🌐 Deployment on Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file path: `app.py`
5. Add secret in Settings:
```toml
GROQ_API_KEY = "your_key_here"
```
6. Click **Deploy**!

---

## 👥 Team Members

| Name | Role | Responsible File |
|------|------|-----------------|
| Sampathirao Niranjan Raju | Team Lead  | `src/ingest.py` |
| Sai Dinesh Alugoji | UI | `app.py` |
| Talasu Chethris | Scraper Dev | `src/scraper.py` |
| Sai Sandeep Sadhu | AI Engineer | `src/vector_store.py` + `src/agent.py` |

---

## 📦 Requirements

```
langchain
langchain-community
langchain-text-splitters
langchain-groq
langchain-huggingface
groq
sentence-transformers
faiss-cpu
streamlit
beautifulsoup4
pypdf
pandas
requests
python-dotenv
python-docx
```

---

## ❓ Sample Questions to Ask

- *"What departments are available in ANITS?"*
- *"Where is the placement cell located?"*
- *"What are the library timings?"*
- *"How do I join the coding club?"*
- *"What facilities does ANITS have?"*
- *"How do I apply for a bonafide certificate?"*

---

## ⚠️ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `GROQ_API_KEY not found` | Check your `.env` file exists |
| `Vector store not found` | Run `python src/vector_store.py` first |
| `Git push rejected` | Run `git pull origin main` first |
| App fails on Streamlit Cloud | Add `GROQ_API_KEY` in Streamlit Secrets |



## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [ANITS College](https://www.anits.org) for the campus information
- [Groq](https://groq.com) for free LLM API
- [HuggingFace](https://huggingface.co) for free embeddings
- [LangChain](https://langchain.com) for the AI framework
- [Streamlit](https://streamlit.io) for the web interface

---

*Built with ❤️ *