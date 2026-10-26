from collections import Counter


class FoodDatabase:
    def __init__(self, graph):
        self.graph = graph

    # Adds a food or updates its ingredients.
    # Time: Depends on the number of ingredients.
    def add_or_update_food(self, food, ingredients):
        return self.graph.add_food(food, ingredients)

    # Removes a food hyperedge.
    # Time: O(k), where k is the number of ingredients in that food.
    def remove_food(self, food):
        return self.graph.remove_food(food)

    # Checks whether a food exists by its exact name.
    # Time: O(n) for name cleanup, then O(1) average lookup.
    def search_food(self, food):
        return self.graph.contains_food(food)

    # Returns the ingredients shared by two foods.
    # Time: O(k1 + k2) to retrieve and compare the ingredient sets.
    def get_shared_ingredients(self, food1, food2):
        ingredients1 = self.graph.get_ingredients_for_food(food1)
        ingredients2 = self.graph.get_ingredients_for_food(food2)
        return ingredients1 & ingredients2

    # Finds foods sharing at least one ingredient with the selected food.
    # Time: Depends on the incidence sets visited.
    def find_related_foods(self, food):
        food = self.graph._normalize_name(food)
        if food not in self.graph.hyperedges:
            return {}

        ingredients = self.graph.get_ingredients_for_food(food)
        related = {}

        for ingredient in ingredients:
            for other_food in self.graph.get_foods_for_ingredient(ingredient):
                if other_food != food:
                    related.setdefault(other_food, set()).add(ingredient)

        return related

    # Ranks foods by Jaccard similarity using only foods that share ingredients.
    # Time: Depends on candidates and sorting; worst case can approach O(F log F + I).
    def find_similar_foods(self, food, limit=5):
        food = self.graph._normalize_name(food)
        target = self.graph.get_ingredients_for_food(food)
        if not target:
            return []

        candidates = set()
        for ingredient in target:
            candidates.update(self.graph.get_foods_for_ingredient(ingredient))
        candidates.discard(food)

        results = []
        for other_food in candidates:
            other = self.graph.get_ingredients_for_food(other_food)
            shared = target & other
            if shared:
                score = len(shared) / len(target | other)
                results.append((other_food, round(score, 3), shared))

        results.sort(key=lambda item: item[1], reverse=True)
        return results[:max(0, limit)]

    # Counts how many foods contain each ingredient.
    # Time: O(I + V log V) as a general upper bound including sorting.
    def get_most_common_ingredients(self, limit=10):
        counts = Counter()
        for ingredients in self.graph.hyperedges.values():
            counts.update(ingredients)
        return counts.most_common(max(0, limit))

    # Finds ingredient pairs that occur together in at least two foods.
    # Time: O(V^2 * D) in the worst case, where D is set-intersection cost.
    def get_ingredient_overlap_report(self):
        ingredients = sorted(self.graph.incidence)
        report = {}

        for i, ingredient1 in enumerate(ingredients):
            for ingredient2 in ingredients[i + 1:]:
                foods = self.graph.incidence[ingredient1] & self.graph.incidence[ingredient2]
                if len(foods) >= 2:
                    report[(ingredient1, ingredient2)] = sorted(foods)

        return report
