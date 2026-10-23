
class HyperGraph:
    """
    Hypergraph ADT for the Food Ingredient Allergy Checker.
    Vertices:
        Ingredients
    Hyperedges:
        Food items connected to multiple ingredients.
    Incidence index:
        Ingredient -> set of foods containing that ingredient.
    """

    def __init__(self):
        self.vertices = set()
        self.hyperedges = {}
        self.incidence = {}

    # --------------------------------------------------
    # VERTEX OPERATIONS
    # --------------------------------------------------

    def add_ingredient(self, ingredient):
        """Add an ingredient vertex."""
        if not isinstance(ingredient, str):
            raise TypeError("Ingredient must be a string.")
        ingredient = ingredient.strip().casefold()

        if not ingredient:
            raise ValueError("Ingredient cannot be empty.")

        if ingredient in self.vertices:
            return False

        self.vertices.add(ingredient)
        self.incidence[ingredient] = set()
        return True

    def remove_ingredient(self, ingredient):
        """
        Remove an ingredient vertex and its incidences.
        The ingredient is also removed from every food
        hyperedge that contains it.
        """

        ingredient = self._normalize_name(ingredient)
        if ingredient not in self.vertices:
            return False

        affected_foods = list(self.incidence[ingredient])

        for food in affected_foods:
            self.hyperedges[food].remove(ingredient)
        del self.incidence[ingredient]
        self.vertices.remove(ingredient)

        return True

    # --------------------------------------------------
    # HYPEREDGE OPERATIONS
    # --------------------------------------------------

    def add_food(self, food, ingredients):
        """
        Add a food hyperedge containing multiple ingredients.

        If the food already exists, replace its ingredient
        set and update the reverse incidence index.

        Returns True when added or updated.
        """

        if not isinstance(food, str):
            raise TypeError("Food name must be a string.")
        food = food.strip().casefold()

        if not food:
            raise ValueError("Food name cannot be empty.")

        if isinstance(ingredients, str):
            raise TypeError(
                "Ingredients must be an iterable of names, "
                "such as ['milk', 'wheat']."
            )

        try:
            ingredient_list = list(ingredients)
        except TypeError:
            raise TypeError("Ingredients must be iterable.")

        if not ingredient_list:
            raise ValueError(
                "A food must contain at least one ingredient."
            )

        normalized_ingredients = set()

        for ingredient in ingredient_list:
            normalized_ingredients.add(
                self._normalize_name(ingredient)
            )

        # Ensure all ingredient vertices exist.
        for ingredient in normalized_ingredients:
            self.add_ingredient(ingredient)

        # Remove old incidences if this food already exists.
        if food in self.hyperedges:
            old_ingredients = self.hyperedges[food]

            for ingredient in old_ingredients:
                self.incidence[ingredient].discard(food)

        # Store the new hyperedge.
        self.hyperedges[food] = normalized_ingredients

        # Update reverse incidence relationships.
        for ingredient in normalized_ingredients:
            self.incidence[ingredient].add(food)

        return True

    def remove_food(self, food):
        """Remove a food hyperedge and all its incidences."""

        food = self._normalize_name(food)

        if food not in self.hyperedges:
            return False

        ingredients = self.hyperedges.pop(food)
        for ingredient in ingredients:
            self.incidence[ingredient].discard(food)

        return True

    # --------------------------------------------------
    # HYPERGRAPH TRAVERSAL
    # --------------------------------------------------

    def get_foods_for_ingredient(self, ingredient):
        """
        Return foods containing an ingredient.
        Uses the reverse incidence index.
        """

        ingredient = self._normalize_name(ingredient)

        if ingredient not in self.vertices:
            return set()

        return set(self.incidence[ingredient])

    def get_ingredients_for_food(self, food):
        """Return the ingredients belonging to a food."""

        food = self._normalize_name(food)

        if food not in self.hyperedges:
            return set()

        return set(self.hyperedges[food])

    def get_common_foods(self, ingredient1, ingredient2):
        """Find foods containing both specified ingredients."""

        ingredient1 = self._normalize_name(ingredient1)
        ingredient2 = self._normalize_name(ingredient2)
        if (ingredient1 not in self.vertices or
                ingredient2 not in self.vertices):
            return set()

        # Start with the smaller incidence set.
        foods1 = self.incidence[ingredient1]
        foods2 = self.incidence[ingredient2]

        if len(foods1) > len(foods2):
            foods1, foods2 = foods2, foods1

        return {
            food for food in foods1
            if food in foods2
        }

    
    def count_foods_for_ingredient(self, ingredient):
        ingredient = self._normalize_name(ingredient)

        if ingredient not in self.vertices:
            return 0

        return len(self.incidence[ingredient])

    def contains_food(self, food):
        food = self._normalize_name(food)
        return food in self.hyperedges
    # --------------------------------------------------
    # INFORMATION AND DISPLAY
    # --------------------------------------------------

    def get_vertex_count(self):
        """Return the number of ingredient vertices."""

        return len(set(self.vertices))

    def get_hyperedge_count(self):
        """Return the number of food hyperedges."""
        count = len(self.hyperedges)
        return count

    def get_incidence_count(self):
        """Return the total number of ingredient-food links."""

        return sum(
            len(ingredients)
            for ingredients in self.hyperedges.values()
        )

    def display_hypergraph(self):
        """Display foods and their ingredient hyperedges."""

        print("\n========== HYPERGRAPH ==========")

        if not self.hyperedges:
            print("No food hyperedges available.")
            return

        for food in sorted(self.hyperedges):
            ingredients = sorted(self.hyperedges[food])
           
            print(f"{food.title()} -> {{{', '.join(ingredients)}}}")

        print("================================")

    def display_incidence_index(self):
        """Display each ingredient and its associated foods."""

        print("\n====== INCIDENCE INDEX ======")

        if not self.incidence:
            print("No ingredient vertices available.")
            return
        for ingredient in sorted(self.incidence):
            foods = sorted(self.incidence[ingredient])
            food_text = ", ".join(f.title() for f in foods)
            print(f"{ingredient.title():<15} -> {food_text} ({len(foods)} foods)")

        print("=============================")
        
    
    def display_statistics(self):
        """Display structural statistics of the hypergraph."""
        print("\n====== HYPERGRAPH STATISTICS ======")
        print(f"Ingredient Vertices (V): {self.get_vertex_count()}")
        print(f"Food Hyperedges (E):     {self.get_hyperedge_count()}")
        print(f"Total Incidence Links:   {self.get_incidence_count()}")
        print(f"Valid Structure:         {self.validate_invariants()}")
        print("===================================")

    # --------------------------------------------------
    # INTERNAL VALIDATION
    # --------------------------------------------------

    @staticmethod
    def _normalize_name(name):
        """Validate and standardize ingredient/food names."""

        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        name = name.strip().casefold()
        if not name:
            raise ValueError("Name cannot be empty.")
        return name

    def validate_invariants(self):
        """
        Verify that vertices, hyperedges and incidence
        relationships are consistent.
        """

        # Every ingredient in every food must be a vertex.
        for ingredients in self.hyperedges.values():
            if not ingredients.issubset(self.vertices):
                return False

        # Reconstruct expected incidence relationships.
        expected_incidence = {
            ingredient: set()
            for ingredient in self.vertices
        }

        for food, ingredients in self.hyperedges.items():
            for ingredient in ingredients:
                expected_incidence[ingredient].add(food)

        return expected_incidence == self.incidence


