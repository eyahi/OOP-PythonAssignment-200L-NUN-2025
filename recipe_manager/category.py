class Category:
    # Represents a category that holds a collection of recipes.
    def __init__(self, name):
        # Initializes a Category with a name and an empty recipe dictionary.
        self.name = name
        self.recipes = []

    def add_recipe(self, recipe):
        # Adds a recipe to the category.
        self.recipes.append(recipe)

    def remove_recipe(self, recipe):
        # Removes a recipe from the category by its name.
        if recipe in self.recipes:
            self.recipes.remove(recipe)