
from hypergraph import HyperGraph
from food_database import FoodDatabase
from allergy_checker import AllergyChecker


# Time Complexity: O(n)
# Splits the input into names and removes extra spaces.
def read_names(prompt):
    values = input(prompt).strip()

    if not values:
        return []

    return [
        value.strip()
        for value in values.split(",")
        if value.strip()
    ]


# Time Complexity: O(F log F)
# Sorts the food names before displaying them.
def display_foods(foods):
    if not foods:
        print("No results found.")
        return

    for food in sorted(foods):
        print("-", food.title())


# Time Complexity: O(1)
# Displays all the available menu options.
def display_menu():
    print("\n" + "=" * 50)
    print("     FOOD INGREDIENT ALLERGY CHECKER")
    print("=" * 50)
    print("1. Display hypergraph")
    print("2. Display incidence index")
    print("3. Find foods containing any allergen")
    print("4. Find foods containing all ingredients")
    print("5. Find candidate foods without listed allergens")
    print("6. Explain ingredient matches")
    print("7. Add or update food")
    print("8. Remove food")
    print("9. Search food by name")
    print("10. Find shared ingredients")
    print("11. Find related foods")
    print("12. Find similar foods")
    print("13. Show common ingredients")
    print("14. Show ingredient overlap report")
    print("15. Show safety audit report")
    print("16. Show hypergraph statistics")
    print("0. Exit")
    print("=" * 50)


