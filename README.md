#20232758 Ezechi nnanyere
#20230056 Folayemi David 
#20230888 Owolawi Sultan
# Recipe Manager

A simple Python application with a graphical user interface (GUI) that allows you to add, view, search, and delete recipes. Recipes are categorized, and all data is saved to a JSON file for persistence.

## Features

- Add new recipes with name, category, ingredients, and instructions.
- View detailed recipes.
- Search recipes by name, category, or ingredient.
- Delete recipes.
- Recipes are saved to a local JSON file (`recipes.json`).
- Simple and clean GUI using `Tkinter`.

## Requirements

- Python 3.x
- Tkinter (included by default in standard Python distributions)

## How to Run

1. Clone or download the repository.
2. Make sure all files (`recipe_manager.py`, `recipe.py`, `category.py`) are in the same folder.
3. Open your terminal or VS Code terminal in the project folder.
4. Run the app:

```bash
python recipe_manager.py


class Recipe:
    def __init__(self, name, category, ingredients, instructions):
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.instructions = instructions

    def get_details(self):
        return {
            'name': self.name,
            'category': self.category,
            'ingredients': self.ingredients,
            'instructions': self.instructions
        }

    def set_details(self, name, category, ingredients, instructions):
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.instructions = instructions


class Category:
    def __init__(self, name):
        self.name = name
        self.recipes = []

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def remove_recipe(self, recipe_name):
        self.recipes = [r for r in self.recipes if r.name != recipe_name]




import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from recipe import Recipe
from category import Category


class RecipeManager:
    def __init__(self):
        self.recipes = {}
        self.categories = {}
        self.load_from_file()

    def add_recipe(self, name, category, ingredients, instructions):
        if category not in self.categories:
            self.categories[category] = Category(category)
        recipe = Recipe(name, category, ingredients, instructions)
        self.recipes[name] = recipe
        self.categories[category].add_recipe(recipe)

    def get_recipe(self, name):
        return self.recipes.get(name)

    def update_recipe(self, name, category, ingredients, instructions):
        if name in self.recipes:
            self.recipes[name].set_details(name, category, ingredients, instructions)

    def delete_recipe(self, name):
        recipe = self.recipes.pop(name, None)
        if recipe and recipe.category in self.categories:
            self.categories[recipe.category].remove_recipe(name)

    def search_recipes(self, query):
        query = query.lower()
        return [
            r for r in self.recipes.values()
            if query in r.name.lower() or
               query in r.category.lower() or
               any(query in ing.lower() for ing in r.ingredients)
        ]

    def save_to_file(self):
        with open("recipes.json", "w") as f:
            json.dump({name: r.get_details() for name, r in self.recipes.items()}, f, indent=4)

    def load_from_file(self):
        if os.path.exists("recipes.json"):
            with open("recipes.json", "r") as f:
                data = json.load(f)
                for r in data.values():
                    self.add_recipe(r['name'], r['category'], r['ingredients'], r['instructions'])


# GUI FUNCTIONS
def main():
    manager = RecipeManager()
    root = tk.Tk()
    root.title("Recipe Manager")

    def prompt_recipe_data(update=False):
        name = simpledialog.askstring("Recipe Name", "Enter recipe name:")
        if not name:
            return None

        if update and name not in manager.recipes:
            messagebox.showerror("Error", "Recipe not found.")
            return None

        category = simpledialog.askstring("Category", "Enter category:")
        ingredients = simpledialog.askstring("Ingredients", "Enter ingredients (comma-separated):")
        instructions = []

        while True:
            step = simpledialog.askstring("Instructions", "Enter instruction (type 'end' to stop):")
            if not step or step.lower() == "end":
                break
            instructions.append(step)

        return name, category, ingredients.split(","), instructions

    def add_recipe():
        data = prompt_recipe_data()
        if data:
            name, category, ingredients, instructions = data
            manager.add_recipe(name, category, ingredients, instructions)
            manager.save_to_file()
            messagebox.showinfo("Success", "Recipe added!")

    def view_recipe():
        name = simpledialog.askstring("View Recipe", "Enter recipe name:")
        recipe = manager.get_recipe(name)
        if recipe:
            details = recipe.get_details()
            info = (
                f"Name: {details['name']}\nCategory: {details['category']}\n\n"
                f"Ingredients:\n- " + "\n- ".join(details['ingredients']) + "\n\n"
                f"Instructions:\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(details['instructions']))
            )
            messagebox.showinfo("Recipe Details", info)
        else:
            messagebox.showerror("Error", "Recipe not found.")

    def update_recipe():
        data = prompt_recipe_data(update=True)
        if data:
            name, category, ingredients, instructions = data
            manager.update_recipe(name, category, ingredients, instructions)
            manager.save_to_file()
            messagebox.showinfo("Success", "Recipe updated.")

    def delete_recipe():
        name = simpledialog.askstring("Delete Recipe", "Enter recipe name:")
        if manager.get_recipe(name):
            manager.delete_recipe(name)
            manager.save_to_file()
            messagebox.showinfo("Deleted", "Recipe deleted.")
        else:
            messagebox.showerror("Error", "Recipe not found.")

    def search_recipe():
        query = simpledialog.askstring("Search", "Enter search term:")
        results = manager.search_recipes(query)
        if results:
            text = "\n".join([f"{r.name} ({r.category})" for r in results])
            messagebox.showinfo("Search Results", text)
        else:
            messagebox.showinfo("No Results", "No recipes found.")

    # GUI Layout
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    tk.Label(frame, text="Recipe Manager", font=("Arial", 18, "bold")).pack(pady=10)

    for text, func in [
        ("Add Recipe", add_recipe),
        ("View Recipe", view_recipe),
        ("Update Recipe", update_recipe),
        ("Delete Recipe", delete_recipe),
        ("Search Recipes", search_recipe),
        ("Exit", root.quit)
    ]:
        tk.Button(frame, text=text, width=25, command=func).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
