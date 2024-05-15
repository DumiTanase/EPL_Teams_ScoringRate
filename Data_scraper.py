import requests
from bs4 import BeautifulSoup
import datetime as dt


class FootballData:
    def __init__(self, months):
        self.months = months
        self.raw_text = []
        self.now = dt.date.today()
        self.month_to_format = self.now.month
        self.current_month = "{:02d}".format(self.month_to_format)
        self.current_year = self.now.year
        self.NAME = "?filter=results"
        self.year = 2023

    def scrape_data(self):
        for month in self.months:
            # Adjusting the year if month is December
            url = f"https://www.bbc.co.uk/sport/football/premier-league/scores-fixtures/{self.year}-{month}"
            if month == "12":
                self.year = self.current_year
                response = requests.get(f"{url}")
            else:
                response = requests.get(f"{url}")
            if month == str(self.current_month):
                response = requests.get(f"{url}{self.NAME}")
            html_text = response.text
            soup = BeautifulSoup(html_text, "html.parser")
            content = soup.find_all(name="div", class_="ssrcss-1jkg1a7-HeaderWrapper e4zdov50")
            for element in content:
                content_2 = element.find_all(name="div", class_="ssrcss-j8sqox-StyledHeadToHead e64wp3e0")
                for i in content_2:
                    content_3 = i.find(name="span",
                                           class_="visually-hidden ssrcss-1f39n02-VisuallyHidden e16en2lz0")
                    self.raw_text.append(content_3.get_text())
            if month == str(self.current_month):
                break

    def save_to_csv(self, filename):
        with open(filename, mode="w") as file:
            for item in self.raw_text:
                file.write(item)