# Time Complexity: Depends on the selected operation.
# Creates the graph, loads sample foods and runs the menu.
def main():
    graph = HyperGraph()

    # Add sample foods so the program can be tested.
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
            # Time Complexity: Depends on the number of foods and ingredients that need to be displayed.
            if choice == "1":
                graph.display_hypergraph()

            # Time Complexity: Depends on the incidence index and the sorting needed for display.
            elif choice == "2":
                graph.display_incidence_index()

            # Finds foods containing at least one listed allergen.
            # Time Complexity: Depends on the incidence sets visited.
            elif choice == "3":
                allergens = read_names(
                    "Enter allergens separated by commas: "
                )
                result = checker.find_foods_with_any_allergen(allergens)
                display_foods(result)

            # Finds foods containing every requested ingredient.
            # Time Complexity: Depends on the sizes of the incidence sets.
            elif choice == "4":
                ingredients = read_names(
                    "Enter required ingredients separated by commas: "
                )
                result = checker.find_foods_with_all_ingredients(
                    ingredients
                )
                display_foods(result)

            # Lists foods that do not contain any listed allergens.
            # Time Complexity: O(F + I) in the general case.
            elif choice == "5":
                allergens = read_names(
                    "Enter allergens to exclude, separated by commas: "
                )
                result = checker.find_safe_candidates(allergens)
                print("Candidates with no recorded allergen matches:")
                display_foods(result)
                print(
                    "Note: This does not guarantee medical safety "
                    "or rule out cross-contamination."
                )

            # Explains which requested ingredients are present in foods.
            # Uses the explain_food_matches(ingredients) method from the earlier AllergyChecker implementation.
            elif choice == "6":
                ingredients = read_names(
                    "Enter ingredients to check, separated by commas: "
                )
                reports = checker.explain_food_matches(ingredients)

                if not reports:
                    print("No matching foods found.")
                else:
                    for report in reports:
                        print("\nFood:", report["food"].title())
                        print("Found:", report["found"])
                        print("Matching ingredients:", report["matches"])
                        print("Message:", report["message"])

            # Adds a food or updates its ingredient list.
            # Time Complexity: O(k) graph operations for a new food, excluding name-processing costs.
            elif choice == "7":
                food = input("Enter food name: ").strip()
                ingredients = read_names(
                    "Enter ingredients separated by commas: "
                )

                if not ingredients:
                    print("Please enter at least one ingredient.")
                    continue

                database.add_or_update_food(food, ingredients)
                print("Food added or updated.")

            # Removes a food and its links from the graph.
            # Time Complexity: O(k), excluding name normalization.
            elif choice == "8":
                food = input("Enter food name to remove: ").strip()

                if database.remove_food(food):
                    print("Food removed.")
                else:
                    print("Food not found.")

            # Checks whether the exact food name exists.
            # Time Complexity: O(n) because the name is normalized.
            elif choice == "9":
                food = input("Enter food name to search: ").strip()

                if database.search_food(food):
                    ingredients = graph.get_ingredients_for_food(food)
                    print(
                        food.title(),
                        "->",
                        ", ".join(sorted(ingredients))
                    )
                else:
                    print("Food not found.")

            # Finds ingredients shared by two foods.
            # Time Complexity: O(k1 + k2) to retrieve and compare the two ingredient sets.
            elif choice == "10":
                food1 = input("Enter first food: ").strip()
                food2 = input("Enter second food: ").strip()

                result = database.get_shared_ingredients(food1, food2)

                if result:
                    print("Shared ingredients:", ", ".join(sorted(result)))
                else:
                    print("No shared ingredients found.")

            # Finds foods that share one or more ingredients.
            # Time Complexity: Depends on the incidence sets visited.
            elif choice == "11":
                food = input("Enter food name: ").strip()
                results = database.find_related_foods(food)

                if not results:
                    print("No related foods found.")
                else:
                    for related_food, ingredients in sorted(results.items()):
                        print(
                            related_food.title(),
                            "- shared:",
                            ", ".join(sorted(ingredients))
                        )

            # Ranks foods according to ingredient similarity.
            # Time Complexity: Depends on the number of candidate foods and the sorting step.
            elif choice == "12":
                food = input("Enter food name: ").strip()
                results = database.find_similar_foods(food)

                if not results:
                    print("No similar foods found.")
                else:
                    for name, score, shared in results:
                        print(
                            name.title(),
                            "| Similarity:", score,
                            "| Shared ingredients:",
                            ", ".join(sorted(shared))
                        )

            # Shows the most frequently used ingredients.
            # Time Complexity: O(I + V log V) as a general bound.
            elif choice == "13":
                limit = int(
                    input("Number of ingredients to display: ")
                )
                results = database.get_most_common_ingredients(limit)

                for ingredient, count in results:
                    print(ingredient.title(), ":", count, "foods")

            # Shows ingredient pairs that occur together in multiple foods.
            # Time Complexity: Worst case depends on all ingredient pairs and the sizes of their incidence sets.
            elif choice == "14":
                results = database.get_ingredient_overlap_report()

                if not results:
                    print("No shared ingredient pairs found.")
                else:
                    for ingredients, foods in sorted(results.items()):
                        print(
                            ingredients[0].title(),
                            "and",
                            ingredients[1].title(),
                            "->",
                            ", ".join(food.title() for food in foods)
                        )

            # Reports foods with and without recorded allergen matches.
            # Time Complexity: Depends on the foods and incidence sets.
            elif choice == "15":
                allergens = read_names(
                    "Enter your allergens separated by commas: "
                )
                report = checker.get_safety_audit_report(allergens)

                print("\nSAFETY AUDIT SUMMARY")
                print("-" * 30)
                print("Total foods:", report["total_foods"])
                print("Foods with matching allergens:", report["unsafe_foods"])
                print("Foods without recorded matches:", report["safe_foods"])
                print(
                    "Percentage without recorded matches:",
                    str(report["safe_percentage"]) + "%"
                )
                print("This report does not certify food as medically safe.")

            # Displays the hypergraph counts and checks its structure.
            # Time Complexity: O(V + F + I) for validation.
            elif choice == "16":
                graph.display_statistics()
                print(
                    "Incidence index valid:",
                    graph.validate_invariants()
                )

            # Exits the program.
            # Time Complexity: O(1).
            elif choice == "0":
                print("Exiting the application.")
                break

            else:
                print("Invalid choice. Please select 0 to 16.")

        # Handles invalid input and incorrect data types.
        except (ValueError, TypeError) as error:
            print("Input error:", error)

    print("Thank you for using the Food Ingredient Allergy Checker!")


if __name__ == "__main__":
    main()
