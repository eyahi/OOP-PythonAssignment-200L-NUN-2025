class Recipe:
    # Represents a single recipe with its name, category, ingredients, instructions, and rating.
    def __init__(self, name, category, ingredients, instructions, rating=0.0, ratings_count=0):
        # Initializes a new Recipe instance.
        self.name = name  # Name of the recipe.
        self.category = category  # Category the recipe belongs to.
        self.ingredients = ingredients  # List of ingredints.
        self.instructions = instructions  # Preparation Instructions.
        self.rating = rating  # Recipe rating. 
        self.ratings_count = ratings_count  # Recipe rating count.

    def add_rating(self, new_rating):
        # Adds the desired rating to the recipe.
        total = self.rating * self.ratings_count
        self.ratings_count += 1
        total += new_rating
        self.rating = round(total / self.ratings_count, 2)

    def to_dict(self):
        # Converts the recipe object into a dictionary for JSON serialization.
        return{
            "name": self.name,
            "category": self.category,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "rating": self.rating,
            "ratings_count": self.ratings_count
        }
    
    @classmethod
    def from_dict(cls, data):
        # Creates a Recipe instance from a dictionary.
        return cls(data["name"], data["category"], data["ingredients"], data["instructions"], data.get("rating", 0.0), data.get("ratings_count", 0))