# 🍲 Food Ingredient & Allergy Management System

*A DSA Case Study using a Custom Python Hypergraph*

## 💡 Project Overview

The **Food Ingredient & Allergy Management System** is a Python-based application that models relationships between foods and their ingredients using a custom Hypergraph Abstract Data Type (ADT).

The system allows users to search for foods by ingredients, check foods against recorded allergens, compare food items, analyse ingredient relationships, and manage the food database.

## 🧠 Why a Hypergraph?

In a conventional graph, an edge connects two vertices. However, a food item can contain multiple ingredients simultaneously.

A **hypergraph** allows a single hyperedge to connect any number of vertices, making it suitable for representing food–ingredient relationships.

In our model:

- **Vertices:** Unique ingredients, such as Wheat, Milk, Egg and Cheese.
- **Hyperedges:** Food items, each connecting all the ingredients it contains.
- **Incidence index:** Maps each ingredient to the foods containing it, enabling efficient reverse lookups.

For example:

- Pizza = {Wheat, Milk, Cheese, Tomato}
- Pasta = {Wheat, Egg, Cheese, Tomato}
- Cake = {Wheat, Egg, Milk, Butter}

The shared ingredients allow the system to identify related foods and support ingredient-based queries.

## ✨ Key Features

- **Custom Hypergraph ADT:** Manages ingredient vertices and food hyperedges.
- **Reverse Incidence Indexing:** Retrieves foods associated with a given ingredient.
- **Food Database Management:** Supports adding, updating, deleting and searching food items.
- **Ingredient-Based Search:** Supports ANY, ALL and EXACT matching modes.
- **Allergy Screening:** Identifies foods containing recorded allergens.
- **Food Comparison:** Finds shared ingredients between food items.
- **Similarity Analysis:** Uses Jaccard similarity to measure ingredient overlap.
- **Ingredient Analytics:** Analyses ingredient frequency and relationships.
- **Invariant Validation:** Checks consistency between the hypergraph representation and its indexes.

## 📁 Project Structure

```text
DsaProject/
│
├── hypergraph.py
│   └── Core Hypergraph ADT, incidence indexing
│       and invariant validation
│
├── food_database.py
│   └── Food CRUD operations, search,
│       comparison and similarity analytics
│
├── allergy_checker.py
│   └── Allergen screening, ingredient matching,
│       safety checks and match explanations
│
├── main.py
│   └── Main menu and integration of modules
│
├── test_project.py
│   └── Automated tests, if included in the repository
│
└── README.md
    └── Project documentation
```

## ⚙️ Implementation Details

### 1. Hypergraph ADT — `hypergraph.py`

Implements the core data structure.

Responsibilities include:
- Maintaining unique ingredient vertices.
- Representing each food as a hyperedge.
- Maintaining the reverse incidence index.
- Adding and deleting vertices or food hyperedges.
- Validating structural invariants.

### 2. Food Database — `food_database.py`

Provides operations on the food collection.

Responsibilities include:
- Adding and updating food records.
- Removing food items.
- Searching for foods by name or ingredients.
- Finding shared ingredients.
- Identifying related foods.
- Calculating ingredient overlap and similarity.

### 3. Allergy Checker — `allergy_checker.py`

Implements ingredient-based screening.

Responsibilities include:
- Finding foods containing any specified ingredient.
- Finding foods containing all specified ingredients.
- Finding foods whose ingredient sets match exactly.
- Identifying foods containing recorded allergens.
- Providing explanations for matching results.

### 4. Main Application — `main.py`

Provides the user-facing interface and integrates the hypergraph, database and allergy-checking modules.

## 🔍 Ingredient Matching Modes

| Mode | Description |
|---|---|
| ANY | Returns foods containing at least one of the specified ingredients. |
| ALL | Returns foods containing every specified ingredient. |
| EXACT | Returns foods whose ingredient sets match the specified set exactly. |

## 📐 Time Complexity Analysis

Let:

- \(V\) = number of unique ingredient vertices.
- \(F\) = number of food hyperedges.
- \(I\) = total number of ingredient–food relationships.
- \(k\) = number of ingredients in a food.
- \(r_x\) = number of foods containing ingredient \(x\).

The following are expected bounds for the described set/dictionary representation. Exact complexity depends on the implementation of each operation.

| Operation | Expected Time Complexity |
|---|---|
| Ingredient membership check | \(O(1)\) |
| Add a food with \(k\) ingredients | \(O(k)\) |
| Retrieve all foods containing ingredient \(x\) | \(O(r_x)\) |
| Compare foods with \(a\) and \(b\) ingredients | \(O(a+b)\) |
| Scan all foods | \(O(F)\) |
| Traverse the complete representation | \(O(V+F+I)\) |

Python set and dictionary operations generally have expected constant-time membership or key lookup. Operations involving multiple ingredients, foods or index updates require additional time proportional to the elements processed.

These bounds should be checked against the actual implementation, especially for deletion and similarity calculations.

## 🚀 How to Run the Project

### Prerequisites

- Python 3.10 or a compatible Python version.
- Git, if cloning the repository.

### Step 1: Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Replace the placeholder with your repository's actual URL.

### Step 2: Open the project directory

```bash
cd DsaProject
```

### Step 3: Run the application

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

Follow the menu prompts to explore the available features.

### Step 4: Run automated tests

If `test_project.py` is present and uses Python's built-in `unittest` framework, run:

```bash
python -m unittest -v
```

## 🧪 Testing

The project should be tested for:

- Correct ingredient and food insertion.
- Food updates and deletion.
- Ingredient-based matching.
- Allergen detection.
- Shared-ingredient and similarity calculations.
- Missing food or ingredient searches.
- Consistency of the incidence index after updates and deletions.
- Invalid input and edge cases.

## ⚠️ Limitations

- Results depend on the accuracy and completeness of the stored food ingredients.
- The system cannot independently verify product labels or detect undeclared ingredients.
- Cross-contamination and preparation conditions are not automatically evaluated.
- Allergy screening results are informational and **must not be treated as a guarantee of medical safety**.

## 🔮 Future Enhancements

- Import ingredient information from verified product labels.
- Add a graphical user interface.
- Support ingredient quantities and recipe-level analysis.
- Store food data persistently in a database.
- Add user profiles for managing individual ingredient restrictions.
- Improve validation and reporting for incomplete ingredient information.

## 👥 Team Collaboration

This project was developed collaboratively using GitHub. Team members contributed to the implementation, testing, debugging and integration of the project modules.

The repository's commit history records changes made during development.

## 🎓 Academic Context

**Project Type:** Data Structures and Algorithms Case Study

**Primary Data Structure:** Custom Hypergraph ADT

**Programming Language:** Python

**Application Domain:** Food ingredient management and allergen screening

---

*This project demonstrates how a specialised data structure can model real-world relationships and support efficient data retrieval and analysis.*
