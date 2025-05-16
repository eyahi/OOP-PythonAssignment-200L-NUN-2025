#group members
# Divine UDOH 20231712
# Blair Nwokike 20230050
#Edeoga Chukwuemeka 20230941

import tkinter as tk
from tkinter import simpledialog, messagebox
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from movie import Movie
from review import Review

# SQLAlchemy setup
Base = declarative_base()

class MovieModel(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    director = Column(String)
    genre = Column(String)
    release_year = Column(Integer)
    reviews = relationship("ReviewModel", back_populates="movie", cascade="all, delete")

    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(r.rating for r in self.reviews) / len(self.reviews)

class ReviewModel(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    reviewer_name = Column(String)
    rating = Column(Float)
    comment = Column(String)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship("MovieModel", back_populates="reviews")

# DB engine
engine = create_engine('sqlite:///movies.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

class MovieDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Database")
        self.root.geometry("500x400")
        self.root.configure(bg="#2e2e2e")

        title_label = tk.Label(root, text="Movie Database", font=("Arial", 18, "bold"), bg="#2e2e2e", fg="#ffffff")
        title_label.pack(pady=20)

        button_frame = tk.Frame(root, bg="#2e2e2e")
        button_frame.pack(pady=10)

        self.create_button(button_frame, "Add Movie", self.add_movie).pack(pady=5)
        self.create_button(button_frame, "Delete Movie", self.delete_movie).pack(pady=5)
        self.create_button(button_frame, "View Movies", self.view_movies).pack(pady=5)
        self.create_button(button_frame, "Search Movies", self.search_movies).pack(pady=5)
        self.create_button(button_frame, "Exit", root.quit).pack(pady=5)

    def create_button(self, parent, text, command):
        return tk.Button(parent, text=text, width=20, height=2, bg="#4CAF50", fg="white",
                         font=("Arial", 12), command=command, relief="raised", bd=2)

    def add_movie(self):
        title = simpledialog.askstring("Movie Title", "Enter the movie title:")
        if  not title :
            return
        director = simpledialog.askstring("Director", "Enter the director:")
        genre = simpledialog.askstring("Genre", "Enter the genre:")
        year = simpledialog.askinteger("Release Year", "Enter the release year:")

        if session.query(MovieModel).filter_by(title=title).first():
            messagebox.showwarning("Duplicate", "This movie already exists.")
            return

        movie = MovieModel(title=title, director=director, genre=genre, release_year=year)
        session.add(movie)
        session.commit()
        messagebox.showinfo("Success", "Movie added successfully.")

    def delete_movie(self):
        title = simpledialog.askstring("Delete Movie", "Enter the title of the movie to delete:")
        if not title:
            return
        movie = session.query(MovieModel).filter_by(title=title).first()
        if not movie:
            messagebox.showerror("Error", "Movie not found.")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{title}'?")
        if confirm:
            session.delete(movie)
            session.commit()
            messagebox.showinfo("Deleted", f"'{title}' has been deleted.")

    def view_movies(self):
        top = tk.Toplevel(self.root)
        top.title("All Movies")
        top.geometry("600x500")
        top.configure(bg="#1e1e1e")

        movies = session.query(MovieModel).all()
        reviews = session.query(ReviewModel).all()
        for movie in movies:
            rating = round(movie.average_rating(), 2)
            movie_description = f"{movie.title} ({movie.release_year}) - {movie.genre}, Dir: {movie.director} | ⭐ {rating}"

            tk.Label(top, text=movie_description, bg="#1e1e1e", fg="white", font=("Arial", 14)).pack(anchor="w", padx=10, pady=2)
            tk.Label(top, text="Reviews:", bg="#1e1e1e", fg="white", font=("Arial", 13)).pack(anchor="w", padx=10, pady=2)

            for review in reviews:
                if review.movie_id == movie.id:
                    text = (f"{review.reviewer_name} {review.rating}⭐\n "
                            f"{review.comment}")
                    tk.Label(top, text=text, bg="#1e1e1e", fg="white", font=("Times New Roman", 11)).pack(anchor="w", padx=10, pady=2)

            tk.Button(top, text="Add Review", command=lambda m=movie: self.add_review(m), bg="#2196F3", fg="white").pack(pady=2)

    def search_movies(self):
        query = simpledialog.askstring("Search", "Enter title, director, or genre:")
        if not query:
            return

        results = session.query(MovieModel).filter(
            (MovieModel.title.ilike(f"%{query}%")) |
            (MovieModel.genre.ilike(f"%{query}%")) |
            (MovieModel.director.ilike(f"%{query}%"))
        ).all()

        top = tk.Toplevel(self.root)
        top.title("Search Results")
        top.geometry("600x500")
        top.configure(bg="#1e1e1e")

        if not results:
            tk.Label(top, text="No results found.", font=("Arial", 12), fg="red", bg="#1e1e1e").pack(pady=20)
            return

        for movie in results:
            rating = round(movie.average_rating(), 2)
            info = f"{movie.title} ({movie.release_year}) - {movie.genre}, Dir: {movie.director} | ⭐ {rating}"
            tk.Label(top, text=info, bg="#1e1e1e", fg="white", font=("Arial", 11)).pack(anchor="w", padx=10, pady=2)

    def add_review(self, movie):
        reviewer = simpledialog.askstring("Reviewer", "Enter your name:")
        rating = simpledialog.askfloat("Rating", "Enter rating (0-5):")
        comment = simpledialog.askstring("Comment", "Enter your comment:")

        if not reviewer or rating is None:
            return

        review = ReviewModel(reviewer_name=reviewer, rating=rating, comment=comment, movie=movie)
        session.add(review)
        session.commit()
        messagebox.showinfo("Success", "Review added successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieDatabaseApp(root)
    root.mainloop()
