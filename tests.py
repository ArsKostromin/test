import unittest
from Library import Book


class TestBook(unittest.TestCase):
    def test_book_initialization(self):
        book = Book("test title", "test author", 2020)
        self.assertEqual(book.title, "test title")
        self.assertEqual(book.year, 2020)
        self.assertEqual(book.author, "test author")
        self.assertEqual(book.status, "в наличии")
        self.assertIsInstance(book.id, int)

    def test_book_to_dict(self):
        book = Book("Test Title", "Test Author", 2023)
        book_dict = book.to_dict()
        expected_dict = {
            "id": book.id,
            "title": "Test Title",
            "author": "Test Author",
            "year": 2023,
            "status": "в наличии",
        }
        self.assertEqual(book_dict, expected_dict)
        
    def test_book_from_dict(self):
        """Тестирует восстановление объекта книги из словаря"""
        book_data = {
            "id": 12345,
            "title": "Restored Title",
            "author": "Restored Author",
            "year": 2021,
            "status": "выдана",
        }
        book = Book.from_dict(book_data)
        self.assertEqual(book.id, 12345)
        self.assertEqual(book.title, "Restored Title")
        self.assertEqual(book.author, "Restored Author")
        self.assertEqual(book.year, 2021)
        self.assertEqual(book.status, "выдана")

if __name__ == "__main__":
    unittest.main()