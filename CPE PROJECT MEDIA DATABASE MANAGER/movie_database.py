
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
import json, os

from movie import Movie
from review import Review

class MovieDatabase:
    def __init__(self):
        self.movies = {}
        self.load()

    def add_movie(self, title, director, genre, year, poster_path):
        self.movies[title] = Movie(title, director, genre, year, poster_path)

    def get_movie(self, title):
        return self.movies.get(title)

    def search_movies(self, keyword):
        return [m for m in self.movies.values() if keyword.lower() in m.title.lower()]

    def save(self):
        data = {
            t: vars(m) | {
                "reviews": [vars(r) for r in m.reviews],
                "poster_path": m.poster_path
            }
            for t, m in self.movies.items()
        }
        with open("movies.json", "w") as f:
            json.dump(data, f)

    def load(self):
        if not os.path.exists("movies.json"):
            return

        try:
            with open("movies.json") as f:
                data = json.load(f)
                for t, m in data.items():
                    release_year = m.get("release_year") or m.get("year", "Unknown")
                    poster_path = m.get("poster_path", None)
                    title = m.get("title", "Untitled")
                    director = m.get("director", "Unknown")
                    genre = m.get("genre", "Unknown")
                    movie = Movie(title, director, genre, release_year, poster_path)
                    for r in m.get("reviews", []):
                        movie.add_review(Review(r["reviewer_name"], r["rating"], r["comment"]))
                    self.movies[t] = movie
        except Exception as e:
            print("Error loading movies:", e)

# GUI
db = MovieDatabase()

def add_movie():
    title = simpledialog.askstring("Title", "Enter movie title:")
    if not title: return
    director = simpledialog.askstring("Director", "Enter director:")
    genre = simpledialog.askstring("Genre", "Enter genre:")
    year = simpledialog.askstring("Year", "Enter release year:")

    poster_path = filedialog.askopenfilename(
        title="Select Poster Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")]
    )

    db.add_movie(title, director, genre, year, poster_path)
    db.save()
    messagebox.showinfo("Success", "Movie added!")

def view_movies():
    for movie in db.movies.values():
        top = tk.Toplevel()
        top.title(movie.title)

        info = f"{movie.title} ({movie.release_year})\nDirector: {movie.director}\nGenre: {movie.genre}"
        tk.Label(top, text=info, font=("Arial", 12)).pack()

        if movie.poster_path and os.path.exists(movie.poster_path):
            try:
                img = Image.open(movie.poster_path)
                img.thumbnail((300, 400))
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(top, image=img_tk)
                img_label.image = img_tk
                img_label.pack()
            except Exception as e:
                tk.Label(top, text=f"Failed to load image: {e}").pack()

def search_movie():
    keyword = simpledialog.askstring("Search", "Enter title keyword:")
    results = db.search_movies(keyword)
    if results:
        msg = "\n\n".join([f"{m.title} ({m.release_year})" for m in results])
        messagebox.showinfo("Results", msg)
    else:
        messagebox.showinfo("Results", "No movies found.")

def add_review():
    title = simpledialog.askstring("Movie Title", "Enter movie title:")
    movie = db.get_movie(title)
    if not movie:
        messagebox.showerror("Error", "Movie not found.")
        return
    reviewer = simpledialog.askstring("Name", "Enter your name:")
    rating = simpledialog.askstring("Rating", "Enter rating (1-5):")
    comment = simpledialog.askstring("Comment", "Enter review comment:")
    movie.add_review(Review(reviewer, rating, comment))
    db.save()
    messagebox.showinfo("Success", "Review added!")

root = tk.Tk()
root.title("Movie Database")

tk.Button(root, text="Add Movie", command=add_movie).pack(pady=5)
tk.Button(root, text="View Movies", command=view_movies).pack(pady=5)
tk.Button(root, text="Search Movies", command=search_movie).pack(pady=5)
tk.Button(root, text="Add Review", command=add_review).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()
