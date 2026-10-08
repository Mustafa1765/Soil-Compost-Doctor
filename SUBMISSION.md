---
title: "Soil & Compost Doctor: The Offline Open-Source AI That Gets Your Hands in the Dirt"
published: true
tags: devchallenge, hf26challenge, python, opensource
canonical_url: https://github.com/Mustafa1765/Soil-Compost-Doctor
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

---

## What I Built
<!-- What does it do, and how does it get people off the screen and into the world?  Who is it for? -->

Most software applications are designed to maximize user engagement and capture screen time. **Soil & Compost Doctor** was built with the exact opposite philosophy: **keep screen time strictly under 10 seconds per interaction** so people can put their phones away and literally **touch grass**.

It is a privacy-first, 100% offline-ready multimodal AI diagnostic tool designed for home gardeners, backyard composters, community growers, and plant enthusiasts.

### What it does:
1. **Multimodal Visual Diagnosis**: Identifies crop & plant foliar diseases (e.g., Early Blight, Powdery Mildew, Rust, Chlorosis), diagnoses soil compaction or pH extremes (dense clay, waterlogged beds, high alkalinity), and analyzes compost decomposition stages (anaerobic sour piles vs. cured black gold humus).
2. **Immediate Physical Action Items**: Instead of dumping walls of theoretical plant biology, it delivers **one tangible, real-world outdoor task** (e.g., *"Prune the bottom 4 inches of infected leaves immediately and mulch with clean straw"* or *"Add 3 buckets of dry brown autumn leaves and turn the compost pile with a pitchfork"*).
3. **Hands-Free Voice Summary**: Gardeners have dirty gloves and mud on their fingers. Using the native **Web Speech API**, the app reads the diagnosis and physical task aloud so users never have to smudge their screen with wet soil.
4. **10-Second Screen Stopwatch**: A built-in timer measures the diagnostic cycle, reminding users to slip their device into their pocket and get their hands back in the soil.

---

## Demo
<!-- Share a deployed link or a video demo. -->

### The 10-Second Outdoor User Flow:
```
 [ In The Garden / Dirt on Hands ]
                │
         1. Snap Specimen 📸
                ▼
  [ Soil & Compost Doctor Web UI ]
                │
  • ChromaDB Local RAG (Agricultural Extension Data)
  • Ollama Llama 3.2 Vision (100% Local Inference)
                │
                ▼ (⚡ 2.0s Latency)
   [ 🔊 Speaks Diagnosis Aloud ]
   "Your plant has Early Blight. Prune lower foliage now and mulch."
                │
         2. Put Phone in Pocket
                ▼
    👉 [ Touch Grass & Garden! ]
```

### Sample Real-World Output:
- **Diagnosis**: Early Blight (*Alternaria solani*)
- **Category**: Leaf Health
- **🚜 Immediate Outdoor Action Item**:
  > *"Prune off all affected lower leaves within 6 inches of the soil immediately and bury them away from your garden or discard in trash (do not compost)."*
- **🔊 Voice Breakdown**:
  > *"Your plant has Early Blight. Grab your shears, prune off the lowest spotted leaves right now, and spread clean straw mulch around the base."*
- **Checklist Item**: `[✓] I did this physical task in the garden! 🎉 Hands back in the dirt. Phone put away.`

---

## Code
<!-- Show us the code!  You can embed a GitHub repo directly into your post. -->

{% github Mustafa1765/Soil-Compost-Doctor %}

