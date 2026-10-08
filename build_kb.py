"""
build_kb.py - Seed Local ChromaDB Vector Database
===================================================
Project: Soil & Compost Doctor (Hacktoberfest "Touch Grass" Challenge)
Author: Student Builder
Description:
  Initializes a persistent local ChromaDB collection (`soil_compost_kb`)
  and populates it with open agricultural extension guidelines for
  leaf health, soil deficiencies, and compost pile management.
  Everything runs 100% locally and offline.
"""

import os
import sys
import json

# Ensure UTF-8 output on Windows console
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import chromadb
from chromadb.config import Settings
from embeddings import get_embedding_function

# Path to local persistent ChromaDB directory
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
COLLECTION_NAME = "soil_compost_kb"

# Open Agricultural Extension Dataset
KNOWLEDGE_BASE = [
    # ==========================================
    # CATEGORY: Leaf Health
    # ==========================================
    {
        "id": "leaf_early_blight",
        "category": "Leaf Health",
        "diagnosis": "Early Blight (Alternaria solani)",
        "symptoms": "Dark brown to black spots with concentric rings like a target board on lower, older leaves. Foliage turns yellow around the lesions and drops.",
        "real_world_task": "Prune off all affected lower leaves within 6 inches of the soil immediately and bury them away from your garden or discard in trash (do not compost).",
        "care_tips": [
            "Mulch heavily around the plant base with 2 inches of clean straw to prevent soil spores from splashing up during rain.",
            "Water strictly at the soil base using a watering can or drip hose—never wet the foliage.",
            "Sterilize your pruning shears with rubbing alcohol between cuts."
        ],
        "spoken_summary": "Your plant has Early Blight. Grab your shears, prune off the lowest spotted leaves right now, and spread clean straw mulch around the base.",
        "tags": ["tomato", "potato", "blight", "yellowing", "concentric rings", "fungal", "spots"]
    },
    {
        "id": "leaf_powdery_mildew",
        "category": "Leaf Health",
        "diagnosis": "Powdery Mildew (Fungal Infection)",
        "symptoms": "White to grayish talcum powder-like dusting across the upper surfaces of leaves, stems, and flower buds. Leaves may curl, turn brown, and shrivel.",
        "real_world_task": "Mix 1 tablespoon of baking soda and half a teaspoon of mild dish soap into 1 gallon of water; spray the top and bottom of affected leaves in the early morning sun.",
        "care_tips": [
            "Thin out neighboring branches and suckers to boost airflow and sunlight penetration through the plant canopy.",
            "Ensure plants are not overcrowded in tight garden beds.",
            "Avoid overhead watering late in the afternoon or evening."
        ],
        "spoken_summary": "That white coating is Powdery Mildew. Mix a gentle baking soda water spray, mist the leaves immediately, and prune crowded stems to let morning sunlight in.",
        "tags": ["squash", "cucumber", "zucchini", "white powder", "fuzzy", "mildew", "fungus"]
    },
    {
        "id": "leaf_nitrogen_deficiency",
        "category": "Leaf Health",
        "diagnosis": "Nitrogen Chlorosis (Nitrogen Starvation)",
        "symptoms": "Uniform pale light-green to pale-yellow coloration starting at the oldest bottom leaves, while upper new leaves remain greener but stunted.",
        "real_world_task": "Top-dress the soil around the plant drip line with 2 handfuls of rich compost, worm castings, or organic blood meal, then water it in thoroughly.",
        "care_tips": [
            "Brew compost tea or use diluted fish emulsion for immediate fast-acting root uptake.",
            "Check soil drainage to ensure roots are not rotting from standing water.",
            "Plant nitrogen-fixing cover crops like clover or bush beans next season."
        ],
        "spoken_summary": "Your plant is starving for nitrogen, shown by the pale yellow lower leaves. Top-dress with two handfuls of compost or organic fish fertilizer and water deeply.",
        "tags": ["yellow leaves", "chlorosis", "pale green", "stunted", "nitrogen", "deficiency"]
    },
    {
        "id": "leaf_iron_chlorosis",
        "category": "Leaf Health",
        "diagnosis": "Iron Chlorosis (Interveinal Chlorosis)",
        "symptoms": "Distinct bright yellowing between leaf veins while the veins themselves remain dark green. Primarily manifests on newest top leaves.",
        "real_world_task": "Drench root area with chelated iron foliar spray or apply powdered elemental sulfur to gently lower alkaline soil pH.",
        "care_tips": [
            "Test soil pH—iron is often locked out in soils with pH above 7.2.",
            "Aerate dense soil around the root zone to promote oxygen exchange.",
            "Avoid over-watering, as cold saturated soil severely inhibits iron uptake."
        ],
        "spoken_summary": "Notice the dark green veins on yellow leaves? That is Iron Chlorosis. Apply a chelated iron drench to the roots and check that your soil pH isn't too alkaline.",
        "tags": ["iron deficiency", "green veins yellow leaf", "interveinal", "alkaline soil", "chlorosis"]
    },
    {
        "id": "leaf_blossom_end_rot",
        "category": "Leaf Health",
        "diagnosis": "Blossom End Rot (Calcium Transport Imbalance)",
        "symptoms": "Water-soaked dark sunken leathery patch developing on the bottom (blossom end) of ripening fruits, accompanied by curling foliage.",
        "real_world_task": "Harvest and discard sunken fruits immediately so plant directs energy into healthy new flowers; soak the soil deeply with consistent moisture.",
        "care_tips": [
            "Keep soil consistently moist like a wrung-out sponge—inconsistent watering prevents calcium transport.",
            "Apply a 3-inch layer of organic mulch around root perimeter to regulate soil moisture.",
            "Avoid excessive synthetic high-nitrogen fertilizers that spur foliage overgrowth at the expense of fruit calcium."
        ],
        "spoken_summary": "The dark sunken spot on your fruit is Blossom End Rot. Remove the damaged fruit right away and water your plant deeply on a steady, even schedule.",
        "tags": ["tomato", "pepper", "black bottom", "calcium", "sunken rot", "watering"]
    },
    {
        "id": "leaf_aphid_infestation",
        "category": "Leaf Health",
        "diagnosis": "Aphid Cluster & Honeydew Infestation",
        "symptoms": "Clusters of tiny pear-shaped green, yellow, or black insects grouped on new shoots or leaf undersides. Sticky shiny honeydew residue or black sooty mold present.",
        "real_world_task": "Turn your garden hose to a firm spray nozzle and blast the undersides of the leaves to physically knock the aphids off into the soil.",
        "care_tips": [
            "Spray with organic neem oil or horticultural insecticidal soap in the evening.",
            "Introduce or attract beneficial predatory insects like ladybugs and lacewings.",
            "Companion-plant sweet alyssum, marigolds, and dill to repel pests naturally."
        ],
        "spoken_summary": "You have an aphid cluster on the tender leaves. Blast them with a sharp jet of water from your hose right now, then mist with neem oil at sunset.",
        "tags": ["aphids", "bugs", "sticky leaf", "curled leaves", "pests", "honeydew", "insects"]
    },
    {
        "id": "leaf_rust_fungus",
        "category": "Leaf Health",
        "diagnosis": "Rust Fungus (Pucciniales)",
        "symptoms": "Bright reddish-orange, rust-brown, or yellow pustules bursting through leaf undersides. Leaves turn brittle, dry out, and prematurely drop.",
        "real_world_task": "Gently cut off heavily infected leaves into a plastic bag to prevent spores from blowing, and apply organic sulfur or copper fungicide.",
        "care_tips": [
            "Ensure wide plant spacing for rapid morning leaf drying.",
            "Never splash water on foliage when watering.",
            "Rake and safely discard all fallen autumn leaf litter where fungal spores overwinter."
        ],
        "spoken_summary": "Those bright orange spots are Rust Fungus. Carefully clip the infected leaves into a bag so spores don't spread, and spray with sulfur dust.",
        "tags": ["orange spots", "rust", "pustules", "fungal", "beans", "roses"]
    },

    # ==========================================
    # CATEGORY: Soil Quality
    # ==========================================
    {
        "id": "soil_compacted_clay",
        "category": "Soil Quality",
        "diagnosis": "Compacted Heavy Clay Soil",
        "symptoms": "Dense, brick-hard soil that cracks when dry and forms sticky puddling mud when wet. Hard to push a trowel more than 2 inches deep. Poor root penetration.",
        "real_world_task": "Insert a garden broadfork or digging fork 8 inches deep into the soil bed and gently rock it backward to crack open aeration channels without inverting layers.",
        "care_tips": [
            "Top-dress with a generous 3-inch layer of rich homemade compost and leaf mold; let earthworms incorporate it down.",
            "Never work or walk on clay soil when it is dripping wet.",
            "Plant deep tap-root cover crops like daikon radish to naturally shatter subsoil compaction."
        ],
        "spoken_summary": "Your soil is heavily compacted clay. Take a garden fork, plunge it in to crack the soil open for air, and spread three inches of crumbly compost across the surface.",
        "tags": ["compacted", "clay", "hard soil", "cracked", "puddles", "aeration"]
    },
    {
        "id": "soil_sandy_depleted",
        "category": "Soil Quality",
        "diagnosis": "Dry, Nutrient-Depleted Sandy Soil",
        "symptoms": "Gritty, loose soil that falls apart through fingers. Water drains through almost instantly without retention. Soil feels dry just an hour after watering.",
        "real_world_task": "Blend 3 to 4 shovel loads of mature compost, coconut coir, or aged leaf mold into the top 6 inches of soil to supercharge moisture retention.",
        "care_tips": [
            "Keep soil permanently shielded with 3 inches of wood chip or straw mulch to prevent evaporation.",
            "Incorporate biochar soaked in compost tea for permanent nutrient retention.",
            "Fertilize with slow-release organic granules rather than liquid synthetics that leach away."
        ],
        "spoken_summary": "This soil is gritty, depleted sand that loses moisture instantly. Mix in three big shovels of organic compost and cap it with wood mulch to lock in moisture.",
        "tags": ["sandy", "dry", "loose", "drainage", "nutrient poor", "organic matter"]
    },
    {
        "id": "soil_acidic_low_ph",
        "category": "Soil Quality",
        "diagnosis": "Excessively Acidic Soil (pH below 5.8)",
        "symptoms": "Yellowing foliage despite fertilization, presence of moss or field horsetail, poor seedling germination and root stunting due to aluminum toxicity.",
        "real_world_task": "Sprinkle clean hardwood fireplace ash (1 cup per 10 sq ft) or agricultural garden lime evenly across the garden bed and rake into the top inch.",
        "care_tips": [
            "Use an inexpensive soil test kit to monitor pH upward toward the ideal 6.2 - 6.8 range.",
            "Avoid heavy use of chemical ammonium fertilizers which drive soil pH further down.",
            "Incorporate well-rotted leaf compost to buffer soil biology against extreme acidity."
        ],
        "spoken_summary": "Your soil is overly acidic, which locks up vital nutrients. Spread a light dusting of wood ash or garden lime across the bed and water it in.",
        "tags": ["acidic", "low ph", "moss", "lime", "wood ash", "yellowing"]
    },
    {
        "id": "soil_alkaline_high_ph",
        "category": "Soil Quality",
        "diagnosis": "Alkaline / Chalky Soil (pH above 7.5)",
        "symptoms": "White mineral crust on soil surface, chalky or pale limestone texture, widespread plant yellowing and stunted growth due to micronutrient lockout.",
        "real_world_task": "Work organic elemental sulfur granules or acidic peat moss / pine needle mulch into the top soil layer to gently reduce alkalinity.",
        "care_tips": [
            "Top-dress with rotted oak leaves or pine needle compost.",
            "Feed plants with acid-loving organic fertilizers containing chelated micronutrients.",
            "Use rainwater instead of hard tap water when watering potted beds."
        ],
        "spoken_summary": "This soil has high alkalinity and chalky minerals locking out iron. Work elemental sulfur or pine needle mulch into the top layer to balance the pH.",
        "tags": ["alkaline", "high ph", "chalky", "crust", "sulfur", "limestone"]
    },
    {
        "id": "soil_waterlogged_anaerobic",
        "category": "Soil Quality",
        "diagnosis": "Waterlogged & Anaerobic Garden Bed",
        "symptoms": "Sour or swampy sulfur smell coming from soil. Gray or mottled bluish soil hue. Plant roots are brown, slimy, and decaying with root rot.",
        "real_world_task": "Stop watering immediately; dig shallow diversion drainage trenches along bed edges to channel standing water away from plant roots.",
        "care_tips": [
            "Build raised beds (8 to 12 inches high) if the native water table or clay prevents drainage.",
            "Aerate the perimeter around plants with a hand fork to draw oxygen into root pockets.",
            "Allow the top 2 inches of soil to completely dry out before watering again."
        ],
        "spoken_summary": "Your soil is dangerously waterlogged and suffocating the root system. Stop all watering immediately and dig a quick trench along the bed edge to drain the pool.",
        "tags": ["waterlogged", "muddy", "sour smell", "root rot", "swampy", "drainage"]
    },

    # ==========================================
    # CATEGORY: Compost Status
    # ==========================================
    {
        "id": "compost_anaerobic_smelly",
        "category": "Compost Status",
        "diagnosis": "Anaerobic / Overly Wet Smelly Compost Pile",
        "symptoms": "Foul ammonia or rotten egg sulfur stench. Pile is soggy, dark, slimy, and compacted with little to no oxygen flow inside.",
        "real_world_task": "Add 3 to 4 buckets of dry brown carbon material (dry autumn leaves, shredded cardboard, or straw) and vigorously turn the entire pile with a pitchfork.",
        "care_tips": [
            "Aim for a 3:1 brown-to-green volume ratio in your compost bin.",
            "Cover the pile with a breathable tarp during heavy rainstorms to prevent water saturation.",
            "Keep kitchen food scraps buried deep inside the brown layers, never left exposed on top."
        ],
        "spoken_summary": "Your compost has turned anaerobic and smelly from excess wet greens. Grab your pitchfork, add three buckets of dry brown leaves or shredded cardboard, and turn the pile.",
        "tags": ["smelly compost", "anaerobic", "slimy", "rotten egg", "too wet", "browns", "pitchfork"]
    },
    {
        "id": "compost_dry_stalled",
        "category": "Compost Status",
        "diagnosis": "Dry & Stalled Compost Pile",
        "symptoms": "Pile is cold to the touch with zero decomposition happening. Brittle brown leaves sitting unchanged for months. Moisture level feels bone dry.",
        "real_world_task": "Add fresh green nitrogen materials (fresh lawn grass clippings or vegetable scraps) and spray the pile with a garden hose until it feels like a damp wrung-out sponge.",
        "care_tips": [
            "Turn the pile thoroughly while spraying water so moisture penetrates the dry center.",
            "Maintain pile minimum size of 3x3x3 feet to retain internal microbial warmth.",
            "Mix in a shovel of mature active compost or garden soil to reseed beneficial bacteria."
        ],
        "spoken_summary": "Your compost has stalled and gone cold because it is too dry. Dump in fresh green grass clippings, spray it down with your hose until damp, and mix well.",
        "tags": ["dry compost", "stalled", "cold pile", "no heat", "greens", "nitrogen", "water"]
    },
    {
        "id": "compost_active_hot",
        "category": "Compost Status",
        "diagnosis": "Active Thermophilic Hot Compost Pile",
        "symptoms": "Steam rising when turned. Pile temperature between 130°F and 150°F (55°C - 65°C). Sweet earthy aroma. Material is rapidly breaking down.",
        "real_world_task": "Check internal core temperature with a compost thermometer; turn the outer edges into the center core once temperature begins to drop below 120°F.",
        "care_tips": [
            "Do not turn while temperature is peaking between 140°F and 150°F—this kills weed seeds and pathogens.",
            "Maintain moisture like a wrung-out sponge by adding small splashes of water if core dries.",
            "Celebrate! Your pile is performing at peak biological efficiency."
        ],
        "spoken_summary": "Awesome job! Your compost is in the hot thermophilic stage breaking down weeds and pathogens. Keep the core moist and turn the outer edges in next week.",
        "tags": ["hot compost", "active", "steaming", "thermophilic", "temperature", "healthy"]
    },
    {
        "id": "compost_finished_humus",
        "category": "Compost Status",
        "diagnosis": "Finished Cured Compost ('Black Gold')",
        "symptoms": "Deep dark rich brown or black crumbly texture. Smells wonderfully earthy like a fresh forest floor after rain. No original food or plant scraps visible.",
        "real_world_task": "Sift compost through a 1/2-inch wire mesh screen to filter out large twigs, and spread a 1 to 2-inch layer across your garden vegetable beds or tree rings.",
        "care_tips": [
            "Throw any unsifted chunky wood pieces back into the new compost pile as inoculant.",
            "Top-dress house plants with 1/2 inch of this finished compost for natural fertilization.",
            "Store cured compost in a covered bin to keep rain from leaching out valuable nutrients."
        ],
        "spoken_summary": "You have pure Black Gold! Your compost is completely finished. Sift out large twigs and spread a rich two-inch layer across your garden beds right now.",
        "tags": ["finished compost", "black gold", "humus", "cured", "ready", "dark crumbly", "forest smell"]
    },
    {
        "id": "compost_critter_pests",
        "category": "Compost Status",
        "diagnosis": "Pest-Attracting Compost Pile (Flies / Rodents)",
        "symptoms": "Swarm of fruit flies, houseflies, maggots, or rodent burrow holes around the compost bin edges. Unpleasant food scrap odor.",
        "real_world_task": "Cap the entire top of the compost pile with a solid 4-inch blanket of dry leaves, wood shavings, or cardboard to seal in odors and block flies.",
        "care_tips": [
            "Never add meat, bones, cheese, oil, or pet feces to backyard compost bins.",
            "Always bury new kitchen vegetable scraps at least 10 inches under the compost core.",
            "Wrap wire mesh (hardware cloth) under open-bottom wooden bins to deter digging rodents."
        ],
        "spoken_summary": "Pests are smelling exposed food scraps. Cover the pile with a thick four-inch blanket of dry brown leaves immediately to seal off odors and flies.",
        "tags": ["flies", "maggots", "rats", "rodents", "food scraps", "pests", "smell"]
    }
]

