# 🌿 Soil & Compost Doctor
### *Touch Grass Edition — Privacy-First, Offline-Ready AI for Gardeners*

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-Week%201%3A%20Touch%20Grass-brightgreen.svg)](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Local Inference](https://img.shields.io/badge/Local%20AI-Ollama%20%2B%20ChromaDB-blue.svg)](#)
[![Screen Time](https://img.shields.io/badge/Screen%20Time-%3C%2010s-orange.svg)](#)

> **"Put your phone away and get your hands in the dirt."**  
> An open-source, local-first multimodal AI assistant designed to identify plant leaf diseases, diagnose soil deficiencies, evaluate compost decomposition stages, and deliver immediate physical outdoor tasks in under 10 seconds.

---

## 🎯 The "Touch Grass" Philosophy

Technology usually keeps us glued to screens. **Soil & Compost Doctor is engineered to do the exact opposite**:
1. **Under 10 Seconds Screen Time**: Snap a photo or tap a specimen preset.
2. **Hands-Free Audio Readout**: The Web Speech API speaks the immediate diagnosis and physical instructions aloud so you don't need to tap a phone screen with muddy gardening gloves.
3. **Real-World Action Item**: Every scan outputs a concrete physical task (e.g., *"Prune bottom 4 inches of infected leaves,"* or *"Add 3 buckets of dry brown leaves and turn the pile"*).
4. **100% Offline & Open-Weight**: Works deep in your garden, at a community allotment, or on remote farmland with zero cell reception and zero cloud data leaks.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│  GARDEN / OUTDOOR ENVIRONMENT (No Internet Required)  │
└────────────────────────────────────────────────────────┘
                           │
                 [1] Snap Photo (Mobile Camera)
                           ▼
         ┌───────────────────────────────────┐
         │       Local Web UI (PWA)          │
         │   • Camera & HTML5 File API       │
         │   • Web Speech Synthesis API      │
         │   • 10-Second Screen Stopwatch    │
         └─────────────────┬─────────────────┘
                           │ POST /diagnose (Localhost)
                           ▼
         ┌───────────────────────────────────┐
         │       Flask Backend Server        │
         └─────────┬───────────────┬─────────┘
                   │               │
        [2] RAG Vector Search      │ [3] Multimodal Vision Prompt
                   ▼               ▼
         ┌────────────────┐ ┌────────────────────────┐
         │   ChromaDB     │ │  Ollama Local Server   │
         │ (Vector Store) │ │  (llama3.2-vision)     │
         │ Open Extension │ │  Open-Weight Model     │
         │ Knowledge Base │ │  100% On-Device GPU/CPU│
         └────────────────┘ └────────────────────────┘
                   │               │
                   └───────┬───────┘
                           │
                [4] Standardized JSON Output
                           ▼
         ┌───────────────────────────────────┐
         │   Spoken Audio + Real Action      │
         │   "Prune lower leaves now & mulch"│
         │   👉 Put phone away & TOUCH GRASS │
         └───────────────────────────────────┘
```

---

## ⚡ Quick Start (Beginner Friendly)

### 1. Prerequisites
- **Python 3.10 to 3.12** installed on your system.
- *(Optional for Vision LLM)*: [Ollama](https://ollama.com/) installed on your machine.

---

### 2. Setup Project Environment

Clone the repository and enter the directory:
```bash
git clone https://github.com/Mustafa1765/Soil-Compost-Doctor.git
cd Soil-Compost-Doctor
```

Create and activate a virtual environment:
- **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

Install the lightweight dependencies:
```bash
pip install -r requirements.txt
```

---

### 3. Seed the Local Knowledge Base (ChromaDB)

Seed your local vector database with verified agricultural extension guidelines:
```bash
python build_kb.py
```
*Output: Indexing records for Leaf Health, Soil Quality, and Compost Status into `./chroma_db`.*

---

### 4. (Optional) Setup Ollama & Local Vision Model

To enable full multimodal visual AI reasoning locally:
1. Download and run Ollama from [ollama.com](https://ollama.com).
2. Pull the open-weight vision model:
   ```bash
   ollama pull llama3.2-vision
   ```
*(Note: If Ollama is not installed or the model is still downloading, the app automatically runs in **Smart Local RAG Mode** using ChromaDB vector matching, so you can test and use it immediately with zero blockers!)*

---

### 5. Launch the Application

Start the local Flask server:
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📱 How to Use in the Garden

1. **Pick a Specimen**: Select a category (*Leaf Health*, *Soil Quality*, or *Compost Status*).
2. **Capture or Choose Photo**: Click **"Open Live Camera"** or snap a picture directly with your phone.
3. **Or Test 1-Click Samples**: Click preset chips like **"Early Blight"**, **"Compacted Clay"**, or **"Smelly Compost"** to test immediately.
4. **Instant Action**:
   - The diagnosis and physical task appear on screen.
   - The app **speaks the voice summary aloud** via the Web Speech API.
   - Check the physical task box, put your phone in your pocket, and get back to gardening!

---

## 📋 Standardized JSON Output Schema

Every diagnostic result adheres to this strict schema:
```json
{
  "diagnosis": "Early Blight (Alternaria solani)",
  "category": "Leaf Health",
  "real_world_task": "Prune off all affected lower leaves within 6 inches of the soil immediately and discard in trash.",
  "care_tips": [
    "Mulch heavily around the plant base with 2 inches of clean straw to prevent soil spores from splashing up.",
    "Water strictly at the soil base using a watering can—never wet the foliage."
  ],
  "spoken_summary": "Your plant has Early Blight. Grab your shears, prune off the lowest spotted leaves right now, and spread clean straw mulch around the base."
}
```

---

## 🔒 Why Open-Source AI Matters

| Feature | Closed Cloud APIs (OpenAI / Cloud Vision) | Open-Source AI (Ollama + ChromaDB) |
| :--- | :--- | :--- |
| **Connectivity** | Fails outdoors with weak/no internet signal | **100% Offline & works in remote fields** |
| **Data Privacy** | Images sent to corporate cloud servers | **Zero bytes leave your computer** |
| **Running Cost** | Per-token / per-image API subscription fees | **$0.00 Forever** |
| **Ownership** | Proprietary black box | **Fully hackable, inspectable, and student-friendly** |

---

## 📂 Project Structure

```
Soil-Compost-Doctor/
├── app.py              # Flask server, ChromaDB RAG integration & Ollama endpoint
├── build_kb.py         # Knowledge base seeder for local ChromaDB vector store
├── index.html          # Lightweight, mobile-first Web UI with Camera & Web Speech API
├── requirements.txt    # Project Python dependencies
├── chroma_db/          # Persistent local ChromaDB database (created by build_kb.py)
├── SUBMISSION.md       # Pre-written Dev.to Hacktoberfest submission article
└── README.md           # Documentation and setup guide
```

---

## 🏆 Hacktoberfest "Touch Grass" Submission
This project is submitted for the **Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass**.  
See [`SUBMISSION.md`](./SUBMISSION.md) for the complete submission post ready for [Dev.to](https://dev.to).