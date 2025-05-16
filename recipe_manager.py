import json
import os
from recipe import Recipe

class RecipeManager:
    def __init__(self):
        self.recipes = {}

    def add_recipe(self, name, category, ingredients, instructions):
        self.recipes[name] = Recipe(name, category, ingredients, instructions)

    def get_recipe(self, name):
        return self.recipes.get(name)

    def update_recipe(self, name, category, ingredients, instructions):
        if name in self.recipes:
            self.recipes[name] = Recipe(name, category, ingredients, instructions)

    def delete_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]

    def search_recipes(self, query):
        return [r for r in self.recipes.values() if query.lower() in r.name.lower()]

    def save_to_file(self, filename='data/recipes.json'):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({k: vars(v) for k, v in self.recipes.items()}, f, indent=4)

    def load_from_file(self, filename='data/recipes.json'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.recipes = {k: Recipe(**v) for k, v in data.items()}
        except FileNotFoundError:
            print("No recipe file found. Starting with an empty recipe manager.")

if __name__ == "__main__":
    manager = RecipeManager()
    manager.load_from_file()

    while True:
        print("\nRecipe Manager")
        print("1. Add Recipe")
        print("2. View Recipe")
        print("3. Delete Recipe")
        print("4. Search Recipes")
        print("5. Save and Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Recipe name: ")
            category = input("Category: ")
            ingredients = input("Ingredients (comma-separated): ").split(",")
            instructions = input("Instructions: ")
            manager.add_recipe(name, category, ingredients, instructions)

        elif choice == "2":
            name = input("Enter recipe name: ")
            recipe = manager.get_recipe(name)
            if recipe:
                print(f"\nName: {recipe.name}")
                print(f"Category: {recipe.category}")
                print(f"Ingredients: {', '.join(recipe.ingredients)}")
                print(f"Instructions: {recipe.instructions}")
            else:
                print("Recipe not found.")

        elif choice == "3":
            name = input("Enter recipe name to delete: ")
            manager.delete_recipe(name)
            print("Recipe deleted if it existed.")

        elif choice == "4":
            query = input("Search query: ")
            results = manager.search_recipes(query)
            for recipe in results:
                print(f"- {recipe.name}")

        elif choice == "5":
            manager.save_to_file()
            print("Recipes saved. Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")