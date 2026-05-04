import json
import os


class Book:
    def __init__(self, title, author, genre, pages):
        self.title = title
        self.author = author
        self.genre = genre
        self.pages = pages

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "pages": self.pages
        }

    @staticmethod
    def from_dict(data):
        return Book(data["title"], data["author"], data["genre"], data["pages"])


class BookTracker:
    def __init__(self, filename="books.json"):
        self.filename = filename
        self.books = []

    def load_books(self):
        """Загружает книги из JSON-файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(b) for b in data]
            except (json.JSONDecodeError, KeyError, TypeError):
                self.books = []
        else:
            self.books = []

    def save_books(self):
        """Сохраняет книги в JSON-файл"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4, ensure_ascii=False)

    def add_book(self, title, author, genre, pages):
        """Добавляет новую книгу, проверяет на дубликаты"""
        # Проверка на дубликат
        for book in self.books:
            if book.title.lower() == title.lower() and book.author.lower() == author.lower():
                return False, "Такая книга уже есть в списке"

        book = Book(title, author, genre, pages)
        self.books.append(book)
        self.save_books()
        return True, "Книга добавлена"

    def get_filtered_books(self, genre_filter=None, pages_min=None):
        """Возвращает отфильтрованный список книг"""
        result = self.books

        if genre_filter:
            result = [b for b in result if genre_filter.lower() in b.genre.lower()]

        if pages_min is not None:
            result = [b for b in result if b.pages > pages_min]

        return result