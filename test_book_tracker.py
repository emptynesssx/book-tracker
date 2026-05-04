# test_book_tracker.py
import unittest
import os
import json
from book_tracker import BookTracker, Book


class TestBookTracker(unittest.TestCase):

    def setUp(self):
        """Создаём временный файл для тестов"""
        self.test_file = "test_books.json"
        self.tracker = BookTracker(self.test_file)

    def tearDown(self):
        """Удаляем временный файл после тестов"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # === ПОЗИТИВНЫЕ ТЕСТЫ ===

    def test_add_book_success(self):
        """Тест успешного добавления книги"""
        result, message = self.tracker.add_book("Тестовая книга", "Тестовый автор", "Тестовый жанр", 100)
        self.assertTrue(result)
        self.assertEqual(len(self.tracker.books), 1)

    def test_load_saved_books(self):
        """Тест загрузки сохранённых книг"""
        self.tracker.add_book("Книга1", "Автор1", "Жанр1", 200)

        # Создаём новый трекер и загружаем данные
        new_tracker = BookTracker(self.test_file)
        new_tracker.load_books()

        self.assertEqual(len(new_tracker.books), 1)
        self.assertEqual(new_tracker.books[0].title, "Книга1")

    def test_filter_by_genre(self):
        """Тест фильтрации по жанру"""
        self.tracker.add_book("Книга1", "Автор1", "Фантастика", 300)
        self.tracker.add_book("Книга2", "Автор2", "Детектив", 250)
        self.tracker.add_book("Книга3", "Автор3", "Фантастика", 400)

        filtered = self.tracker.get_filtered_books(genre_filter="Фантастика")
        self.assertEqual(len(filtered), 2)

    def test_filter_by_pages(self):
        """Тест фильтрации по страницам"""
        self.tracker.add_book("Маленькая", "Автор1", "Жанр1", 100)
        self.tracker.add_book("Средняя", "Автор2", "Жанр2", 250)
        self.tracker.add_book("Большая", "Автор3", "Жанр3", 500)

        filtered = self.tracker.get_filtered_books(pages_min=200)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(book.pages > 200 for book in filtered))

    def test_combined_filters(self):
        """Тест комбинированной фильтрации"""
        self.tracker.add_book("Книга1", "Автор1", "Фантастика", 300)
        self.tracker.add_book("Книга2", "Автор2", "Фантастика", 100)
        self.tracker.add_book("Книга3", "Автор3", "Детектив", 300)

        filtered = self.tracker.get_filtered_books(genre_filter="Фантастика", pages_min=200)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "Книга1")

    # === НЕГАТИВНЫЕ ТЕСТЫ ===

    def test_add_duplicate_book(self):
        """Тест добавления дубликата книги"""
        self.tracker.add_book("Дубликат", "Автор", "Жанр", 100)
        result, message = self.tracker.add_book("Дубликат", "Автор", "Жанр", 100)

        self.assertFalse(result)
        self.assertIn("уже есть", message)

    def test_load_corrupted_json(self):
        """Тест загрузки повреждённого JSON"""
        with open(self.test_file, "w") as f:
            f.write("this is not valid json {")

        self.tracker.load_books()
        self.assertEqual(self.tracker.books, [])

    # === ГРАНИЧНЫЕ ТЕСТЫ ===

    def test_empty_filters(self):
        """Тест с пустыми фильтрами"""
        self.tracker.add_book("Книга1", "Автор1", "Жанр1", 100)
        self.tracker.add_book("Книга2", "Автор2", "Жанр2", 200)

        filtered = self.tracker.get_filtered_books(genre_filter="", pages_min=None)
        self.assertEqual(len(filtered), 2)

    def test_one_page_book(self):
        """Тест книги с 1 страницей"""
        result, _ = self.tracker.add_book("Мини-книга", "Автор", "Жанр", 1)
        self.assertTrue(result)

        filtered = self.tracker.get_filtered_books(pages_min=0)
        self.assertEqual(len(filtered), 1)

        filtered = self.tracker.get_filtered_books(pages_min=1)
        self.assertEqual(len(filtered), 0)

    def test_very_large_pages(self):
        """Тест книги с очень большим количеством страниц"""
        result, _ = self.tracker.add_book("Том", "Автор", "Жанр", 5000)
        self.assertTrue(result)

        filtered = self.tracker.get_filtered_books(pages_min=4999)
        self.assertEqual(len(filtered), 1)


if __name__ == "__main__":
    unittest.main()