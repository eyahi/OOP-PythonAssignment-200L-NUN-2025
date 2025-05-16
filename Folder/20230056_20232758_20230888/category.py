class Category:
    def __init__(self, name):
        self.name = name
        self.recipes = []

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def remove_recipe(self, recipe_name):
        self.recipes = [r for r in self.recipes if r.name != recipe_name]