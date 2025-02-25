class ReportBuilder:
    def __init__(self, race_result):
        self.race_result = race_result

    def build_report(self, top_n=15, ascending=True):
        """
        Створює звіт про гонку.

        :param top_n: Кількість топ-гонщиків у звіті.
        :param ascending: Сортувати за зростанням, якщо True, або за спаданням.
        :return: Текстовий звіт.
        """
        sorted_results = self.race_result.get_sorted_results(ascending)
        report = []

        for i, result in enumerate(sorted_results[:top_n]):
            # Форматуємо час у вигляді MM:SS.mmm
            minutes, seconds = divmod(result["time"].total_seconds(), 60)
            milliseconds = result["time"].microseconds // 1000
            formatted_time = f"{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"
            report.append(f"{i+1}. {result['name']} | {result['team']} | {formatted_time}")

        report.append("-" * 72)
        for i, result in enumerate(sorted_results[top_n:], start=top_n + 1):
            minutes, seconds = divmod(result["time"].total_seconds(), 60)
            milliseconds = result["time"].microseconds // 1000
            formatted_time = f"{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"
            report.append(f"{i}. {result['name']} | {result['team']} | {formatted_time}")

        return "\n".join(report)

    def build_driver_report(self, driver_abbreviation):
        """
        Створює детальний звіт для конкретного гонщика.

        :param driver_abbreviation: Абевіатура гонщика.
        :return: Текстовий звіт для конкретного гонщика.
        """
        # Шукаємо гонщика в результатах
        driver_result = None
        for result in self.race_result.results:
            if result['name'] == driver_abbreviation:
                driver_result = result
                break

        if not driver_result:
            return f"Гонщик з абревіатурою {driver_abbreviation} не знайдений у результатах."

        # Форматуємо час для гонщика
        minutes, seconds = divmod(driver_result["time"].total_seconds(), 60)
        milliseconds = driver_result["time"].microseconds // 1000
        formatted_time = f"{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"

        # Формуємо звіт
        report = f"Звіт для гонщика {driver_abbreviation}:\n"
        report += f"Ім'я: {driver_result['name']}\n"
        report += f"Команда: {driver_result['team']}\n"
        report += f"Час: {formatted_time}\n"

        return report
