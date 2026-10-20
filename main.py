
from hypergraph import HyperGraph
from food_database import FoodDatabase
from allergy_checker import AllergyChecker


def read_names(prompt):
    values = input(prompt).strip()

    if not values:
        return []

    return [
        value.strip()
        for value in values.split(",")
        if value.strip()
    ]


def display_foods(foods):
    if not foods:
        print("No results found.")
        return

    for food in sorted(foods):
        print("-", food.title())


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


def main():
    graph = HyperGraph()

    # Sample food data
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
            if choice == "1":
                graph.display_hypergraph()

            elif choice == "2":
                graph.display_incidence_index()

            elif choice == "3":
                allergens = read_names(
                    "Enter allergens separated by commas: "
                )
                result = checker.find_foods_with_any_allergen(allergens)
                display_foods(result)

            elif choice == "4":
                ingredients = read_names(
                    "Enter required ingredients separated by commas: "
                )
                result = checker.find_foods_with_all_ingredients(
                    ingredients
                )
                display_foods(result)

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

            elif choice == "6":
                food = input("Enter food name: ").strip()
                allergens = read_names(
                    "Enter allergens to check: "
                )
                report = checker.explain_food_matches(food, allergens)

                print("Food:", report["food"].title())
                print("Found:", report["found"])
                print("Matching ingredients:", report["matches"])
                print("Message:", report["message"])

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

            elif choice == "8":
                food = input("Enter food name to remove: ").strip()

                if database.remove_food(food):
                    print("Food removed.")
                else:
                    print("Food not found.")

            elif choice == "9":
                term = input("Enter full or partial food name: ")
                results = database.search_food(term)

                if not results:
                    print("No matching foods found.")
                else:
                    for food, ingredients in sorted(results.items()):
                        print(
                            food.title(),
                            "->",
                            ", ".join(sorted(ingredients))
                        )

            elif choice == "10":
                food1 = input("Enter first food: ").strip()
                food2 = input("Enter second food: ").strip()

                result = database.get_shared_ingredients(food1, food2)
                print("Shared ingredients:")
                display_foods(result) if False else print(
                    ", ".join(sorted(result)) if result else "None"
                )

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

            elif choice == "13":
                limit = int(input("Number of ingredients to display: "))
                results = database.get_most_common_ingredients(limit)

                for ingredient, count in results:
                    print(ingredient.title(), ":", count, "foods")

            elif choice == "14":
                results = database.get_ingredient_overlap_report()

                if not results:
                    print("No shared ingredients found.")
                else:
                    for ingredient, foods in sorted(results.items()):
                        print(
                            ingredient.title(),
                            "->",
                            ", ".join(food.title() for food in foods)
                        )

            elif choice == "15":
                allergens = read_names(
                    "Enter your allergens separated by commas: "
                )
                report = checker.get_safety_audit_report(allergens)

                print("\nSAFETY AUDIT SUMMARY")
                print("-" * 30)
                print("Total foods:", report["total_foods"])
                print("Foods with matching allergens:", report["unsafe_count"])
                print("Foods without recorded matches:", report["safe_count"])
                print(
                    "Percentage without recorded matches:",
                    str(report["safety_percentage"]) + "%"
                )
                print("This report does not certify food as medically safe.")

            elif choice == "16":
                graph.display_statistics()

                print(
                    "Incidence index valid:",
                    graph.validate_invariants()
                )

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
