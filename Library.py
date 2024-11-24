import json
from typing import List, Dict, Optional


class Book:
    def __init__(self, title: str, author: str, year: int): #Инициализация 
        self.id = id(self)
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def to_dict(self) -> Dict: #Преобразует объект книги в словарь
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @classmethod #делает метод привязанным к классу, а не к конкретному экземпляру.
    def from_dict(cls, data: Dict): #перевод из dict 
        book = cls(data["title"], data["author"], data["year"])
        book.id = data["id"]
        book.status = data["status"]
        return book


class Library:
    def __init__(self, storage_file: str = "library.json"): #Инициализация 
        self.storage_file = storage_file #файл
        self.books: List[Book] = self.load_books() #список книг

    def load_books(self) -> List[Book]: #достаёт книги из json
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data] #преобразуем в объекты Book.
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self): # сохранение текущего состояния библиотеки в файл json
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        book = Book(title, author, year)
        self.books.append(book)
        self.save_books()
        print(f"Книга '{title}' добавлена с ID {book.id}.")

    def delete_book(self, book_id: int):
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_books(self, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None):
        results = [
            book
            for book in self.books
            if (title is None or title.lower() in book.title.lower())
            and (author is None or author.lower() in book.author.lower())
            and (year is None or book.year == year)
        ]
        if results:
            for book in results:
                self.display_book(book)
        else:
            print("Книги не найдены.")

    def display_books(self): #вывод всех книг
        if not self.books:
            print("Библиотека пуста.")
        else:
            for book in self.books:
                self.display_book(book)

    def change_book_status(self, book_id: int, new_status: str): #изменяет статус книги
        book = self.find_book_by_id(book_id)
        if book:
            if new_status in ["в наличии", "выдана"]:
                book.status = new_status
                self.save_books()
                print(f"Статус книги с ID {book_id} изменён на '{new_status}'.")
            else:
                print("Неверный статус. Используйте 'в наличии' или 'выдана'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        return next((book for book in self.books if book.id == book_id), None)

    @staticmethod
    def display_book(book: Book):
        print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")



def main():
    library = Library()

    while True:
        print("\nВыберите действие:")
        print("1: Добавить книгу")
        print("2: Удалить книгу")
        print("3: Поиск книги")
        print("4: Показать все книги")
        print("5: Изменить статус книги")
        print("6: Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            library.add_book(title, author, year)

        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            library.delete_book(book_id)

        elif choice == "3":
            title = input("Введите название книги (оставьте пустым для пропуска): ") or None
            author = input("Введите автора книги (оставьте пустым для пропуска): ") or None
            year = input("Введите год издания книги (оставьте пустым для пропуска): ")
            year = int(year) if year else None
            library.find_books(title, author, year)

        elif choice == "4":
            library.display_books()

        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.change_book_status(book_id, new_status)

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
