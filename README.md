# 🚀 DataCenter-RAG  
## AI EPC Project Intelligence Platform

An AI-powered engineering document intelligence platform built using **Retrieval Augmented Generation (RAG)** and **Multi-Agent AI Architecture**.

The platform enables engineers to upload EPC project documents, automatically extract knowledge, store information in a vector database, and interact with specialized AI agents for intelligent project assistance.

---

# 📌 Problem Statement

Large-scale EPC (Engineering, Procurement, and Construction) projects generate massive amounts of unstructured data:

- Engineering documents
- SOPs
- Compliance documents
- Incident reports
- Commissioning procedures
- Project schedules

Finding relevant information manually is time-consuming and inefficient.

**DataCenter-RAG solves this by combining:**

- Large Language Models (LLMs)
- Retrieval Augmented Generation (RAG)
- Vector Databases
- LangGraph Multi-Agent Workflows
- Document Intelligence

---

# ✨ Key Features

## 📄 Intelligent Document Processing

- Upload PDF, DOCX, and TXT files
- Automatic text extraction
- Document chunking
- Semantic embeddings generation
- Vector database indexing


## 🔍 Retrieval Augmented Generation

The system answers questions based only on uploaded project documents.

### RAG Pipeline
Document Upload
|
↓
Document Loader
|
↓
Text Splitting
|
↓
Embedding Generation
|
↓
ChromaDB Vector Store
|
↓
Semantic Retrieval
|
↓
LLM Response


---

# 🤖 Multi-Agent AI Architecture

The system uses a supervisor-based agent architecture.
                User
                 |
                 ↓
         Supervisor Agent
                 |
    --------------------------------
    |              |              |
    ↓              ↓              ↓
 QA Agent    Compliance Agent  Schedule Agent
    |              |              |
    --------------------------------
                 |
                 ↓
              RAG Tool
                 |
                 ↓
            ChromaDB
                 |
                 ↓
         Engineering Documents


## Available AI Agents

### 🔹 QA Agent
Handles general engineering questions.

### 🔹 Compliance Agent
Handles compliance requirements and standards.

### 🔹 Schedule Agent
Handles project planning and timelines.

### 🔹 Commissioning Agent
Handles commissioning procedures.

---

# 🏗️ System Architecture
            React Frontend
                  |
                  ↓
            FastAPI Backend
                  |
      --------------------------
      |                        |
      ↓                        ↓
 Upload API              Chat API
      |                        |
      ↓                        ↓
      Document Processing Supervisor Agent
                  | |
                   ↓ ---------------------
               ChromaDB | | |
                 ↓ ↓ ↓
         QA Compliance Schedule
                   |
                   ↓
               RAG Tool
                  |
                  ↓
          Vector Retrieval
                  | 
                  ↓
                 LLM


---

# 🛠️ Tech Stack

## Frontend

- React.js
- Vite
- JavaScript
- HTML/CSS


## Backend

- Python
- FastAPI
- REST API


## AI / RAG

- LangChain
- LangGraph
- HuggingFace Embeddings
- ChromaDB
- Retrieval Augmented Generation


## LLM

- Ollama
- Local LLM Models


## Document Processing

- PyPDFLoader
- Docx2txtLoader
- TextLoader
- RecursiveCharacterTextSplitter

---

# 📂 Project Structure
DataCenter-RAG/

├── backend/
│ ├── agents/
│ │ ├── compliance/
│ │ ├── commissioning/
│ │ ├── qa/
│ │ ├── schedule/
│ │ └── supervisor/
│ │
│ ├── app/
│ │ └── api/
│ │
│ ├── tools/
│ │ └── rag_tool.py
│ │
│ └── schemas/
│
├── rag/
│ ├── ingestion.py
│ ├── retrieval.py
│ ├── pipeline.py
│ └── llm.py
│
├── frontend/
│ ├── src/
│ └── package.json
│
├── requirements.txt
├── README.md
└── .gitignore


---
