
import os

class DiaryEntry:
    def __init__(self, title, content):
        self.title = title.strip()
        self.content = content.strip()

    def save(self):
        if not self.title:
            raise ValueError("Title cannot be empty.")
        with open(f"entries/{self.title}.txt", "w", encoding="utf-8") as file:
            file.write(self.content)

class DiaryManager:
    def __init__(self, directory="entries"):
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def list_entries(self):
        return [file[:-4] for file in os.listdir(self.directory) if file.endswith(".txt")]

    def load_entry(self, title):
        try:
            with open(f"{self.directory}/{title}.txt", "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return ""

    def delete_entry(self, title):
        path = f"{self.directory}/{title}.txt"
        if os.path.exists(path):
            os.remove(path)
