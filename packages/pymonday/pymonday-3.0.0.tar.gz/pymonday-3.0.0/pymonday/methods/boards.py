# pymonday/methods/boards.py

########################################################################################################################
# BOARDS CLASS
########################################################################################################################
class Boards:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def get_all_boards(self):
        """
        Get all boards from the platform.
        :return: Dictionary containing Board IDs and Board Names. Return None or error message on API call failure.
        """
        query_string = f'''
            query {{boards(limit: 1000) {{name id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            board_data = response['data']['boards']
            return {item['id']: item['name'] for item in board_data}
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_board_info(self, board_id):
        """
        Get the following information from a board: Name, ID, State, Permissions, Type, Workspace.
        :param board_id: UUID of the board.
        :return: Dictionary containing above values. Return None or error message on API call failure.
        """
        query_string = f'''
            query {{boards (ids: {board_id}) {{name state id permissions board_kind workspace_id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['boards'][0]
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_board_groups(self, board_id):
        """
        Get all groups of a specific board.
        :param board_id: UUID of the board.
        :return: Dictionary containing Group IDs and Group Names. Return None or error message on API call failure.
        """
        query_string = f'''
            query {{boards (ids: {board_id}) {{groups {{id title}}}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            group_data = response['data']['boards'][0]['groups']
            return {item['title']: item['id'] for item in group_data}
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_board_from_item(self, item_id):
        """
        Get UUID of the board an item is on.
        :param item_id: UUID of the item.
        :return: Dictionary containing Board IDs and Board Names. Return None or error message on API call failure.
        """
        query_string = f'''
            query {{items(ids: {item_id}){{board{{id name}}}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['items'][0]['board']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def create_board(self, board_name, board_type, workspace_id):
        """
        Create a new board within a specific workspace.
        :param board_name: Required. The Name of the new board
        :param board_type: Required. Board Visibility. Options: public, private, share
        :param workspace_id: Required. UUID of the workspace to create the board in
        :return: UUID of newly created board. Return None or error message on API call failure.
        """
        query_string = f'''mutation 
            {{create_board (board_name: "{board_name}", board_kind: {board_type}, workspace_id: {workspace_id}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['create_board']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def delete_board(self, board_id):
        """
        Delete a board.
        :param board_id: UUID of the board to delete.
        :return: True if successful. Return None or error message on API call failure.
        """
        query_string = f'''mutation 
                    {{delete_board (board_id: {board_id}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None

        try:
            if response['data']['delete_board']['id']:
                return True
        except (TypeError, KeyError, IndexError):
            return response


    ####################################################################################################################
    def update_board_description(self, board_id, description):
        """
        Update the description of a specific board.
        :param board_id: UUID of the board to update.
        :param description: Text String to be used as the board description.
        :return: Response from the API. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{
            update_board(board_id: {board_id}, board_attribute: description, new_value: "{description}")}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['update_board']
        except (TypeError, KeyError, IndexError):
            return None


    ####################################################################################################################
    def archive_board(self, board_id):
        """
        Archive a board.
        :param board_id: UUID of the board to archive.
        :return: True if successful. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{archive_board (board_id: {board_id}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            if response['data']['archive_board']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response


    ####################################################################################################################
    # New - duplicate_board
    def duplicate_board(self, board_id, duplicate_type='duplicate_board_with_structure', board_name=None,
                        keep_subscribers=False, workspace_id=None, folder_id=None):
        """
        Duplicate a board with its items and groups.
        :param board_id: The unique identifier of the board to duplicate.
        :param duplicate_type: The duplication type. Options are:
                               'duplicate_board_with_structure',
                               'duplicate_board_with_pulses',
                               'duplicate_board_with_pulses_and_updates'.
                               Default is 'duplicate_board_with_structure'.
        :param board_name: Optional new name for the duplicated board. If omitted, it will be automatically generated.
        :param keep_subscribers: Boolean indicating whether to duplicate the subscribers to the new board. Defaults to False.
        :param workspace_id: Optional ID of the destination workspace. If omitted, it will default to the original board's workspace.
        :param folder_id: Optional ID of the destination folder within the destination workspace. Required if duplicating to another workspace; otherwise, optional.
        :return: New board UUID. Return None or error message on API call failure.
        """
        mutation = f'''mutation {{duplicate_board (board_id: {board_id}, duplicate_type: {duplicate_type.lower()}
        {f', board_name: "{board_name}"' if board_name else ''} {f', keep_subscribers: {str(keep_subscribers).lower()}'}
        {f', workspace_id: {workspace_id}' if workspace_id else ''} {f', folder_id: {folder_id}' if folder_id else ''}) 
        {{board {{id name}}}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['duplicate_board']['board']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - get_board_views
    def get_board_views(self, board_id):
        """
        Retrieve the views of a specific board.
        Required Scope: `boards:read`
        :param board_id: ID of the board whose views are to be retrieved.
        :return: List of board views or None if the request fails. Return None or error message on API call failure.
        """
        query = f'''query {{boards(ids: {board_id}) {{views {{id name type settings_str view_specific_data_str}}}}}}'''
        payload = {"query": query}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None

        try:
            return response["data"]["boards"][0]["views"]
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################