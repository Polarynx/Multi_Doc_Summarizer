# Multi-Document Project Analyzer

## Project Overview
The Multi-Document Project Analyzer is a Python-based tool designed to help users understand complex projects by combining **AI-powered summarization** with **interactive knowledge graph visualization**. It ingests multiple document formats (DOCX, PPTX, XLSX), extracts key information, and presents it in a way that is **easy to explore, analyze, and understand**.

This tool is ideal for project managers, technical analysts, or anyone who wants to quickly extract insights from large sets of project documents.

---

## Included Tools

### 1. RAG Summarizer
- **File:** `app_project_rag.py`
- **Function:** Acts as a project assistant. You can ask natural language questions about your project, and it will answer based on the contents of the provided project documents.
- **Technology:** Uses Ollama LLM via a local API (`venv_ollama` required).

### 2. Knowledge Graph Visualizer
- **File:** `visualize_v3.py`
- **Function:** Generates an interactive knowledge graph showing entities (nodes) and their relationships extracted across all project documents.
- **Features:**  
  - Unique node colors based on project topics  
  - Click-to-source functionality (shows which document the node comes from)  
  - Node search and highlight  
  - Interactive physics-based layout  
- **Technology:** Uses Python libraries (`venv311` required).

---

## Methodology

The tool works in the following steps:

1. **Document Ingestion**
   - All documents in the `project_docs/` folder (DOCX, PPTX, XLSX) are processed by `document_loader.py`.
   - Text is extracted and saved into a structured JSON file: `extracted_documents.json`.
   
2. **Question Answering (RAG Summarizer)**
   - The RAG Summarizer (`app_project_rag.py`) uses the JSON file as its knowledge base.
   - Users can ask questions about the project; the AI answers accurately using the project content.
   - Questions about integration, weaknesses, or general knowledge are handled with caution to avoid hallucination.

3. **Knowledge Graph Visualization**
   - The Visualizer (`visualize_v3.py`) reads the JSON file and generates a graph.
   - Each entity from all documents is represented as a node, with relationships inferred by AI.
   - Nodes are color-coded by project topics.
   - Interactive HTML file generated: `knowledge_graph.html`.

---

## Environment Setup

Two separate Python virtual environments are required:

### 1. RAG Summarizer Environment (`venv_ollama`)
```bash
python -m venv venv_ollama
venv_ollama\Scripts\activate      # Windows
source venv_ollama/bin/activate   # macOS/Linux
pip install -r requirements_ollama.txt
```
Requirements:
  - ollama
  - requests
    
### 2. Visualizer Environment (`venv311`)
```bash
python -m venv venv311
venv311\Scripts\activate          # Windows
source venv311/bin/activate       # macOS/Linux
pip install -r requirements_311.txt
python -m spacy download en_core_web_sm
```
Requirements:
  - spacy
  - pyvis
  - networkx
  - python-docx
  - python-pptx
  - pandas
  - openpyxl
  - numpy
#### **Note: Each tool uses a seperate virtual environemnt to avoid package conflicts**
---
## Directory & File Overview 
  - project_docs/ - contains all project source documents (DOCX, PPTX, XLSX) used for ingestion.
  - extracted_documents.json – JSON output from document_loader.py containing the processed text from all documents.
  - app_project_rag.py – RAG summarizer for natural language Q&A about the project.
  - visualize_v3.py – Interactive knowledge graph generator using all project documents.
  - requirements_ollama.txt – Python dependencies for the summarizer (venv_ollama).
  - requirements_311.txt – Python dependencies for the visualizer (venv311).
  - knowledge_graph.html – Example interactive knowledge graph generated from the sample documents.
  - gitignore – Specifies files/directories to exclude from the repo (virtual environments, large outputs, etc.)
---
## How to Use
1. Prepare the environments (reference Environment Setup above)
2. Ingest documents
   ```bash
   python document_loader.py
   ```
3. Run RAG Summarizer
   ```bash
   python app_project_rag.py
   ```
4. Run Knowledge Graph Visualizer
   ```bash
   python visualize_v3.py
   ```
---
## Demo Video
This is a ~10 minute live demo of the tools, a walkthrough of both frameworks: https://drive.google.com/file/d/1aGUwjw3T0zr5GHH7Of98-X-RVcLxKy__/view?usp=sharing

