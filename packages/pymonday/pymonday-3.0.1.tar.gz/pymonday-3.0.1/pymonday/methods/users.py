# pymonday/methods/users.py

########################################################################################################################
# USERS CLASS
########################################################################################################################
class Users:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def get_all_users(self):
        """
        Get the names of all platform users and their UUIDs
        :return: Dictionary of item IDs and usernames. Return None or error message on API call failure.
        """
        query_string = f'''query {{users(limit: 200) {{id name email phone country_code created_at last_activity}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            user_data = response['data']['users']
            return {item['id']: item['name'] for item in user_data}
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_user_info(self, user_id):
        """
        Get all details of a specific user. One UUID permitted per query.
        :param user_id: UUID of the User.
        :return: Dictionary containing user specific information. Return None or error message on API call failure.
        """
        query_string = f'''query {{
        users(ids: {user_id}) {{id name email phone country_code created_at last_activity}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            user_data = response['data']['users'][0]
            return user_data
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def add_user_to_board(self, board_id, user_ids):
        """
        Add users to a board as subscribers.
        :param board_id: UUID of the board. Single Integer value.
        :param user_ids: UUIDs of the users to add. Should be a list of integers.
        :return: List containing the IDs of the newly added users. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{
        add_users_to_board (board_id: {board_id}, user_ids: {user_ids}, kind: subscriber) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            return response['data']['add_users_to_board']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def remove_user_from_board(self, board_id, user_ids):
        """
        Remove users from a board as subscribers.
        :param board_id: UUID of the board. Single Integer value.
        :param user_ids: UUIDs of the users to remove. Should be a list of integers.
        :return: True if successful. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{
            delete_subscribers_from_board (board_id: {board_id}, user_ids: {user_ids}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            if response['data']['delete_subscribers_from_board']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################