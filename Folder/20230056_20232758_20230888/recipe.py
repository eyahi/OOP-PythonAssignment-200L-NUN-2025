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