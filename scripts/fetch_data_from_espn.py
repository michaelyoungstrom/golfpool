import requests
import io
from bs4 import BeautifulSoup

"""
This script pulls data from the ESPN leaderboard and parses it into
a format that can be used with this application.
"""
def fetch_data_from_espn():
    response = requests.get("http://www.espn.com/golf/leaderboard")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tournament_name = soup.find("h1", "headline__h1 Leaderboard__Event__Title").text

        tournament_date = soup.find("span", "Leaderboard__Event__Date n7")
        tournament_year = tournament_date.text.split(",")[1].strip(" ")

        table_rows = soup.find_all("tr", class_="Table2__tr Table2__even")
        with io.open("testing.csv", "w") as csv_file:
            for row in table_rows:
                player = row.contents[1].text
                first = row.contents[5].text
                second = row.contents[6].text
                third = row.contents[7].text
                fourth = row.contents[8].text
                csv_file.write(u"{},{},{},{},{},{},{}\n".format(
                    tournament_name,
                    tournament_year,
                    player,
                    first,
                    second,
                    third,
                    fourth
                ))

fetch_data_from_espn()
