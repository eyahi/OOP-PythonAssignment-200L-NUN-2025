class Category:
    def __init__(self, name):
        self.name = name
        self.recipes = []

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def remove_recipe(self, recipe_name):
        self.recipes = [recipe for recipe in self.recipes if recipe.name != recipe_name]

    def list_recipes(self):
        return [recipe.name for recipe in self.recipes]

    def __str__(self):
        return f"Category: {self.name} | Recipes: {', '.join(self.list_recipes())}"