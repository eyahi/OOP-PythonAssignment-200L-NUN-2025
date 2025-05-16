import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db import add_user, get_user_id
import unittest
from models.report import Report

class TestReport(unittest.TestCase):
    def setUp(self):
        self.username = "tester"
        self.password = "password123"
        if get_user_id(self.username) is None:
            add_user("Victory", "ezioauditore")

    def test_report_init(self):
        report = Report("Victory")
        self.assertEqual(report.username, "Victory")
        self.assertIsNotNone(report.user_id)

if __name__ == '__main__':
    unittest.main()
