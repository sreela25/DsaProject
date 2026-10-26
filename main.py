
from hypergraph import HyperGraph
from food_database import FoodDatabase
from allergy_checker import AllergyChecker


# Reads comma-separated names from the user.
# Time Complexity: O(n), where n is the input length.
def read_names(prompt):
    values = input(prompt).strip()

    if not values:
        return []

    return [
        value.strip()
        for value in values.split(",")
        if value.strip()
    ]


# Displays food names in alphabetical order.
# Time Complexity: O(F log F), where F is the number of foods.
def display_foods(foods):
    if not foods:
        print("No matching foods found.")
        return

    for food in sorted(foods):
        print("-", food.title())


# Displays the available operations.
# Time Complexity: O(1), since the menu size is fixed.
def display_menu():
    print("\n" + "=" * 55)
    print("       FOOD INGREDIENT ALLERGY CHECKER")
    print("=" * 55)
    print("1. Display food hypergraph")
    print("2. Display ingredient incidence index")
    print("3. Find foods containing at least one listed allergen")
    print("4. Find foods containing all specified ingredients")
    print("5. Find foods with no recorded allergen matches")
    print("6. Explain ingredient matches")
    print("7. Add or update a food")
    print("8. Remove a food")
    print("9. Find food by exact name")
    print("10. Compare ingredients of two foods")
    print("11. Find foods sharing ingredients")
    print("12. Rank foods by ingredient similarity")
    print("13. Show most frequently used ingredients")
    print("14. Show ingredient pairs shared by multiple foods")
    print("15. Show allergen matching summary")
    print("16. Show hypergraph statistics")
    print("0. Exit")
    print("=" * 55)


