# pymonday/methods/groups.py

########################################################################################################################
# GROUPS CLASS
########################################################################################################################
class Groups:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def create_group(self, board_id, group_name):
        """
        Create a new group on a board at the top position.
        :param board_id: UUID of the board to create the item on.
        :param group_name: Name of the new group to be created.
        :return: UUID of the newly created group. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{create_group (board_id: {board_id}, group_name: "{group_name}") {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None

        try:
            return response['data']['create_group']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def delete_group(self, board_id, group_id):
        """
        Delete a group from a board.
        :param board_id: UUID of the board to delete the group from.
        :param group_id: UUID of the group to delete.
        :return: True if successful. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{delete_group (board_id: {board_id}, group_id: "{group_id}") {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            if response['data']['delete_group']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def move_item_to_group(self, item_id, group_id):
        """
        Move an item from one group in a board to another.
        :param item_id: UUID of the item to move.
        :param group_id: UUID of the group to move the item to.
        :return: UUID of the moved item. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{move_item_to_group (item_id: {item_id}, group_id: "{group_id}") {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None

        try:
            return response['data']['move_item_to_group']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - update_group
    def update_group(self, board_id, group_id, group_attribute, new_value):
        """
        Update an attribute of an existing group.
        :param board_id: ID of the board.
        :param group_id: ID of the group to update.
        :param group_attribute: Attribute to update ('title', 'color', 'position').
        :param new_value: New value for the attribute.
        :return: UUID of the updated group. Return None or error message on API call failure.
        """
        mutation = f'''mutation {{update_group (board_id: {board_id}, group_id: "{group_id}", group_attribute: 
        {group_attribute}, new_value: "{new_value}") {{id}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['update_group']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - duplicate_group
    def duplicate_group(self, board_id, group_id, add_to_top=True):
        """
        Duplicate an existing group within a board.
        :param board_id: ID of the board.
        :param group_id: ID of the group to duplicate.
        :param add_to_top: Boolean to add the new group to the top of the board.
        :return: UUID of the duplicated group. Return None or error message on API call failure.
        """
        mutation = (f'mutation {{ duplicate_group (board_id: {board_id}, group_id: "{group_id}", add_to_top: '
                    f'{str(add_to_top).lower()}) {{ id }} }}')
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['duplicate_group']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - archive_group
    def archive_group(self, board_id, group_id):
        """
        Archive an existing group within a board.
        :param board_id: The ID of the board where the group exists.
        :param group_id: The ID of the group to be archived.
        :return: True if the group is successfully archived. Return None or error message if the request fails.
        """
        query = f'''
        mutation {{
            archive_group (board_id: {board_id}, group_id: "{group_id}") {{
                id
            }}
        }}
        '''
        payload = {'query': query}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            if response['data']['archive_group']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - is_group_empty()
    def is_group_empty(self, board_id, group_id):
        """
        Check if a group in a board is empty (has zero items).
        :param board_id: The ID of the board.
        :param group_id: The ID of the group.
        :return: True if the group is empty, False otherwise. None or error message if the request fails.
        """
        query = (f'query {{ boards (ids: {board_id}) {{ groups (ids: "{group_id}") {{ items_page (limit: 1) {{ '
                 f'items {{ id }} }} }} }} }}')

        payload = {'query': query}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            items = response["data"]["boards"][0]["groups"][0]["items_page"]["items"]
            return len(items) == 0  # True if no items, False otherwise
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################