def build_vector_database():
    """Initializes ChromaDB and stores the knowledge base."""
    print("=" * 65)
    print("[+] Soil & Compost Doctor: Seeding ChromaDB Knowledge Base")
    print("=" * 65)
    print(f"Target DB Directory: {DB_DIR}")

    os.makedirs(DB_DIR, exist_ok=True)

    # Initialize persistent ChromaDB client
    client = chromadb.PersistentClient(path=DB_DIR)

    # Delete existing collection if it exists to ensure fresh seed
    try:
        existing = [c.name for c in client.list_collections()]
        if COLLECTION_NAME in existing:
            print(f"[*] Resetting existing '{COLLECTION_NAME}' collection...")
            client.delete_collection(COLLECTION_NAME)
    except Exception as e:
        print(f"[!] Note during reset: {e}")

    # Create collection with 100% offline embedding function
    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"description": "Agricultural extension guidelines for leaves, soil, and compost."}
    )

    ids = []
    documents = []
    metadatas = []

    for item in KNOWLEDGE_BASE:
        # Build composite document string for rich embedding search
        doc_text = (
            f"Category: {item['category']}\n"
            f"Diagnosis: {item['diagnosis']}\n"
            f"Visual Symptoms & Signs: {item['symptoms']}\n"
            f"Immediate Outdoor Task: {item['real_world_task']}\n"
            f"Care Tips: {' '.join(item['care_tips'])}\n"
            f"Tags: {', '.join(item['tags'])}"
        )

        ids.append(item["id"])
        documents.append(doc_text)
        metadatas.append({
            "category": item["category"],
            "diagnosis": item["diagnosis"],
            "symptoms": item["symptoms"],
            "real_world_task": item["real_world_task"],
            "care_tips_json": json.dumps(item["care_tips"]),
            "spoken_summary": item["spoken_summary"],
            "tags_str": ", ".join(item["tags"])
        })

    # Add all records to collection
    print(f"[*] Indexing {len(ids)} agricultural knowledge records...")
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    count = collection.count()
    print(f"[+] Successfully seeded ChromaDB! Total records in '{COLLECTION_NAME}': {count}")
    print("=" * 65)
    return count

if __name__ == "__main__":
    try:
        build_vector_database()
    except Exception as ex:
        print(f"[ERROR] Failed to seed ChromaDB: {ex}", file=sys.stderr)
        sys.exit(1)
