class Recipe:
    def __init__(self, name, category, ingredients, instructions):
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.instructions = instructions

    def to_dict(self):
        """Convert recipe object to dictionary for saving to file."""
        return {
            "name": self.name,
            "category": self.category,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        }

    def __str__(self):
        """String representation of the recipe."""
        return f"{self.name} ({self.category})\nIngredients: {', '.join(self.ingredients)}\nInstructions: {self.instructions}"