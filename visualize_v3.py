# visualize_v3.py
from pyvis.network import Network
import networkx as nx
import spacy
import json
from collections import Counter, defaultdict
import random
import re

nlp = spacy.load("en_core_web_sm")

# ----------------------------
# Load JSON
# ----------------------------
def load_project_json(path="extracted_documents.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------
# Helpers
# ----------------------------
def normalize(text):
    return text.strip().title()

def is_metadata(text):
    blacklist = {"project", "name", "overview", "introduction", "architecture"}
    return text.lower() in blacklist or len(text) < 3

# ----------------------------
# DOCX / PDF extraction (linguistic + fallback)
# ----------------------------
def extract_from_sentences(block, relationships):
    doc = nlp(block["content"])
    src = block["source_file"]

    for sent in doc.sents:
        subjects = [t for t in sent if t.dep_ in ("nsubj", "nsubjpass")]
        objects = [t for t in sent if t.dep_ in ("dobj", "attr", "pobj")]

        if subjects and objects:
            verb = sent.root.lemma_
            for s in subjects:
                for o in objects:
                    relationships.append({
                        "subject": normalize(s.text),
                        "relation": verb,
                        "object": normalize(o.text),
                        "source_file": src
                    })
        else:
            # fallback: noun–noun pairing
            nouns = [t.text for t in sent if t.pos_ in ("NOUN", "PROPN")]
            if len(nouns) >= 2:
                relationships.append({
                    "subject": normalize(nouns[0]),
                    "relation": "associated with",
                    "object": normalize(nouns[1]),
                    "source_file": src
                })

# ----------------------------
# PPTX bullet extraction
# ----------------------------
def extract_from_bullets(block, relationships):
    src = block["source_file"]
    lines = block["content"].splitlines()

    for line in lines:
        parts = re.split(r"\band\b|\bwith\b", line, flags=re.I)
        parts = [normalize(p) for p in parts if len(p.strip()) > 3]

        if len(parts) >= 2:
            relationships.append({
                "subject": parts[0],
                "relation": "combined with",
                "object": parts[1],
                "source_file": src
            })

# ----------------------------
# XLSX structured extraction
# ----------------------------
def extract_from_xlsx(block, relationships):
    src = block["source_file"]
    text = block["content"]

    service = re.search(r"Service:\s*(.+?)\s*\|", text)
    dependency = re.search(r"Dependency:\s*(.+)", text)

    if service and dependency:
        relationships.append({
            "subject": normalize(service.group(1)),
            "relation": "depends on",
            "object": normalize(dependency.group(1)),
            "source_file": src
        })

# ----------------------------
# Master extraction
# ----------------------------
def extract_relationships(blocks):
    relationships = []

    for block in blocks:
        t = block["source_type"]

        if t in ("docx", "pdf"):
            extract_from_sentences(block, relationships)
        elif t == "pptx":
            extract_from_bullets(block, relationships)
        elif t == "xlsx":
            extract_from_xlsx(block, relationships)

    return relationships

# ----------------------------
# Topics
# ----------------------------
def extract_project_topics(blocks, n=5):
    text = " ".join(b["content"] for b in blocks)
    doc = nlp(text)

    nouns = [t.lemma_.lower() for t in doc if t.pos_ in ("NOUN", "PROPN")]
    common = Counter(nouns).most_common(n)

    return [w for w, _ in common]

# ----------------------------
# Graph
# ----------------------------
def build_graph(relations):
    G = nx.DiGraph()
    files = defaultdict(set)

    for r in relations:
        s, o = r["subject"], r["object"]
        files[s].add(r["source_file"])
        files[o].add(r["source_file"])
        G.add_edge(s, o, label=r["relation"])

    for n in G.nodes:
        G.nodes[n]["files"] = sorted(files[n])

    return G

# ----------------------------
# Visualization
# ----------------------------
def visualize(G, topics):
    net = Network(height="800px", width="100%", directed=True)
    net.barnes_hut(gravity=-20000)

    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    topic_map = {topics[i]: palette[i] for i in range(len(topics))}

    for n, a in G.nodes(data=True):
        topic = next((t for t in topics if t in n.lower()), random.choice(topics))
        files = "\n".join(f"• {f}" for f in a["files"])

        net.add_node(
            n,
            label=n,
            color=topic_map[topic],
            title=f"Sources:\n{files}"
        )

    for u, v, a in G.edges(data=True):
        net.add_edge(u, v, label=a["label"], arrows="to")

    net.show("knowledge_graph.html", notebook=False)

# ----------------------------
# Main
# ----------------------------
def main():
    blocks = load_project_json()
    relations = extract_relationships(blocks)

    print(f"✅ Extracted {len(relations)} relationships")

    G = build_graph(relations)
    topics = extract_project_topics(blocks)

    visualize(G, topics)
    print("🎉 Graph generated")

if __name__ == "__main__":
    main()
