# pymonday/methods/teams.py

########################################################################################################################
# TEAMS CLASS
########################################################################################################################
class Teams:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def get_teams(self):
        """
        Get Names and IDs of all teams.
        :return: Dictionary of IDs and Names. Return None or error message on API call failure.
        """
        query_string = f'''{{teams {{name id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            team_data = response['data']['teams']
            teams = {item['id']: item['name'] for item in team_data}
            return teams
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_team_members(self, team_ids):
        """
        Get ID, Name & Email of team members.
        :param team_ids: UUIDs of the Teams to be retrieved. List of integers.
        :return: Dictionary of Teams and member data. Return None or error message on API call failure.
        """
        query_string = f'''{{teams (ids: {team_ids}){{name users {{name id email}}}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            member_data = response['data']['teams']
            team_dictionary = {item['name']: item['users'] for item in member_data}
            return team_dictionary
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################