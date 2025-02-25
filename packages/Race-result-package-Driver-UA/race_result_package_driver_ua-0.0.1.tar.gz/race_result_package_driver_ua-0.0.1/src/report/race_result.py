import datetime
from typing import List, Dict

class RaceResult:
    def __init__(self, start_file: str, end_file: str, abbreviation_file: str):
        self.start_file = start_file
        self.end_file = end_file
        self.abbreviation_file = abbreviation_file
        self.results = []

    def parse_log_file(self, file_path: str) -> Dict[str, datetime.datetime]:
        data = {}
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    abbreviation = line[:3]
                    time_str = line[3:]
                    time_obj = datetime.datetime.strptime(time_str, "%Y-%m-%d_%H:%M:%S.%f")
                    data[abbreviation] = time_obj
        return data

    def parse_abbreviation_file(self, file_path: str) -> Dict[str, Dict[str, str]]:
        abbreviations = {}
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("_")
                if len(parts) == 3:
                    abbreviation, name, team = parts
                    abbreviations[abbreviation] = {"name": name, "team": team}
        return abbreviations

    def collect_data(self):
        start_data = self.parse_log_file(self.start_file)
        end_data = self.parse_log_file(self.end_file)
        abbreviations = self.parse_abbreviation_file(self.abbreviation_file)

        self.results = []
        for abbreviation, start_time in start_data.items():
            if abbreviation in end_data:
                end_time = end_data[abbreviation]
                duration = end_time - start_time
                if abbreviation in abbreviations:
                    name = abbreviations[abbreviation]["name"]
                    team = abbreviations[abbreviation]["team"]
                    self.results.append({"name": name, "team": team, "time": duration})

    def get_sorted_results(self, ascending: bool = True) -> List[Dict[str, str]]:
        """
        Повертає результати, відсортовані за часом.

        :param ascending: Сортувати за зростанням, якщо True. Інакше — за спаданням.
        :return: Список словників із даними про гонщиків.
        """
        return sorted(self.results, key=lambda x: x["time"], reverse=not ascending)
