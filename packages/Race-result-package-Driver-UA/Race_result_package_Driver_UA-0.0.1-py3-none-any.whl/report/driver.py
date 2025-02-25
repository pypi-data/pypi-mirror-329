class Driver:
    """
    Клас для представлення гонщика.
    """
    def __init__(self, abbreviation, team, time):
        self.abbreviation = abbreviation  # абревіатура гонщика
        self.team = team                  # команда
        self.time = time                  # час

    def __str__(self):
        return f"{self.abbreviation} | {self.team} | {self.time.strftime('%M:%S.%f')[:-3]}"