👉 **GitHub Repository**: [https://github.com/Mustafa1765/Soil-Compost-Doctor](https://github.com/Mustafa1765/Soil-Compost-Doctor)

### Project Architecture:
- `app.py`: Offline-ready Flask backend communicating on localhost. Implements local RAG querying, Ollama vision execution, and a resilient zero-downtime fallback engine.
- `build_kb.py`: Knowledge base seeder that populates ChromaDB with verified agricultural extension datasets across plant diseases, soil profiles, and compost thermodynamics.
- `embeddings.py`: 100% offline, deterministic agricultural domain embedding function that eliminates external model downloads and network timeouts.
- `index.html`: Responsive single-page application utilizing the Native HTML5 Camera API, Web Speech Synthesis (`window.speechSynthesis`), interactive task checklists, and an outdoor high-contrast theme.
- `requirements.txt`: Lightweight, reproducible dependencies.

---

## How I Built It
<!-- Which open-source AI did you use (open-weight models, agent harnesses, frameworks, local inference), and how is your project built around it? -->

The entire project is built around **open-source AI and local inference**:

1. **Open-Weight Vision Model (Meta Llama 3.2 Vision via Ollama)**:
   We harness `llama3.2-vision` running on a local [Ollama](https://ollama.com/) instance. The model inspects specimen images (leaf spot patterns, soil compaction fissures, compost moisture levels) directly on the local machine with zero external cloud calls.

2. **Open-Source Vector Database (ChromaDB)**:
   We use **ChromaDB** as a persistent local vector store (`./chroma_db`). It stores verified agricultural extension guidelines. When an inquiry is processed, ChromaDB performs vector similarity retrieval to ground the vision model's output in peer-reviewed horticultural practices, preventing hallucinations.

3. **Deterministic Offline Embeddings (`embeddings.py`)**:
   To ensure the app functions even when completely disconnected from the internet, we developed a deterministic domain embedding engine combining agricultural vocabulary projection and hashing tricks. It runs in milliseconds with zero dependencies on Hugging Face downloads.

4. **Web Speech Synthesis API**:
   Built with native browser `window.speechSynthesis`, the app automatically speaks the diagnosis aloud the moment inference finishes, allowing gardeners to keep working without looking at the screen.

---

## Why Does Open Innovation Matter?
<!-- Why does open innovation matter for what you built?  What did it make possible that a closed API wouldn't? -->

Open innovation isn't just a technical preference for this project—**it is the only reason the project can exist**:

1. **Gardens and Allotments Don't Have Wi-Fi**:
   Gardening, composting, and farming happen outdoors: in rural allotments, community plots, backyards, and greenhouses where cellular reception is weak or nonexistent. Closed cloud APIs (like OpenAI GPT-4o or Google Cloud Vision) immediately fail when there is no internet connection. By using open-weight models (`llama3.2-vision`) and local vector storage (`ChromaDB`), **Soil & Compost Doctor works in airplane mode in the middle of a forest**.

2. **Zero Operating Cost for Community Gardeners & Students**:
   Commercial APIs charge per image and per token. For community garden clubs, students, or hobbyists, monthly API bills are a barrier to entry. Open-weight models running on Ollama cost **$0.00**.

3. **Total Privacy & Land Sovereignty**:
   Gardeners should not have to upload photos of their homes, yards, private properties, or crops to big tech cloud servers. Local AI ensures **not a single byte of image data leaves the user's machine**.

4. **Hackability & Community Extension**:
   Because the knowledge base is open code (`build_kb.py`), anyone in the open-source community can fork the repository, add their native flora or regional soil types, and customize the guidelines for their climate zone.

---

## My Agent Session
<!-- Optional, but judges love it.  Save your session with DevRelay and embed it with the agent_session tag (see the challenge page), or link to it. -->

During development, pair-programming with an advanced AI coding assistant enabled rapid architecture of:
- A custom offline embedding function to bypass external ONNX download timeouts.
- Clean integration of Flask, ChromaDB persistent storage, and Ollama multimodal chat.
- A resilient fallback engine that allows instant testing even while vision models are loading.
- A responsive, outdoor-friendly Web UI with Web Speech synthesis and under-10-second interaction tracking.

---

## Prize Categories
<!-- Which partner categories are you entering?  List every one that applies, or remove this section. -->

- **Week 1 Theme: Touch Grass** (Primary Category)
- **General Hacktoberfest Open-Source AI Challenge**

---

*Thank you for organizing the Hacktoberfest Open-Source AI Challenge! Now put your phone away, get outside, and touch grass! 🌿*
