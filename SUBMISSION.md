---
title: "Soil & Compost Doctor: The Offline Local-AI That Gets Your Hands in the Dirt"
published: true
tags: devchallenge, hf26challenge, python, ai, opensource
canonical_url: https://github.com/Mustafa1765/Soil-Compost-Doctor
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

---

## 🌿 What I Built

Most modern technology is designed to maximize screen time. When I saw the **"Touch Grass"** Hacktoberfest challenge, I wanted to build the complete antithesis: an application where **screen time is strictly capped under 10 seconds**, engineered to get home gardeners, composters, and growers *off their phones and back into the living soil*.

**Soil & Compost Doctor** is a privacy-first, 100% offline-ready multimodal AI application that:
1. **Instantly Identifies Plant & Soil Troubles**: Diagnoses crop and plant diseases (e.g., early blight, powdery mildew, chlorosis), evaluates soil conditions (compacted clay, waterlogged beds, high alkalinity), and analyzes compost decomposition stages (anaerobic sour heaps vs. finished black gold).
2. **Issues Physical Outdoor Action Items**: Rather than presenting walls of academic text, it delivers a single, concrete physical task you can execute immediately with your garden shears, pitchfork, or watering can.
3. **Reads Aloud via Hands-Free Voice Synthesis**: With dirty gardening gloves, you don't want to keep touching a smartphone screen. The app uses the native Web Speech API to read the diagnosis and real-world task aloud, so you can slip your phone into your pocket and get straight to work.
4. **Runs Completely Offline**: Zero cloud calls, zero monthly subscriptions, zero telemetry. It works at the far corner of your backyard, a community allotment, or an off-grid farm without a cellular signal.

---

## 🎥 Demo

### User Flow in Under 10 Seconds:
1. **Snap or Tap**: The gardener snaps a photo of spotted leaves or a cold compost pile.
2. **Local RAG + Vision Inference**: The local ChromaDB vector store retrieves verified agricultural extension guidelines, and Ollama's local `llama3.2-vision` analyzes the visual features.
3. **Voice Summary**: The device speaks aloud: *"Your plant has Early Blight. Prune off the lowest spotted leaves within 6 inches of the ground right now and mulch the base with straw."*
4. **Touch Grass Action**: The gardener checks the task box, pockets their device, and returns to physical gardening.

---

## 💻 Code

The entire codebase is open-source and available on GitHub:
👉 **[Mustafa1765/Soil-Compost-Doctor](https://github.com/Mustafa1765/Soil-Compost-Doctor)**

### Key Components:
- `build_kb.py`: Seeds the local ChromaDB vector database with open agricultural extension guidelines across Leaf Health, Soil Quality, and Compost Status.
- `app.py`: Lightweight Python Flask backend handling RAG vector search, local Ollama multimodal inference, and a resilient fallback engine.
- `index.html`: Responsive mobile-first single-page application integrating camera APIs, the Web Speech API (`window.speechSynthesis`), a real-world task checklist, and a 10-second screen-time meter.
- `requirements.txt`: Minimal dependencies for easy reproduction.

---

## ⚙️ How I Built It

As a student developer, I wanted an architecture that was powerful yet simple and dependable:

1. **Local Vision Model (Ollama & Llama 3.2 Vision)**:
   We harness Meta's open-weight `llama3.2-vision` running on a local Ollama daemon. The model inspects leaf discoloration, lesion patterns, soil clumping, and compost texture entirely on-device without shipping photos to an external server.

2. **Local Vector Database (ChromaDB)**:
   We index open agricultural extension knowledge directly into a local persistent ChromaDB directory (`./chroma_db`). The knowledge base includes specific guidelines on fungal pathogens, macronutrient chlorosis, soil compaction physics, and carbon-to-nitrogen compost ratios. When a specimen is analyzed, ChromaDB retrieves verified remedies to ground the vision model's output and eliminate hallucinations.

3. **Hands-Free Speech Synthesis (Web Speech API)**:
   Using `window.speechSynthesis`, the browser automatically speaks the `spoken_summary` field the moment inference completes. This eliminates the need to touch the screen while wearing gardening gloves or handling compost.

4. **10-Second Screen Stopwatch**:
   A visible UI timer tracks the interaction duration, celebrating when the diagnosis completes well under the 10-second threshold.

---

## 🌍 Why Does Open Innovation Matter?

Why did open-source AI make this project possible when closed cloud APIs would have failed?

1. **Gardens Don't Have Wi-Fi**:
   Gardening and composting happen outside—in backyards, allotments, greenhouses, and rural farms where cellular connectivity is frequently unreliable or nonexistent. Closed APIs like OpenAI or Google Cloud Vision require a constant internet uplink. Because `llama3.2-vision` and `chromadb` run locally on localhost, the app functions flawlessly in airplane mode in the middle of a forest.

2. **Zero Operating Cost for Students and Community Gardeners**:
   Closed commercial APIs charge per token and per image. Open-weight models running on Ollama cost **$0.00**. Anyone with a laptop or mini PC can run this indefinitely without worrying about surprise credit card bills.

3. **Absolute Privacy & Data Sovereignty**:
   Gardeners shouldn't have to upload photos of their homes, yards, or property to corporate cloud servers. With open-source local AI, every byte of visual data stays on the user's hardware.

4. **Hackable & Extensible**:
   Because the knowledge base is a simple local ChromaDB database (`build_kb.py`), any gardener or school club can easily add their own regional plant species, local soil types, or native pest remedies without waiting for a third-party company to update their model.

---

## 🏆 Prize Categories

- **Week 1 Theme: Touch Grass**
- **General Hacktoberfest Challenge**

---

*Built with passion for open-source AI and healthy gardens during Hacktoberfest 2026.*
