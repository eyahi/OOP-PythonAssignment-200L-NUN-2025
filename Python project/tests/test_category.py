import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from models.category import Category

class TestCategory(unittest.TestCase):
    def test_edit_category(self):
        cat = Category("Food")
        cat.edit_category("Groceries")
        self.assertEqual(cat.name, "Groceries")

if __name__ == '__main__':
    unittest.main()