"""
app.py - Soil & Compost Doctor Backend Server
===============================================
Project: Soil & Compost Doctor (Hacktoberfest "Touch Grass" Challenge)
Author: Student Builder
Description:
  Offline-ready Flask backend that integrates:
  1. ChromaDB local vector database (retrieves verified agricultural extension guidelines)
  2. Local Ollama AI client (runs open-weight `llama3.2-vision` locally with no cloud dependencies)
  3. Resilient fallback engine (delivers instant offline RAG diagnosis even if Ollama is starting up)
  4. Native Web UI serving & diagnostic API endpoint (/diagnose)
"""

import os
import sys
import io
import time
import json
import base64
import re
from typing import Dict, Any, List, Optional

# Ensure UTF-8 output on Windows console
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
from PIL import Image
from embeddings import get_embedding_function

# Initialize Flask App
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# Local ChromaDB Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "soil_compost_kb"
OLLAMA_MODEL_DEFAULT = "llama3.2-vision"

# Global references for DB and Ollama
_chroma_client = None
_chroma_collection = None


def get_chroma_collection():
    """Initializes and returns the ChromaDB collection with automatic seeding if needed."""
    global _chroma_client, _chroma_collection
    if _chroma_collection is not None:
        return _chroma_collection

    try:
        import chromadb
        _chroma_client = chromadb.PersistentClient(path=DB_DIR)
        ef = get_embedding_function()
        
        # Check if collection exists
        existing_collections = [c.name for c in _chroma_client.list_collections()]
        if COLLECTION_NAME not in existing_collections:
            print("[*] ChromaDB collection not found on first load. Running seeder...")
            try:
                from build_kb import build_vector_database
                build_vector_database()
            except Exception as seed_err:
                print(f"[!] Warning: Seeder execution error: {seed_err}")

        _chroma_collection = _chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef
        )
        print(f"[+] ChromaDB connected. Total records: {_chroma_collection.count()}")
        return _chroma_collection
    except Exception as e:
        print(f"[!] Warning: ChromaDB initialization error: {e}")
        return None


def check_ollama_status() -> Dict[str, Any]:
    """Checks if the local Ollama daemon is reachable and lists installed models."""
    try:
        import ollama
        models_resp = ollama.list()
        models_list = []
        # Support both object and dict formats across ollama-python versions
        if hasattr(models_resp, "models"):
            for m in models_resp.models:
                models_list.append(getattr(m, "model", getattr(m, "name", str(m))))
        elif isinstance(models_resp, dict) and "models" in models_resp:
            for m in models_resp["models"]:
                models_list.append(m.get("name") or m.get("model"))
        
        has_vision = any("llama3.2-vision" in m or "llava" in m for m in models_list)
        return {
            "online": True,
            "models": models_list,
            "has_vision_model": has_vision,
            "preferred_model": OLLAMA_MODEL_DEFAULT if has_vision else (models_list[0] if models_list else None)
        }
    except Exception as e:
        return {
            "online": False,
            "models": [],
            "has_vision_model": False,
            "error": str(e)
        }


def query_rag_knowledge(query_text: str, category_filter: Optional[str] = None, n_results: int = 3) -> List[Dict[str, Any]]:
    """Queries the local ChromaDB vector collection for relevant agricultural knowledge."""
    collection = get_chroma_collection()
    if collection is None or collection.count() == 0:
        return []

    try:
        where_filter = None
        if category_filter and category_filter not in ["All", "Auto-Detect", ""]:
            where_filter = {"category": category_filter}

        query_args = {
            "query_texts": [query_text],
            "n_results": min(n_results, collection.count())
        }
        if where_filter:
            query_args["where"] = where_filter

        results = collection.query(**query_args)
        
        retrieved = []
        if results and "metadatas" in results and results["metadatas"]:
            for meta in results["metadatas"][0]:
                retrieved.append(meta)
        return retrieved
    except Exception as e:
        print(f"[!] ChromaDB query error: {e}")
        return []


