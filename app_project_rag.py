# app_project_rag.py
import ollama
import os
import json
import textwrap

# ----------------------------
# Load Project JSON Data
# ----------------------------
def load_project_json(file_path="extracted_documents.json"):
    """
    Load all project documents from JSON file.
    Returns a combined text of all content sections.
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return ""

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in {file_path}")
            return ""

    # Combine all content into a single text block
    combined_text = []
    for entry in data:
        content = entry.get("content", "").strip()
        if content:
            combined_text.append(content)

    return "\n\n".join(combined_text)

# ----------------------------
# Chunking Utility
# ----------------------------
def chunk_text(text, max_chars=2000):
    """
    Breaks long project text into manageable chunks for Ollama.
    """
    return textwrap.wrap(text, max_chars)

# ----------------------------
# Ask Question Using Ollama
# ----------------------------
def ask_question(project_text, question, model="mistral"):
    """
    Calls Ollama with project context + user question.
    Chunks large text automatically for performance.
    """
    if not project_text:
        return "❌ No project data available."

    chunks = chunk_text(project_text)
    combined_context = "\n\n".join(chunks)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a project assistant. Answer questions using ONLY the "
                "provided project information. If a question requires general "
                "knowledge about system integration, weaknesses, or best practices, "
                "you may answer using general domain knowledge, but never invent "
                "project-specific facts."
            )
        },
        {
            "role": "user",
            "content": f"Project Data:\n{combined_context}\n\nQuestion:\n{question}"
        }
    ]

    try:
        response = ollama.chat(model=model, messages=messages)
        return response["message"]["content"]
    except Exception as e:
        return f"❌ Error calling Ollama: {e}"

# ----------------------------
# Interactive Loop
# ----------------------------
def main():
    project_text = load_project_json()
    if not project_text:
        return

    print("📄 Project loaded from JSON. You can now ask questions.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("❓ Ask: ").strip()
        if question.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break

        print("💻 Thinking…")
        answer = ask_question(project_text, question)
        print(f"💡 Answer: {answer}\n")

# ----------------------------
if __name__ == "__main__":
    main()

