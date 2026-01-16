# Multi_Doc_Summarizer

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