def parse_llm_json(raw_text: str) -> Optional[Dict[str, Any]]:
    """Extracts and parses JSON object from LLM response text."""
    if not raw_text:
        return None

    # Try 1: Find ```json ... ``` code fence
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass

    # Try 2: Find outermost curly braces
    first_brace = raw_text.find("{")
    last_brace = raw_text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        json_candidate = raw_text[first_brace : last_brace + 1]
        try:
            return json.loads(json_candidate)
        except Exception:
            pass

    # Try 3: Direct parsing
    try:
        return json.loads(raw_text)
    except Exception:
        return None


def format_standard_output(diagnosis: str, category: str, real_world_task: str, care_tips: List[str], spoken_summary: str) -> Dict[str, Any]:
    """Ensures output strictly matches the required Hacktoberfest JSON specification."""
    # Validate category format
    valid_categories = ["Leaf Health", "Soil Quality", "Compost Status"]
    if category not in valid_categories:
        # Default or map
        cat_lower = category.lower()
        if "leaf" in cat_lower or "plant" in cat_lower:
            category = "Leaf Health"
        elif "soil" in cat_lower or "clay" in cat_lower or "sand" in cat_lower:
            category = "Soil Quality"
        elif "compost" in cat_lower or "pile" in cat_lower:
            category = "Compost Status"
        else:
            category = "Leaf Health"

    return {
        "diagnosis": diagnosis.strip(),
        "category": category,
        "real_world_task": real_world_task.strip(),
        "care_tips": [tip.strip() for tip in care_tips if str(tip).strip()],
        "spoken_summary": spoken_summary.strip()
    }


# =====================================================================
# API ROUTES
# =====================================================================

