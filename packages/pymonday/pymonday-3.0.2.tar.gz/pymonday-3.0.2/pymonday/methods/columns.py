# pymonday/methods/columns.py

########################################################################################################################
# COLUMNS CLASS
########################################################################################################################
class Columns:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def change_column_values(self, board_id, item_id, column_dict):
        """
        Change the column values of an item. Multiple column values can be changed in a single query.
        :param board_id: UUID of the board the item is on.
        :param item_id: UUID of the Item the column values should be changed on.
        :param column_dict: Dictionary containing column IDs, column types and values.
        :return: UUID of the updated item. Return None or error message on API call failure.
        """
        column_string = self.client.column_id_formatter(column_dict)
        query_string = f'''mutation {{change_multiple_column_values (item_id: {item_id}, board_id: {board_id}, 
        column_values: "{column_string}") {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            return response['data']['change_multiple_column_values']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - create_column
    def create_column(self, board_id, title, column_type):
        """
        Create a new column in a board.
        :param board_id: The ID of the board where the column will be created.
        :param title: The title of the column to be created.
        :param column_type: The type of the column (e.g., text, date).
        :return: ID of the newly created column. None or error message if the request fails.
        """
        query = f'''mutation {{create_column (board_id: {board_id}, title: "{title}", column_type: {column_type}) {{id 
        title type }}}}'''
        payload = {'query': query}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response["data"]["create_column"]["id"]
        except (TypeError, KeyError, IndexError):
            return response


    ####################################################################################################################
    # New - change_column_title
    def change_column_title(self, board_id, column_id, new_title):
        """
        Change the title of a column on a board.
        Required Scope: `boards:write`
        :param board_id: The ID of the board containing the column.
        :param column_id: The ID of the column to be updated.
        :param new_title: The new title to assign to the column.
        :return: UUID of the updated column. None or error message if the request fails.
        """
        mutation = f'''mutation {{change_column_title (board_id: {board_id}, column_id: "{column_id}", title: 
        "{new_title}") {{id title}}}}'''
        payload = {"query": mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response["data"]["change_column_title"]["id"]
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - get_column_metadata
    def get_column_metadata(self, board_id, column_ids):
        """
        Retrieve metadata for specific columns on a given board.
        Required Scope: `boards:read`
        :param board_id: ID of the board to retrieve column metadata from (required).
        :param column_ids: List of column IDs to retrieve (required).
        :return: Column metadata as a list of dictionaries. None or error message if the request fails.
        """
        # Build the query arguments
        arguments = []
        if column_ids:
            ids_str = ", ".join(f'"{col_id}"' for col_id in column_ids)
            arguments.append(f'ids: [{ids_str}]')

        # Combine arguments into the query string
        arguments_str = f"({', '.join(arguments)})" if arguments else ""

        # Construct the query
        query = f'''query {{boards (ids: {board_id}) {{columns {arguments_str} {{id title description type
        settings_str archived width }}}}}}'''
        payload = {"query": query}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response["data"]["boards"][0]["columns"]
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def clear_column(self, board_id, item_id, column_id):
        """
        Clears the value of a given column in an item based on its column type.
        :param item_id: The ID of the item.
        :param board_id: The ID of the board.
        :param column_id: The ID of the column to clear.
        :return: UUID of the updated item. None or error message if the request fails.
        """
        # Retrieve column metadata to determine the column type
        metadata_response = self.get_column_metadata(board_id, [column_id])

        if not metadata_response or not metadata_response[0].get("type"):
            print(f"Failed to retrieve column metadata for column_id {column_id}")
            return None

        column_type = metadata_response[0]["type"]

        # Define clearing methods
        simple_null_columns = {
            "checkbox", "board_relation", "country", "dependency", "dropdown", "email", "hour",
            "link", "location", "long_text", "numbers", "people", "phone", "rating", "status",
            "tags", "text", "timeline", "week", "world_clock"
        }

        file_based_columns = {"file", "monday_doc"}

        if column_type in simple_null_columns:
            mutation = f'''mutation {{change_multiple_column_values (item_id: {item_id}, board_id: {board_id}, 
            column_values: "{{\\"{column_id}\\" : null}}") {{id}}}}'''
        elif column_type in file_based_columns:
            mutation = f'''mutation {{change_column_value (board_id: {board_id}, item_id: {item_id},
            column_id: "{column_id}", value: "{{\\"clear_all\\": true}}") {{id}}}}'''
        elif column_type == "date":
            mutation = f'''mutation {{change_simple_column_value (item_id: {item_id}, board_id: {board_id},
            column_id: "{column_id}", value: "") {{id}}}}'''
        else:
            return None

        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response["data"]["change_multiple_column_values"]["id"]
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
