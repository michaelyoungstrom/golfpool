import requests
import io
import re
import click
from bs4 import BeautifulSoup

"""
This script provides methods that pull data from ESPN and parses it into
a format that can be used with this application. It makes some assumptions
based on the UI which may be subject to change in the future.
"""
def get_latest_tournament_data():
    response = requests.get("http://www.espn.com/golf/leaderboard")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tournament_name = soup.find("h1", "headline__h1 Leaderboard__Event__Title").text

        tournament_date = soup.find("span", "Leaderboard__Event__Date n7")
        tournament_year = tournament_date.text.split(", ")[1]

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

def get_all_golfers():
    """
    Gets all of the golfers that are registered at ESPN.
    """
    response = requests.get("http://www.espn.com/golf/players")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        player_rows = soup.find_all("tr", class_=(lambda row: row and 'row player' in row))
        for player in player_rows:
            comma_name = player.contents[0].text.split(", ")
            player_id_list = re.findall("\d+", str(player.contents[0].a))
            player_id = int(''.join(str(num) for num in player_id_list))
            first_name = comma_name[1]
            last_name = comma_name[0]
            country = player.contents[1].text

@click.command()
@click.option('--datatype', type=click.Choice(['latest_tournament', 'players']), help='Method to run for pulling ESPN data.')
def main(datatype):
    if datatype == "players":
        get_all_golfers()
    elif datatype == "latest_tournament":
        get_latest_tournament_data()
    else:
        raise Exception("Please provide a valid datatype to pull.")

main()