# Time Complexity: Depends on the selected operation.
def main():
    graph = HyperGraph()

    # Sample data for testing the application.
    graph.add_food(
        "Pizza",
        ["Wheat", "Milk", "Cheese", "Tomato"]
    )
    graph.add_food(
        "Pasta",
        ["Wheat", "Egg", "Cheese", "Tomato"]
    )
    graph.add_food(
        "Cake",
        ["Wheat", "Egg", "Milk", "Butter"]
    )
    graph.add_food(
        "Fruit Bowl",
        ["Apple", "Banana", "Grapes"]
    )

    database = FoodDatabase(graph)
    checker = AllergyChecker(graph)

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        try:
            # Displays every food and its ingredients.
            # Time Complexity: Depends on the foods and ingredients displayed.
            if choice == "1":
                graph.display_hypergraph()

            # Shows which foods contain each ingredient.
            # Time Complexity: Depends on the index size and sorting.
            elif choice == "2":
                graph.display_incidence_index()

            # Finds foods containing one or more listed allergens.
            # Time Complexity: Depends on the incidence sets visited.
            elif choice == "3":
                allergens = read_names(
                    "Enter allergens separated by commas: "
                )

                if not allergens:
                    print("Please enter at least one allergen.")
                    continue

                result = checker.find_foods_with_any_allergen(allergens)

                print("\nFoods containing at least one listed allergen:")
                display_foods(result)

            # Finds foods that contain every entered ingredient.
            # Time Complexity: Depends on the sizes of the incidence sets.
            elif choice == "4":
                ingredients = read_names(
                    "Enter required ingredients separated by commas: "
                )

                if not ingredients:
                    print("Please enter at least one ingredient.")
                    continue

                result = checker.find_foods_with_all_ingredients(
                    ingredients
                )

                print("\nFoods containing all specified ingredients:")
                display_foods(result)

            # Lists foods with no recorded matches for the allergens.
            # Time Complexity: O(F + I) in the general case.
            elif choice == "5":
                allergens = read_names(
                    "Enter allergens to exclude, separated by commas: "
                )

                result = checker.find_safe_candidates(allergens)

                print("\nFoods with no recorded allergen matches:")
                display_foods(result)
                print(
                    "\nNote: This result does not guarantee medical safety "
                    "or rule out cross-contamination."
                )

            # Explains which requested ingredients occur in matching foods.
            # Uses explain_food_matches() from AllergyChecker.
            elif choice == "6":
                ingredients = read_names(
                    "Enter ingredients to check, separated by commas: "
                )

                if not ingredients:
                    print("Please enter at least one ingredient.")
                    continue

                reports = checker.explain_food_matches(ingredients)

                if not reports:
                    print("No foods contain all the specified ingredients.")
                else:
                    print("\nIngredient Match Explanation")

                    for report in reports:
                        print("\nFood:", report["food"].title())
                        print("Matching ingredients:", report["matches"])
                        print("Explanation:", report["message"])

            # Adds a food or updates its ingredients.
            # Time Complexity: O(k) graph operations for a new food, excluding name-processing costs.
            elif choice == "7":
                food = input("Enter food name: ").strip()
                ingredients = read_names(
                    "Enter ingredients separated by commas: "
                )

                if not food or not ingredients:
                    print("Food name and ingredients are required.")
                    continue

                database.add_or_update_food(food, ingredients)
                print("Food added or updated successfully.")

            # Removes a food and its ingredient links.
            # Time Complexity: O(k), excluding name normalization.
            elif choice == "8":
                food = input("Enter food name to remove: ").strip()

                if database.remove_food(food):
                    print("Food removed successfully.")
                else:
                    print("Food not found.")

            # Searches for an exact food name and displays its ingredients.
            # Time Complexity: O(n + k), including normalization and copying.
            elif choice == "9":
                food = input("Enter exact food name: ").strip()

                if database.search_food(food):
                    ingredients = graph.get_ingredients_for_food(food)

                    print("\nFood:", food.title())
                    print("Ingredients:", ", ".join(sorted(ingredients)))
                else:
                    print("Food not found. Check the spelling and try again.")

            # Compares two foods and lists their common ingredients.
            # Time Complexity: O(k1 + k2) to retrieve and compare the sets.
            elif choice == "10":
                food1 = input("Enter first food: ").strip()
                food2 = input("Enter second food: ").strip()

                if (not database.search_food(food1) or
                        not database.search_food(food2)):
                    print("One or both foods were not found.")
                    continue

                shared = database.get_shared_ingredients(food1, food2)

                if shared:
                    print("\nShared ingredients:", ", ".join(sorted(shared)))
                else:
                    print("These foods have no shared ingredients.")

            # Finds other foods that share ingredients with the selected food.
            # Time Complexity: Depends on the incidence sets visited.
            elif choice == "11":
                food = input("Enter food name: ").strip()

                if not database.search_food(food):
                    print("Food not found.")
                    continue

                results = database.find_related_foods(food)

                if not results:
                    print("No other foods share its ingredients.")
                else:
                    print("\nRelated foods:")

                    for related_food, ingredients in sorted(results.items()):
                        print(
                            related_food.title(),
                            "- Shared ingredients:",
                            ", ".join(sorted(ingredients))
                        )

            # Ranks foods by Jaccard similarity of their ingredients.
            # Time Complexity: Depends on candidate foods and sorting.
            elif choice == "12":
                food = input("Enter food name: ").strip()

                if not database.search_food(food):
                    print("Food not found.")
                    continue

                results = database.find_similar_foods(food)

                if not results:
                    print("No similar foods found.")
                else:
                    print("\nFoods ranked by ingredient similarity:")

                    for name, score, shared in results:
                        print(
                            name.title(),
                            "| Similarity:", score,
                            "| Shared ingredients:",
                            ", ".join(sorted(shared))
                        )

            # Displays ingredients ranked by how many foods contain them.
            # Time Complexity: O(I + V log V) as a general upper bound.
            elif choice == "13":
                limit = int(
                    input("How many ingredients should be displayed? ")
                )

                if limit < 1:
                    print("Please enter a number greater than zero.")
                    continue

                results = database.get_most_common_ingredients(limit)

                if not results:
                    print("No ingredients available.")
                else:
                    print("\nMost frequently used ingredients:")

                    for ingredient, count in results:
                        print(
                            ingredient.title(),
                            ":", count, "food(s)"
                        )

            # Lists ingredient pairs that occur together in at least two foods.
            # Time Complexity: Worst case depends on all ingredient pairs
            # and the sizes of their incidence sets.
            elif choice == "14":
                results = database.get_ingredient_overlap_report()

                if not results:
                    print("No ingredient pairs are shared by multiple foods.")
                else:
                    print("\nIngredient pairs shared by multiple foods:")

                    for ingredients, foods in sorted(results.items()):
                        print(
                            ingredients[0].title(),
                            "+",
                            ingredients[1].title(),
                            "->",
                            ", ".join(food.title() for food in foods)
                        )

            # Summarizes foods with and without recorded allergen matches.
            # Time Complexity: Depends on the number of foods and incidence sets.
            elif choice == "15":
                allergens = read_names(
                    "Enter allergens separated by commas: "
                )

                report = checker.get_safety_audit_report(allergens)

                print("\nALLERGEN MATCHING SUMMARY")
                print("-" * 35)
                print("Total foods:", report["total_foods"])
                print(
                    "Foods with allergen matches:",
                    report["unsafe_foods"]
                )
                print(
                    "Foods without recorded matches:",
                    report["safe_foods"]
                )
                print(
                    "Percentage without recorded matches:",
                    str(report["safe_percentage"]) + "%"
                )
                print(
                    "\nThis report is based only on the ingredients "
                    "recorded in the database. It does not certify "
                    "food as medically safe."
                )

            # Displays graph counts and checks the data structure.
            # Time Complexity: O(V + F + I) for invariant validation.
            elif choice == "16":
                graph.display_statistics()

                print(
                    "Incidence index valid:",
                    graph.validate_invariants()
                )

            # Exits the application.
            # Time Complexity: O(1).
            elif choice == "0":
                print("Exiting the application.")
                break

            else:
                print("Invalid choice. Please select 0 to 16.")

        except (ValueError, TypeError) as error:
            print("Input error:", error)

    print("Thank you for using the Food Ingredient Allergy Checker!")


if __name__ == "__main__":
    main()
