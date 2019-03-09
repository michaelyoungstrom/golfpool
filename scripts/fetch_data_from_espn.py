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
def get_latest_tournament_data(tournament_id):
    response = requests.get("http://www.espn.com/golf/leaderboard/_/tournamentId/{}".format(tournament_id))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tournament_name = soup.find("h1", "headline__h1 Leaderboard__Event__Title").text

        tournament_date = soup.find("span", "Leaderboard__Event__Date n7")
        tournament_year = tournament_date.text.split(", ")[1]

        # ESPN's leaderboard changes column-wise based on the day and time. Maintain
        # a dict to ensure we are tracking the data we want
        table_headers = soup.find("tr", "Table2__header-row Table2__tr Table2__even")
        table_columns = table_headers.find_all("th")
        table_value_to_column_dict = {
            "PLAYER" : None,
            "TO PAR" : None,
            "TODAY" : None,
            "THRU" : None,
            "R1" : None,
            "R2" : None,
            "R3" : None,
            "R4" : None
        }
        for index in range(0, len(table_columns)):
            if table_columns[index].text in table_value_to_column_dict:
                table_value_to_column_dict[table_columns[index].text] = index

        table_rows = soup.find_all("tr", class_="Table2__tr Table2__even")
        with io.open("testing.csv", "w") as csv_file:
            for row in table_rows:
                line_string = u"{}".format(tournament_id)
                for key in ["PLAYER", "TO PAR", "TODAY", "THRU", "R1", "R2", "R3", "R4"]:
                    table_index = table_value_to_column_dict[key]
                    if table_index is not None:
                        if key == "PLAYER":
                            link_to_player = row.contents[table_index].find("a", class_="leaderboard_player_name").get("href")
                            value = int(re.findall("\d+", link_to_player)[0])
                        else:
                            value = row.contents[table_index].text
                    else:
                        value = ""
                    line_string += ",{}".format(value)
                line_string += "\n"
                csv_file.write(line_string)

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
@click.option('--datatype', type=click.Choice(['tournament', 'players']), help='Method to run for pulling ESPN data.')
@click.option('--id', type=int, help='Tournament id')
def main(datatype, id):
    if datatype == "players":
        get_all_golfers()
    elif datatype == "tournament":
        get_latest_tournament_data(id)
    else:
        raise Exception("Please provide a valid datatype to pull.")

main()
