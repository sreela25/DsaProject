🥗 Food Ingredient & Allergy Management System
A DSA Case Study using a custom Python Hypergraph.

💡 Why a Hypergraph?
Standard graphs struggle to represent recipes because a single food item inherently connects multiple ingredients simultaneously. 
To solve this efficiently, we built a custom Hypergraph from scratch in Python, treating ingredients as vertices and foods as hyperedges.

---

🏗️ Project Structure
hypergraph.py — Core Hypergraph ADT, reverse incidence indexing, and invariant validation.
food_database.py — CRUD operations, search, and an index-optimized similarity engine.
allergy_checker.py — Allergen union/intersection queries and safety screening.

---

📂 Project Structure

├── hypergraph.py        # Core Hypergraph ADT & invariant validation
├── food_database.py     # CRUD operations, search, and similarity analytics
├── allergy_checker.py   # Allergy screening, safety checks, and match explanations
└── README.md            # Project documentation