@app.route("/")
def index():
    """Serves the single-page application."""
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(BASE_DIR, "index.html")
    return "<h1>Soil & Compost Doctor</h1><p>index.html not found. Please ensure index.html exists in project root.</p>", 404


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health status endpoint reporting local ChromaDB and Ollama status."""
    ollama_info = check_ollama_status()
    collection = get_chroma_collection()
    kb_count = collection.count() if collection is not None else 0

    return jsonify({
        "status": "healthy",
        "offline_ready": True,
        "chromadb": {
            "status": "active" if collection is not None else "unavailable",
            "records_count": kb_count,
            "directory": DB_DIR
        },
        "ollama": ollama_info,
        "active_vision_model": OLLAMA_MODEL_DEFAULT
    })


@app.route("/api/sample-cases", methods=["GET"])
def get_sample_cases():
    """Returns preset garden scenarios so users can test offline with 1 click."""
    samples = [
        {
            "id": "sample_blight",
            "title": "Tomato Early Blight",
            "category": "Leaf Health",
            "query": "Dark brown spots with concentric target rings on lower tomato leaves with yellowing",
            "sample_note": "Found dark spots on the bottom leaves of my tomato plant after rainy week."
        },
        {
            "id": "sample_mildew",
            "title": "Squash Powdery Mildew",
            "category": "Leaf Health",
            "query": "White powder coating on upper zucchini leaves like flour or dust",
            "sample_note": "White powdery dust covering the leaves in shaded garden corner."
        },
        {
            "id": "sample_clay",
            "title": "Compacted Clay Bed",
            "category": "Soil Quality",
            "query": "Hard dense cracked clay soil, puddles when watering, cannot push trowel in",
            "sample_note": "Garden bed is rock hard and cracks when dry, turns to sticky mud."
        },
        {
            "id": "sample_smelly_compost",
            "title": "Anaerobic Smelly Compost",
            "category": "Compost Status",
            "query": "Smelly rotten egg compost pile, slimy wet food scraps, no airflow",
            "sample_note": "Compost pile smells foul like rotten eggs and looks dark and slimy."
        },
        {
            "id": "sample_black_gold",
            "title": "Finished Cured Compost",
            "category": "Compost Status",
            "query": "Crumbly dark black gold compost smelling like earthy forest floor, ready for beds",
            "sample_note": "Pile has been curing for 4 months, smells sweet and earthy like woods."
        }
    ]
    return jsonify({"samples": samples})


@app.route("/diagnose", methods=["POST"])
def diagnose():
    """
    Main diagnostic endpoint:
    Accepts:
      - JSON body or Multipart Form:
        - `image`: Base64 data URI string or raw base64
        - `category`: 'Leaf Health' | 'Soil Quality' | 'Compost Status' | 'Auto-Detect'
        - `note`: Optional gardener observation (e.g. 'leaves yellowing', 'pile smells sour')
    Returns:
      Exact JSON schema required for Hacktoberfest 'Touch Grass' challenge.
    """
    start_time = time.time()
    
    # Extract payload
    image_data = None
    category = "Auto-Detect"
    user_note = ""

    if request.is_json:
        data = request.get_json(silent=True) or {}
        image_data = data.get("image")
        category = data.get("category", "Auto-Detect")
        user_note = data.get("note", "")
    else:
        category = request.form.get("category", "Auto-Detect")
        user_note = request.form.get("note", "")
        if "image" in request.files:
            file = request.files["image"]
            image_bytes = file.read()
            image_data = base64.b64encode(image_bytes).decode("utf-8")
        elif "image" in request.form:
            image_data = request.form.get("image")

    # Clean base64 image prefix if present (e.g. "data:image/jpeg;base64,...")
    raw_b64 = image_data
    if raw_b64 and "," in raw_b64:
        raw_b64 = raw_b64.split(",", 1)[1]

    # Formulate RAG search query
    search_terms = []
    if user_note.strip():
        search_terms.append(user_note.strip())
    if category and category not in ["Auto-Detect", "All"]:
        search_terms.append(f"Category {category}")
    if not search_terms:
        search_terms.append("Garden plant leaf soil or compost diagnosis")

    rag_query_text = " ".join(search_terms)

    # 1. Query Local ChromaDB Vector Store
    rag_matches = query_rag_knowledge(
        query_text=rag_query_text,
        category_filter=category if category not in ["Auto-Detect", "All"] else None,
        n_results=3
    )

    # Construct context snippet from RAG
    rag_context_str = ""
    top_rag_match = rag_matches[0] if rag_matches else None
    if rag_matches:
        rag_snippets = []
        for idx, doc in enumerate(rag_matches, 1):
            rag_snippets.append(
                f"[Guideline #{idx}]\n"
                f"Diagnosis: {doc.get('diagnosis')}\n"
                f"Category: {doc.get('category')}\n"
                f"Symptoms: {doc.get('symptoms')}\n"
                f"Outdoor Physical Task: {doc.get('real_world_task')}\n"
                f"Care Tips: {doc.get('care_tips_json', '[]')}\n"
                f"Spoken Summary: {doc.get('spoken_summary')}"
            )
        rag_context_str = "\n\n".join(rag_snippets)

    # Check Ollama AI availability
    ollama_info = check_ollama_status()
    parsed_result = None
    ai_engine_used = "chroma_rag_local"

    # 2. If Ollama is online with vision capability, execute multimodal vision inference
    if ollama_info.get("online") and raw_b64:
        target_model = ollama_info.get("preferred_model") or OLLAMA_MODEL_DEFAULT
        try:
            import ollama

            system_instruction = (
                "You are Soil & Compost Doctor, a local offline AI assistant designed for the Hacktoberfest 'Touch Grass' challenge. "
                "Your mission: Help gardeners identify plant/soil/compost issues in UNDER 10 SECONDS so they can put their phone away "
                "and get back to physical gardening outdoors.\n\n"
                "You have access to open agricultural extension guidelines retrieved from a local vector database:\n"
                f"{rag_context_str}\n\n"
                "INSTRUCTIONS:\n"
                "1. Analyze the provided image and gardener notes.\n"
                "2. Synthesize with the agricultural guidelines provided.\n"
                "3. Provide ONE clear, immediate physical task they can do right now with their hands/tools outdoors.\n"
                "4. You MUST respond with ONLY a valid, parseable JSON object matching this exact schema:\n"
                "{\n"
                '  "diagnosis": "Name of plant issue or compost stage",\n'
                '  "category": "Leaf Health | Soil Quality | Compost Status",\n'
                '  "real_world_task": "Clear, physical step to execute right now in the garden",\n'
                '  "care_tips": ["Tip 1", "Tip 2"],\n'
                '  "spoken_summary": "1-2 sentence voice breakdown to read aloud"\n'
                "}\n"
                "Do not include any conversational filler, markdown intro, or text outside the JSON block."
            )

            user_prompt = f"Analyze this garden specimen. Category hint: {category}. Gardener observation: {user_note or 'Visual inspection'}. Provide immediate physical action."

            # Execute Ollama local chat
            response = ollama.chat(
                model=target_model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {
                        "role": "user",
                        "content": user_prompt,
                        "images": [raw_b64]
                    }
                ],
                options={"temperature": 0.2, "num_predict": 400}
            )

            response_content = ""
            if hasattr(response, "message"):
                response_content = response.message.content
            elif isinstance(response, dict) and "message" in response:
                response_content = response["message"].get("content", "")

            parsed_result = parse_llm_json(response_content)
            if parsed_result:
                ai_engine_used = f"ollama_{target_model}"

        except Exception as ollama_err:
            print(f"[!] Ollama vision inference notice: {ollama_err}. Utilizing local ChromaDB RAG fallback.")

    # 3. Graceful Offline RAG Synthesis (Guarantees zero downtime and 100% offline reliability)
    if not parsed_result:
        if top_rag_match:
            try:
                care_tips_list = json.loads(top_rag_match.get("care_tips_json", "[]"))
            except Exception:
                care_tips_list = ["Inspect soil moisture regularly.", "Aerate root perimeter."]

            parsed_result = format_standard_output(
                diagnosis=top_rag_match.get("diagnosis", "Garden Plant Health Check"),
                category=top_rag_match.get("category", "Leaf Health"),
                real_world_task=top_rag_match.get("real_world_task", "Inspect plant foliage and water root base deeply."),
                care_tips=care_tips_list,
                spoken_summary=top_rag_match.get("spoken_summary", "Inspection complete. Check your soil and prune damaged foliage.")
            )
        else:
            # Fallback general garden diagnostic
            parsed_result = format_standard_output(
                diagnosis="Garden Specimen Inspection",
                category=category if category in ["Leaf Health", "Soil Quality", "Compost Status"] else "Leaf Health",
                real_world_task="Examine soil moisture with your finger 2 inches deep and add organic mulch around base.",
                care_tips=[
                    "Maintain steady, deep watering early in the morning.",
                    "Ensure adequate garden bed spacing for air circulation."
                ],
                spoken_summary="Specimen inspected. Check your soil moisture two inches down and clear debris around the stem."
            )

    # Enforce strict output schema
    standard_response = format_standard_output(
        diagnosis=parsed_result.get("diagnosis", "Garden Health Check"),
        category=parsed_result.get("category", "Leaf Health"),
        real_world_task=parsed_result.get("real_world_task", "Perform immediate physical maintenance."),
        care_tips=parsed_result.get("care_tips") or ["Maintain balanced soil and light."],
        spoken_summary=parsed_result.get("spoken_summary", "Diagnosis complete. Put your phone away and get back to gardening.")
    )

    elapsed_time = round(time.time() - start_time, 2)

    # Attach performance and privacy metadata
    standard_response["meta"] = {
        "engine": ai_engine_used,
        "processing_time_seconds": elapsed_time,
        "screen_time_target_met": elapsed_time < 10.0,
        "offline_local": True,
        "cloud_data_sent": False
    }

    return jsonify(standard_response), 200


if __name__ == "__main__":
    # Ensure ChromaDB is seeded on startup
    get_chroma_collection()

    port = int(os.environ.get("PORT", 5000))
    print("\n" + "=" * 65)
    print("🌿 Soil & Compost Doctor is running!")
    print(f"📍 Local Web App: http://127.0.0.1:{port}")
    print("🌱 100% Offline | Open-Source AI | Screen Time < 10s")
    print("=" * 65 + "\n")
    app.run(host="0.0.0.0", port=port, debug=False)
