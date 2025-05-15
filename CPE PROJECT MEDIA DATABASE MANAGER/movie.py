
class Movie:
    def __init__(self, title, director, genre, release_year, poster_path=None):
        self.title = title
        self.director = director
        self.genre = genre
        self.release_year = release_year
        self.poster_path = poster_path
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)
