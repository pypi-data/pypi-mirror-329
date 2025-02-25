import unittest
from unittest.mock import patch
from report.cli import CLI  # Імпортуємо клас CLI

class TestCLI(unittest.TestCase):

    def setUp(self):
        # Створюємо екземпляр класу CLI перед кожним тестом
        self.cli = CLI()

    @patch('sys.argv', ['test_script', '--files', 'data/', '--asc'])
    def test_parse_ascending(self):
        # Тестуємо, чи правильно парситься аргумент --asc
        args = self.cli.parse()
        self.assertTrue(args.asc)
        self.assertEqual(args.files, 'data/')
        self.assertIsNone(args.driver)

    @patch('sys.argv', ['test_script', '--files', 'data/', '--desc'])
    def test_parse_descending(self):
        # Тестуємо, чи правильно парситься аргумент --desc
        args = self.cli.parse()
        self.assertTrue(args.desc)
        self.assertEqual(args.files, 'data/')
        self.assertIsNone(args.driver)

    @patch('sys.argv', ['test_script', '--files', 'data/', '--asc', '--desc'])
    def test_conflicting_args(self):
        # Тестуємо, чи правильно кидається помилка при конфлікті аргументів --asc і --desc
        with self.assertRaises(ValueError):
            self.cli.parse()

    @patch('sys.argv', ['test_script', '--files', 'data/', '--driver', 'Hamilton'])
    def test_driver_argument(self):
        # Тестуємо, чи правильно парситься аргумент --driver
        args = self.cli.parse()
        self.assertEqual(args.driver, 'Hamilton')
        self.assertEqual(args.files, 'data/')

if __name__ == '__main__':
    unittest.main()
