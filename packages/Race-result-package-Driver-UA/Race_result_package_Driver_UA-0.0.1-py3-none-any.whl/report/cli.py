import argparse

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Generate a Formula 1 race report")
        self.parser.add_argument('--files', required=True, help="Path to the data folder")
        self.parser.add_argument('--asc', action='store_true', help="Sort results in ascending order")
        self.parser.add_argument('--desc', action='store_true', help="Sort results in descending order")
        self.parser.add_argument('--driver', help="Specify a driver to show detailed report")

    def parse(self):
        """Парсить аргументи командного рядка"""
        args = self.parser.parse_args()
        if args.asc and args.desc:
            raise ValueError("You cannot use both --asc and --desc at the same time.")
        if not args.asc and not args.desc:
            args.asc = True  # За замовчуванням сортуємо за зростанням
        return args
