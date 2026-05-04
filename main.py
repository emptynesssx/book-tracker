# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from book_tracker import BookTracker


class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Мои прочитанные книги")
        self.root.geometry("800x550")

        # Создаём экземпляр трекера
        self.tracker = BookTracker("books.json")

        # Создаём все элементы интерфейса
        self.create_widgets()

        # Загружаем данные
        self.load_and_refresh()

    def create_widgets(self):
        """Создаёт все элементы интерфейса"""

        # === Рамка для ввода данных ===
        input_frame = tk.LabelFrame(self.root, text="Добавление новой книги", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Название
        tk.Label(input_frame, text="Название книги:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Автор
        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.author_entry = tk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        # Жанр
        tk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.genre_entry = tk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        # Страницы
        tk.Label(input_frame, text="Количество страниц:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.pages_entry = tk.Entry(input_frame, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_btn = tk.Button(input_frame, text="➕ Добавить книгу", command=self.add_book, bg="#4CAF50", fg="white")
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # === Рамка для фильтров ===
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация книг", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5)
        self.genre_filter_entry = tk.Entry(filter_frame, width=20)
        self.genre_filter_entry.grid(row=0, column=1, padx=5)
        self.genre_filter_entry.bind("<KeyRelease>", self.apply_filters)

        tk.Label(filter_frame, text="Страниц больше:").grid(row=1, column=0, padx=5, pady=5)
        self.pages_filter_entry = tk.Entry(filter_frame, width=10)
        self.pages_filter_entry.grid(row=1, column=1, padx=5, sticky="w")
        self.pages_filter_entry.bind("<KeyRelease>", self.apply_filters)

        # === Таблица для отображения книг ===
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создаём таблицу
        self.tree = ttk.Treeview(table_frame, columns=("Название", "Автор", "Жанр", "Страницы"), show="headings")

        # Настройка заголовков
        self.tree.heading("Название", text="📖 Название")
        self.tree.heading("Автор", text="✍️ Автор")
        self.tree.heading("Жанр", text="📚 Жанр")
        self.tree.heading("Страницы", text="📄 Страницы")

        # Настройка ширины колонок
        self.tree.column("Название", width=250)
        self.tree.column("Автор", width=150)
        self.tree.column("Жанр", width=120)
        self.tree.column("Страницы", width=80, anchor="center")

        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Размещаем таблицу и скроллбар
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_and_refresh(self):
        """Загружает данные и обновляет таблицу"""
        self.tracker.load_books()
        self.apply_filters()

    def add_book(self):
        """Обработчик добавления книги с валидацией"""
        # Получаем данные из полей
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()

        # Валидация: проверяем заполнение полей
        if not title:
            messagebox.showerror("Ошибка", "Введите название книги")
            return
        if not author:
            messagebox.showerror("Ошибка", "Введите автора")
            return
        if not genre:
            messagebox.showerror("Ошибка", "Введите жанр")
            return
        if not pages_str:
            messagebox.showerror("Ошибка", "Введите количество страниц")
            return

        # Валидация: проверяем, что страницы - это число
        try:
            pages = int(pages_str)
            if pages <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть больше 0")
                return
            if pages > 10000:
                messagebox.showerror("Ошибка", "Слишком много страниц (максимум 10000)")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть целым числом")
            return

        # Добавляем книгу
        success, message = self.tracker.add_book(title, author, genre, pages)

        if success:
            # Очищаем поля
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.pages_entry.delete(0, tk.END)

            # Обновляем таблицу
            self.apply_filters()
            messagebox.showinfo("Успех", message)
        else:
            messagebox.showerror("Ошибка", message)

    def apply_filters(self, event=None):
        """Применяет фильтры и обновляет таблицу"""
        genre_filter = self.genre_filter_entry.get().strip()
        pages_filter_str = self.pages_filter_entry.get().strip()

        # Преобразуем фильтр страниц в число, если он не пустой
        pages_min = None
        if pages_filter_str:
            try:
                pages_min = int(pages_filter_str)
                if pages_min < 0:
                    pages_min = 0
            except ValueError:
                pages_min = None

        # Получаем отфильтрованные книги
        filtered_books = self.tracker.get_filtered_books(genre_filter, pages_min)

        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Заполняем таблицу
        for book in filtered_books:
            self.tree.insert("", tk.END, values=(book.title, book.author, book.genre, book.pages))

        # Обновляем статус
        count = len(filtered_books)
        self.root.title(f"Book Tracker - Найдено книг: {count}")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()