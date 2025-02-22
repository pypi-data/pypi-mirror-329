# pymonday/methods/subitems.py

########################################################################################################################
# SUBITEMS CLASS
########################################################################################################################
class Subitems:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def get_subitems(self, item_id):
        """
        Get the UUIDs of the subitems of an item
        :param item_id: UUID of the parent Item
        :return: Array of subitem IDs. Return None or error message on API call failure.
        """
        query_string = f'''{{items (ids: {item_id}) {{subitems {{id}}}}}}'''
        data = {"query": query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            subitem_ids = [item['id'] for item in response['data']['items'][0]['subitems']]
            return subitem_ids
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_subitem_names(self, item_id):
        """
        Get the UUIDs of the subitem IDs and names of an item
        :param item_id: UUID of the parent Item
        :return: Dict of subitem IDs & Names. Return None or error message on API call failure.
        """
        query_string = f'''{{items (ids: {item_id}) {{subitems {{id name}}}}}}'''
        data = {"query": query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            subitem_ids = {item['id']: item['name'] for item in response['data']['items'][0]['subitems']}
            return subitem_ids
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_subitem_info(self, sub_item_id):
        """
        Get the Board ID and Parent ID from a Subitem.
        :param sub_item_id: UUID of the subitem.
        :return: Dictionary containing the parent ID and Board ID of the subitem. Return None or error message on API
        call failure.
        """
        query_string = f'''{{items(ids: {sub_item_id}) {{parent_item {{id}} board {{id}}}}}}'''
        data = {"query": query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            parent_item = response['data']['items'][0]['parent_item']['id']
            board = response['data']['items'][0]['board']['id']
            subitem_dictionary = {"Parent Item": parent_item, "Subitem Board": board}
            return subitem_dictionary
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def create_subitem(self, parent_id, item_name, column_dictionary):
        """
        Create a new Subitem under a Parent Item.
        :param parent_id: UUID of the item to create the subitem under.
        :param item_name: Name of the new Subitem.
        :param column_dictionary: Dictionary containing column IDs, column types and values.
        :return: Dictionary containing the newly created Subitem ID and the board ID on which the subitem was created.
        Return None or error message on API call failure.
        """
        column_string = self.client.column_id_formatter(column_dictionary)
        query_string = f'''mutation {{create_subitem (parent_item_id: {parent_id}, item_name: "{item_name}", 
        column_values: "{column_string}") {{id board {{id}}}}}}'''
        data = {"query": query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            board_id = response['data']['create_subitem']['board']['id']
            new_item_id = response['data']['create_subitem']['id']
            new_item_dict = {"Item ID": new_item_id, "Subitem Board": board_id}
            return new_item_dict
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################