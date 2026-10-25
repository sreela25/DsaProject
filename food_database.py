
from collections import Counter


class FoodDatabase:
    def __init__(self, graph):
        self.graph = graph

    # Time Complexity: O(n + k)
    # Adds a new food or updates its ingredients in the hypergraph.
    def add_or_update_food(self, food, ingredients):
        return self.graph.add_food(food, ingredients)

    # Time Complexity: O(n + k)
    # Removes a food and its ingredient links from the graph.
    def remove_food(self, food):
        return self.graph.remove_food(food)

    # Time Complexity: O(n)
    # Checks whether a food with the given name exists.
    def search_food(self, food):
        return self.graph.contains_food(food)

    # Time Complexity: O(n + k1 + k2)
    # Gets both ingredient sets and finds the ingredients they share.
    def get_shared_ingredients(self, food1, food2):
        ingredients1 = self.graph.get_ingredients_for_food(food1)
        ingredients2 = self.graph.get_ingredients_for_food(food2)

        return ingredients1 & ingredients2

    # Time Complexity: O(n + I)
    # Finds other foods that contain at least one ingredient used in the selected food.
    def find_related_foods(self, food):
        ingredients = self.graph.get_ingredients_for_food(food)
        related = {}

        for ingredient in ingredients:
            foods = self.graph.get_foods_for_ingredient(ingredient)

            for other_food in foods:
                if other_food != food:
                    if other_food not in related:
                        related[other_food] = set()

                    related[other_food].add(ingredient)

        return related

    # Time Complexity: O(n + I + C*k)
    # Checks only foods that share at least one ingredient, calculates their Jaccard similarity, and returns the most similar foods first.
    def find_similar_foods(self, food, limit=5):
        target_ingredients = (
            self.graph.get_ingredients_for_food(food)
        )

        if not target_ingredients:
            return []

        candidates = set()

        for ingredient in target_ingredients:
            foods = self.graph.get_foods_for_ingredient(ingredient)
            candidates.update(foods)

        candidates.discard(food)
        similarities = []

        for other_food in candidates:
            other_ingredients = (
                self.graph.get_ingredients_for_food(other_food)
            )

            shared = target_ingredients.intersection(other_ingredients)
            combined = target_ingredients.union(other_ingredients)

            if combined:
                score = len(shared) / len(combined)

                if shared:
                    similarities.append(
                        (other_food, round(score, 3), shared)
                    )

        similarities.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return similarities[:limit]

    # Time Complexity: O(I + V log V)
    # Counts how often each ingredient appears and sorts the ingredients by frequency.
    def get_most_common_ingredients(self, limit=10):
        ingredient_counts = Counter()

        for ingredients in self.graph.hyperedges.values():
            ingredient_counts.update(ingredients)

        return ingredient_counts.most_common(limit)

    # Time Complexity: O(F log F + I)
    # Groups foods by shared ingredients and reports ingredient pairs that appear together in at least two foods.
    def get_ingredient_overlap_report(self):
        ingredient_foods = self.graph.incidence
        overlap_report = {}

        ingredients = sorted(ingredient_foods)

        for i in range(len(ingredients)):
            ingredient1 = ingredients[i]

            for j in range(i + 1, len(ingredients)):
                ingredient2 = ingredients[j]

                foods = (
                    ingredient_foods[ingredient1]
                    & ingredient_foods[ingredient2]
                )

                if len(foods) >= 2:
                    pair = (ingredient1, ingredient2)
                    overlap_report[pair] = sorted(foods)

        return overlap_report
