# DocuGPT: AI Chatbot for Document Knowledge Retrieval

## Overview

**DocuGPT** is a **Retrieval-Augmented Generation (RAG) system** that allows users to query multi-format documents (PDF, TXT, CSV, Excel). Documents are split into chunks, embedded using **Sentence-Transformers (`all-MiniLM-L6-v2`)**, stored in a **persistent Chroma vector database**, and answers are generated using **Google Gemini-2.5 LLM** with chat history for context-aware responses.

## Features

* Supports **PDF, TXT, CSV, Excel**
* Splits documents into semantic chunks for efficient retrieval
* Stores embeddings in **Chroma** (persistent vector store)
* Maintains **chat history** for conversational queries
* Provides **FastAPI endpoints** to load documents and query

## Architecture

```
Document → Load → Split → Embeddings → Chroma DB → Query → Retrieve → Build Prompt → Gemini LLM → Response
```

## Technology Stack

* **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Vector DB:** Chroma
* **LLM:** Google Gemini-2.5
* **Backend:** FastAPI
* **File Handling:** PyPDFLoader, TextLoader, CSV/Excel

## Installation & Setup

1. Clone repo:

```bash
git clone <repo-url>
cd DocuGPT
```

2. (Optional) Create virtual env:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add **Google GenAI API key** in `main.py`:

```python
client = Client(api_key="YOUR_API_KEY")
```

## Running FastAPI

```bash
uvicorn main:app --reload
```

Access Swagger UI: `http://127.0.0.1:8000/docs`

## Using APIs in Postman

### 1. Load Documents

* **Endpoint:** `/load` | **Method:** POST
* **Body JSON:**

```json
{
  "path": "https://example.com/sample.pdf"
}
```

* **Response:**

```json
{"message": "Successfully Loaded"}
```

### 2. Ask Query

* **Endpoint:** `/ask` | **Method:** POST
* **Body JSON:**

```json
{
  "query": "What is Retrieval-Augmented Generation?"
}
```

* **Response:**

```json
{
  "response": "Retrieval-Augmented Generation (RAG) is a system that combines..."
}
```

> Retrieves top-k relevant chunks from Chroma, builds prompt with chat history, and generates answer via Gemini LLM.

## Project Structure

```
main.py          # FastAPI + RAG pipeline
requirements.txt # Dependencies
chroma_db/       # Persistent vector store
data/            # Temporary downloads
README.md        # Documentation
```

## Results

* Multi-format documents ingested successfully
* **Top-3 relevant chunks retrieved in <0.5s**
* **Context-aware, coherent answers** generated via LLM
* Scalable, offline-capable RAG system

## Notes

* Prefer **POST requests** for `/load` and `/ask`
* Async endpoints can improve concurrent performance
* Vector store can be preloaded from `./chroma_db` to save time
* Metadata filtering can be added for advanced queries

## Contact

**Author:** Rishav Kumar
**Email:** [rishavkuma@iitbhilai.ac.in](mailto:rishavkuma@iitbhilai.ac.in)
**Organization:** Indian Institute of Technology, Bhilai
