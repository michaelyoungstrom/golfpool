import requests
import io
import re
import click
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from players.models import Player

"""
Provides methods that pull data from ESPN and parses it into
a format that can be used with this application. It makes some assumptions
based on the UI which may be subject to change in the future.
"""
class Command(BaseCommand):
    help = 'Fetch data from the ESPN website'

    def add_arguments(self, parser):
        parser.add_argument('datatype', help="Id of the tournament to update", choices=["tournament", "all_players", "player"])
        parser.add_argument('id', help="Id for either tournament or player", nargs="?", default=None)

    def get_latest_tournament_data(self, tournament_id):
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

    def get_all_golfers(self):
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

    def get_golfer_by_id(self, player_id):
        """
        Extracts data from a golfer based on their player_id. Looks like the
        table on ESPN doesn't include every golfer that could potentially show
        up in a tournament.
        """
        response = requests.get("http://www.espn.com/golf/player/_/id/{}/".format(player_id))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            mod_content = soup.find("div", class_="mod-content")
            player_bio = mod_content.find("div", class_="player-bio")

            player_name_full = mod_content.find("h1").text

            first_name = player_name_full.split(' ')[0]
            last_name = " ".join(player_name_full.split(' ')[1:])
            country = player_bio.find("ul", class_="general-info").find("li", class_="first").text

            try:
                existing_player = Player.objects.object(
                    player_id=player_id
                )
                print("Golfer with id: {} already exists".format(player_id))
            except:
                new_player = Player(
                    player_id=player_id,
                    first_name=first_name,
                    last_name=last_name,
                    country=country
                )
                new_player.save()
                print("{} {} added to the players database".format(first_name, last_name))
        else:
            raise ValueError(
                "Could not find a player by id: {}".format(player_id)
            )

    def handle(self, *args, **options):
        datatype = options['datatype']
        id = options['id']

        if datatype == "all_players":
            self.get_all_golfers()
        elif datatype == "tournament":
                self.get_latest_tournament_data(id)
        elif datatype == "player":
            self.get_golfer_by_id(id)
        else:
            raise Exception("Please provide a valid datatype to pull.")
