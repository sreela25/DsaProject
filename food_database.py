
from collections import Counter
from hypergraph import HyperGraph


class FoodDatabase:
    def __init__(self, hypergraph):
        self.graph = hypergraph

    # 1. Add a new food or update an existing food.
    def add_or_update_food(self, food, ingredients):
        return self.graph.add_food(food, ingredients)

    # 2. Remove a food from the database.
    def remove_food(self, food):
        return self.graph.remove_food(food)

    # 3. Search foods by name.
    def search_food(self, search_term):
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")

        search_term = search_term.strip().casefold()

        if not search_term:
            raise ValueError("Search term cannot be empty.")

        return {
            food: self.graph.get_ingredients_for_food(food)
            for food in self.graph.hyperedges
            if search_term in food
        }

    # 4. Find ingredients shared by two foods.
    def get_shared_ingredients(self, food1, food2):
        ingredients1 = self.graph.get_ingredients_for_food(food1)
        ingredients2 = self.graph.get_ingredients_for_food(food2)

        return ingredients1.intersection(ingredients2)

    # 5. Find foods sharing ingredients with a given food.
    # Uses the reverse incidence index instead of scanning all foods.
    def find_related_foods(self, food):
        ingredients = self.graph.get_ingredients_for_food(food)

        if not ingredients:
            return {}

        related = {}

        for ingredient in ingredients:
            foods = self.graph.get_foods_for_ingredient(ingredient)

            for other_food in foods:
                if other_food != food:
                    related.setdefault(other_food, set()).add(ingredient)

        return related

    # 6. Rank foods by ingredient similarity.
    # Jaccard similarity = shared ingredients / total distinct ingredients.
    def find_similar_foods(self, food, limit=5):
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise ValueError("Limit must be a positive integer.")

        target_ingredients = self.graph.get_ingredients_for_food(food)

        if not target_ingredients:
            return []
        candidates=set()
        for ingredient in target_ingredients:
            foods=self.graph.get_foods_for_ingredient(ingredient)
            candidates.update(foods)

        candidates.discard(food)
        similarities = []

        for other_food in candidates:      
            other_ingredients = self.graph.get_ingredients_for_food(other_food)
            shared = target_ingredients.intersection(other_ingredients)
            combined = target_ingredients.union(other_ingredients)

            if combined:
                score = len(shared) / len(combined)
                if shared:
                    similarities.append(
                        (other_food, round(score, 3), shared)
                    )
        similarities.sort(key=lambda item: item[1], reverse=True)

        return similarities[:limit]

    # 7. Count how many foods contain each ingredient.
    def get_most_common_ingredients(self, limit=5):
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise ValueError("Limit must be a positive integer.")

        counts = Counter({
            ingredient: len(foods)
            for ingredient, foods in self.graph.incidence.items()
        })

        return counts.most_common(limit)

    # 8. Produce an ingredient overlap report.
    def get_ingredient_overlap_report(self):
        report = {}

        for ingredient, foods in self.graph.incidence.items():
            if len(foods) > 1:
                report[ingredient] = sorted(foods)

        return report
