import json
import tkinter as tk
from tkinter import messagebox
from recipe import Recipe
from category import Category

class RecipeManager:
    def __init__(self, filename="recipes.json"):
        self.filename = filename
        self.recipes = {}
        self.load_from_file()

    def add_recipe(self, name, category, ingredients, instructions):
        recipe = Recipe(name, category, ingredients.split(","), instructions)
        self.recipes[name] = recipe
        self.save_to_file()

    def get_recipe(self, name):
        return self.recipes.get(name, None)
    
    def update_recipe(self, name, category=None, ingredients=None, instructions=None):
        recipe = self.get_recipe(name)
        if recipe:
            if category:
                recipe.category = category
            if ingredients:
                recipe.ingredients = ingredients.split(",")
            if instructions:
                recipe.instructions = instructions
            self.save_to_file()
            return True
        return False

    def delete_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            self.save_to_file()

    def search_recipes(self, keyword):
        return [recipe for recipe in self.recipes.values() if keyword.lower() in recipe.name.lower()
                or any(keyword.lower() in ingredient.lower() for ingredient in recipe.ingredients)]

    def save_to_file(self):
        with open(self.filename, "w") as file:
            json.dump({name: recipe.to_dict() for name, recipe in self.recipes.items()}, file, indent=4)

    def load_from_file(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.recipes = {name: Recipe(**info) for name, info in data.items()}
        except FileNotFoundError:
            self.recipes = {}

class RecipeApp:
    def __init__(self, root):
        self.manager = RecipeManager()
        self.root = root
        self.root.title("Recipe Manager")

        tk.Label(root, text="Recipe Name:").grid(row=0, column=0)
        tk.Label(root, text="Category:").grid(row=1, column=0)
        tk.Label(root, text="Ingredients (comma-separated):").grid(row=2, column=0)
        tk.Label(root, text="Instructions:").grid(row=3, column=0)

        self.name_entry = tk.Entry(root)
        self.category_entry = tk.Entry(root)
        self.ingredients_entry = tk.Entry(root)
        self.instructions_entry = tk.Entry(root)

        self.name_entry.grid(row=0, column=1)
        self.category_entry.grid(row=1, column=1)
        self.ingredients_entry.grid(row=2, column=1)
        self.instructions_entry.grid(row=3, column=1)

        tk.Button(root, text="Add Recipe", command=self.add_recipe).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="View Recipe", command=self.view_recipe).grid(row=5, column=0, columnspan=2)
        tk.Button(root, text="Update Recipe", command=self.update_recipe).grid(row=6, column=0, columnspan=2)
        tk.Button(root, text="Delete Recipe", command=self.delete_recipe).grid(row=7, column=0, columnspan=2)
        tk.Button(root, text="Search Recipe", command=self.search_recipe).grid(row=8, column=0, columnspan=2)

    def add_recipe(self):
        name = self.name_entry.get()
        category = self.category_entry.get()
        ingredients = self.ingredients_entry.get()
        instructions = self.instructions_entry.get()
        
        if name and category and ingredients and instructions:
            self.manager.add_recipe(name, category, ingredients, instructions)
            messagebox.showinfo("Success", "Recipe added!")
        else:
            messagebox.showwarning("Error", "All fields must be filled.")

    def view_recipe(self):
        name = self.name_entry.get()
        recipe = self.manager.get_recipe(name)
        
        if recipe:
            messagebox.showinfo("Recipe Details", str(recipe))
        else:
            messagebox.showwarning("Error", "Recipe not found.")

    def delete_recipe(self):
        name = self.name_entry.get()
        self.manager.delete_recipe(name)
        messagebox.showinfo("Success", "Recipe deleted.")

    def update_recipe(self):
        success = self.manager.update_recipe(self.name_entry.get(), self.category_entry.get(),
                                             self.ingredients_entry.get(), self.instructions_entry.get())
        messagebox.showinfo("Success", "Recipe updated!" if success else "Recipe not found.")

    def search_recipe(self):
        results = self.manager.search_recipes(self.name_entry.get())
        messagebox.showinfo("Search Results", "\n".join(str(recipe) for recipe in results) if results else "No recipes found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()
