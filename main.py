from hypergraph import HyperGraph
from food_database import FoodDatabase
from allergy_checker import AllergyChecker


# Reads comma-separated names from the user.
# Time: O(n), where n is the input length.
def read_names(prompt):
    values = input(prompt).strip()
    if not values:
        return []
    return [value.strip() for value in values.split(",") if value.strip()]


# Displays a collection of food names in alphabetical order.
# Time: O(F log F), where F is the number of foods.
def display_foods(foods):
    if not foods:
        print("No matching foods found.")
        return
    for food in sorted(foods):
        print("-", food.title())


# Displays the main menu.
# Time: O(1), since the menu size is fixed.
def display_menu():
    print("\n" + "=" * 55)
    print("       FOOD INGREDIENT ALLERGY CHECKER")
    print("=" * 55)
    print("1. Display food hypergraph")
    print("2. Display ingredient incidence index")
    print("3. Search foods by ingredients")
    print("4. Check foods against allergens")
    print("5. Add or update a food")
    print("6. Delete a food")
    print("7. Delete an ingredient vertex")
    print("8. Find a food by exact name")
    print("9. Compare two foods")
    print("10. Find related foods and similarity")
    print("11. Ingredient analysis")
    print("12. Show hypergraph statistics")
    print("0. Exit")
    print("=" * 55)


# Loads sample data and runs the menu.
# Time complexity depends on the operation selected by the user.
def main():
    graph = HyperGraph()

    # Sample foods are added so the program can be tested immediately.
    graph.add_food("Pizza", ["Wheat", "Milk", "Cheese", "Tomato"])
    graph.add_food("Pasta", ["Wheat", "Egg", "Cheese", "Tomato"])
    graph.add_food("Cake", ["Wheat", "Egg", "Milk", "Butter"])
    graph.add_food("Fruit Bowl", ["Apple", "Banana", "Grapes"])

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

            # One search option supports any, all, or exact ingredient matching.
            elif choice == "3":
                print("1. Foods containing ANY listed ingredient")
                print("2. Foods containing ALL listed ingredients")
                print("3. Foods containing EXACTLY these ingredients")
                mode = input("Choose search type: ").strip()
                ingredients = read_names(
                    "Enter ingredients separated by commas: "
                )

                if not ingredients:
                    print("Please enter at least one ingredient.")
                    continue

                if mode == "1":
                    result = checker.find_foods_with_any_allergen(ingredients)
                elif mode == "2":
                    result = checker.find_foods_with_all_ingredients(ingredients)
                elif mode == "3":
                    result = checker.find_foods_with_exact_ingredients(ingredients)
                else:
                    print("Invalid search type.")
                    continue

                display_foods(result)

                for food in sorted(result):
                    matched = graph.get_ingredients_for_food(food) & {
                        item.strip().casefold() for item in ingredients
                    }
                    print(" ", food.title(), "- matching:", ", ".join(sorted(matched)))

            # Shows foods with no recorded matches for the listed allergens.
            elif choice == "4":
                allergens = read_names(
                    "Enter allergens to check, separated by commas: "
                )
                unsafe = checker.find_foods_with_any_allergen(allergens)
                safe = checker.find_safe_candidates(allergens)

                print("\nFoods with recorded allergen matches:")
                display_foods(unsafe)
                print("\nFoods with no recorded allergen matches:")
                display_foods(safe)
                print("This does not guarantee medical safety or rule out cross-contamination.")

            elif choice == "5":
                food = input("Enter food name: ").strip()
                ingredients = read_names(
                    "Enter ingredients separated by commas: "
                )
                if not ingredients:
                    print("Please enter at least one ingredient.")
                    continue
                database.add_or_update_food(food, ingredients)
                print("Food added or updated.")

            elif choice == "6":
                food = input("Enter food name to delete: ").strip()
                if database.remove_food(food):
                    print("Food deleted.")
                else:
                    print("Food not found.")

            # A single graph method handles deletion of an ingredient vertex.
            elif choice == "7":
                ingredient = input("Enter ingredient vertex to delete: ").strip()
                if graph.delete_vertex(ingredient):
                    print("Ingredient vertex deleted.")
                    print("Any food left without ingredients was deleted too.")
                else:
                    print("Ingredient vertex not found.")

            elif choice == "8":
                food = input("Enter exact food name: ").strip()
                if database.search_food(food):
                    ingredients = graph.get_ingredients_for_food(food)
                    print(food.title(), "->", ", ".join(sorted(ingredients)))
                else:
                    print("Food not found.")

            # Combines the two-food ingredient comparison into one option.
            elif choice == "9":
                food1 = input("Enter first food: ").strip()
                food2 = input("Enter second food: ").strip()

                if not database.search_food(food1) or not database.search_food(food2):
                    print("One or both foods were not found.")
                    continue

                shared = database.get_shared_ingredients(food1, food2)
                ingredients1 = graph.get_ingredients_for_food(food1)
                ingredients2 = graph.get_ingredients_for_food(food2)

                print("\\n", food1.title(), ":", ", ".join(sorted(ingredients1)))
                print(food2.title(), ":", ", ".join(sorted(ingredients2)))
                print("Shared ingredients:", ", ".join(sorted(shared)) if shared else "None")

            # Related foods and similarity are shown together, avoiding duplicate options.
            elif choice == "10":
                food = input("Enter food name: ").strip()
                if not database.search_food(food):
                    print("Food not found.")
                    continue

                related = database.find_related_foods(food)
                similar = database.find_similar_foods(food)

                if not related:
                    print("No other foods share ingredients with this food.")
                else:
                    print("\\nRelated foods and shared ingredients:")
                    for name, shared in sorted(related.items()):
                        print(name.title(), "->", ", ".join(sorted(shared)))

                if similar:
                    print("\\nSimilarity ranking (Jaccard score):")
                    for name, score, shared in similar:
                        print(
                            name.title(),
                            "| Score:", score,
                            "| Shared:", ", ".join(sorted(shared))
                        )

            # Ingredient frequency and overlap reports live under one analysis option.
            elif choice == "11":
                print("1. Most frequently used ingredients")
                print("2. Ingredient pairs shared by multiple foods")
                mode = input("Choose analysis: ").strip()

                if mode == "1":
                    limit = int(input("Number of ingredients to display: "))
                    if limit < 1:
                        print("Enter a number greater than zero.")
                        continue
                    results = database.get_most_common_ingredients(limit)
                    for ingredient, count in results:
                        print(ingredient.title(), ":", count, "food(s)")

                elif mode == "2":
                    results = database.get_ingredient_overlap_report()
                    if not results:
                        print("No ingredient pairs are shared by multiple foods.")
                    else:
                        for pair, foods in sorted(results.items()):
                            print(
                                pair[0].title(), "+", pair[1].title(),
                                "->", ", ".join(food.title() for food in foods)
                            )
                else:
                    print("Invalid analysis type.")

            elif choice == "12":
                graph.display_statistics()

            elif choice == "0":
                print("Exiting the application.")
                break

            else:
                print("Invalid choice. Please select 0 to 12.")

        except (ValueError, TypeError) as error:
            print("Input error:", error)

    print("Thank you for using the Food Ingredient Allergy Checker!")


if __name__ == "__main__":
    main()
