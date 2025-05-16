import json
from recipe import Recipe
from category import Category

class RecipeManager:
    """ Manages a collection of recipes and categories.
    Provides methods for CRUD operations, searching, and file I/O.
    """
    def __init__(self):
        # Initializes the Recipemanager with empty dictionaries for recipes and categories.
        self.recipes = {}
        self.categories = {}

    def add_recipe(self, name, category, ingredients, instructions):
        # Adds a new recipe to the manager and assigns it to a category.
        recipe = Recipe(name, category, ingredients, instructions)
        self.recipes[name] = recipe

        if category not in self.categories:
            self.categories[category] = Category(category)
        self.categories[category].add_recipe(recipe)

    def get_recipe(self, name):
        # Retrives a recipe by name.
        return self.recipes.get(name)
    
    def update_recipe(self, name, category, ingredients, instructions):
        # Updates an existing recipe with new values.
        if name in self.recipes:
            self.recipes[name] = Recipe(name, category, ingredients, instructions)
            
    def delete_recipe(self, name):
        # Deletes a recipe from the manager.
        if name in self.recipes:
            category = self.recipes[name].category
            if category in self.categories:
                self.categories[category].remove_recipe(name)
            del self.recipes[name]

    def search_recipes(self, query):
        # Searches for recipes by name, category, or ingredients.
        results = []
        query = query.lower()
        for recipe in self.recipes.values():
            if (query in recipe.name.lower() or
                query in recipe.category.lower() or
                any(query in ingredients.lower() for ingredients in recipe.ingredients)):
                results.append(recipe)
        return results
    
    def save_to_file(self, filename="recipes.json"):
        # Saves all recipes to JSON file.
        with open(filename, "w") as f:
            data = {name: recipe.to_dict() for name, recipe in self.recipes.items()}
            json.dump(data, f, indent=4)

    def load_from_file(self, filename="recipes.json"):
        # Load recipes from a JSON file into the manager.
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for recipe_data in data.values():
                    recipe = Recipe.from_dict(recipe_data)
                    self.recipes[recipe.name] = recipe
                    if recipe.category not in self.categories:
                       self.categories[recipe.category] = Category(recipe.category)
                    self.categories[recipe.category].add_recipe(recipe)
        except FileNotFoundError:
            pass
       
def main():
    """ Provides the command-line interface for the Recipe Manager application.
    Allows users to interact with the system using menu options."""
    manager = RecipeManager()
    manager.load_from_file()

    while True:
        print("\n--- Recipe Manager ---")
        print("1. Add Recipe")
        print("2. View Recipe")
        print("3. Update Recipe")
        print("4. Dlete Recipe")
        print("5. Search Recipes")
        print("6. List All Recipes")
        print("7. Rate a Recipe")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Recipe name: ")
            category = input("Category: ")
            ingredients = input("Ingredients (comma-separated): ").split(",")
            instructions = input("Instructions: ")
            manager.add_recipe(name.strip(), category.strip(), [i.strip() for i in ingredients], instructions.strip())
            manager.save_to_file()

        elif choice == "2":
            name = input("Enter recipe name: ")
            recipe = manager.get_recipe(name.strip())
            if recipe:
                print(f"\nName: {recipe.name}")
                print(f"Category: {recipe.category}")
                print("Ingredinets:", ", ".join(recipe.ingredients))
                print("Instructions:", recipe.instructions)
            else:
                print("Recipe not found.")

        elif choice == "3":
            name = input("Recipe name to update: ")
            if manager.get_recipe(name.strip()):
                category = input("New category: ")
                ingredients = input("New ingredients (Comma-separated): ").split(",")
                instructions = input("New instructions: ")
                manager.update_recipe(name.strip(), category.strip(), [i.strip() for i in ingredients], instructions.strip())
                manager.save_to_file()
            else:
                print("Recipe not found.")

        elif choice == "4":
            name = input("Recipe deleted: ")
            manager.delete_recipe(name.strip())
            manager.save_to_file()

        elif choice == "5":
            query = input("Enter search query: ")
            results = manager.search_recipes(query)
            if results:
                for r in results:
                    print(f"\n- {r.name} [{r.category}]")
            else:
                print("No recipes found.")
        
        elif choice == "6":
            if manager.recipes:
                for r in manager.recipes.values():
                    print(f"- {r.name} [{r.category}] - {r.rating}")
            else:
                print("No recipes available.")

        elif choice == "7":
            name = input("Recipe name to rate: ")
            recipe = manager.get_recipe(name.strip())
            if recipe:
                try:
                    rating = float(input("Enter your rating (1-5): "))
                    if 1 <= rating <= 5:
                        recipe.add_rating(rating)
                        manager.save_to_file()
                        print(f"New average rating: {recipe.rating} based on {recipe.ratings_count} ratings(s).")
                    else:
                        print("Rating must be between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            else:
                print("Recipe not found.")

        elif choice == "8":
            manager.save_to_file()
            print("Goodbye.see you again!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()