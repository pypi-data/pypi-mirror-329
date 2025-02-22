# pymonday/methods/items.py

########################################################################################################################
# IMPORTS
########################################################################################################################
import asyncio


########################################################################################################################
# ITEMS CLASS
########################################################################################################################
class Items:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def get_item_ids_from_group(self, board_id, group_id):
        """
        Get all item IDs from a specific group on a board. Cursor Based Pagination Required. Records limited to 100
        per call.
        :param board_id: UUID of the board.
        :param group_id: UUID of the group.
        :return: Array of Item IDs. Return None or error message on API call failure.
        """
        item_attributes = "id"
        initial_query = f'''query {{boards (ids: {board_id}) {{groups(ids: "{group_id}") {{items_page (limit: 500) {{
        cursor items {{{item_attributes}}}}}}}}}}}'''
        data = {'query': initial_query}
        response = self.client.send_post_request(data)

        if not response:
            return None

        try:
            items_page = response["data"]["boards"][0]["groups"][0]["items_page"]
            item_ids = [item['id'] for item in items_page["items"]]
            cursor = items_page["cursor"]

            if cursor is None:
                return item_ids

            all_item_ids = self.client.get_next_page(cursor, item_ids, item_attributes)
            return [int(item['id']) for item in all_item_ids]

        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_items_page_from_group(self, board_id, group_id, columns):
        """
        Retrieve items from a specific group in a board.

        :param board_id: ID of the board.
        :param group_id: ID of the group.
        :param columns: List of column IDs to retrieve.
        :return: List of items. Return None or error message on API call failure.
        """
        column_string = ", ".join(f'"{col}"' for col in columns)
        column_string = f"[{column_string}]"

        item_attributes = f'''name id parent_item{{id name }} column_values(ids: {column_string}) {{text value 
        column{{id title}} ... on BoardRelationValue {{display_value linked_items {{id}}}} ... on MirrorValue 
        {{display_value}}}}'''

        query = f'''query {{boards(ids: [{board_id}]) {{groups(ids: "{group_id}") {{items_page(limit: 50) {{cursor
        items {{{item_attributes}}}}}}}}}}}'''
        payload = {'query': query}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            items_data = response['data']['boards'][0]['groups'][0]['items_page']
            items = items_data.get('items', [])
            cursor = items_data.get('cursor')

            return items if cursor is None else self.client.get_next_page(cursor, items, item_attributes)
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_items_from_column(self, board_id, column_id, value, columns):
        """
        Retrieve items from a board filtered by a column value.

        :param board_id: ID of the board.
        :param column_id: ID of the column to filter.
        :param value: Value to filter items by.
        :param columns: List of column IDs to retrieve.
        :return: List of items. Return None or error message on API call failure.
        """
        column_string = ", ".join(f'"{col}"' for col in columns)
        column_string = f"[{column_string}]"

        item_attributes = f'''name id parent_item{{id name }} column_values(ids: {column_string}) {{text value column
        {{id title}} ... on BoardRelationValue {{display_value linked_items {{id}}}} ... on MirrorValue 
        {{display_value}}}}'''

        query = f'''query {{items_page_by_column_values (limit: 50, board_id: {board_id}, columns: [{{column_id: 
        "{column_id}", column_values: ["{value}"]}}]) {{cursor items {{{item_attributes}}}}}}}'''
        data = {'query': query}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            items_data = response['data']['items_page_by_column_values']
            items = items_data.get('items', [])
            cursor = items_data.get('cursor')
            return items if cursor is None else self.client.get_next_page(cursor, items, item_attributes)
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_items_with_status(self, board_id, group_id, columns, column_id, index_value):
        """
        Retrieve items from a specific group on a board where a column matches a given status/index value.
        :param board_id: UUID of the board.
        :param group_id: UUID of the group.
        :param columns: List of column IDs to retrieve values from.
        :param column_id: The column to filter items by.
        :param index_value: The value to match in the column.
        :return: List of items. Return None or error message on API call failure.
        """
        column_string = ", ".join(f"\"{column}\"" for column in columns)
        item_attributes = f'''name id parent_item{{id name}} column_values(ids: [{column_string}]) {{text value column
        {{id title}} ... on BoardRelationValue {{display_value linked_items {{id}}}} 
        ... on MirrorValue {{display_value}}}}'''

        query = f'''{{boards(ids: {board_id}) {{groups(ids: "{group_id}") {{items_page(limit: 8 query_params: {{rules: 
        {{column_id: "{column_id}", compare_value: [{index_value}]}}}}) {{cursor items {{{item_attributes}}}}}}}}}}}'''

        data = {'query': query}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            items_page = response["data"]["boards"][0]["groups"][0]["items_page"]
            items = items_page["items"]
            cursor = items_page["cursor"]
            if cursor is None:
                return items
            all_items = self.client.get_next_page(cursor, items, item_attributes)
            return all_items
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_items_page_between_dates(self, board_id, group_id, columns, column_id, start_date, end_date):
        """
        Get Items page between a specified date range. Supports Timeline columns and start dates.
        :param board_id: UUID of the board the items are on.
        :param group_id: UUID of the group the items are in.
        :param columns: List of column IDs
        :param column_id: UUID of the timeline column to filter on.
        :param start_date: Start of date range.
        :param end_date: End of date range.
        :return: Array containing Item IDs. Return None or error message on API call failure.
        """
        column_string = ", ".join(f"\"{column}\"" for column in columns)
        item_attributes = f'''name id parent_item{{id name}} column_values(ids: [{column_string}]) {{text value column
        {{id title}} ... on BoardRelationValue {{display_value linked_items {{id}}}} ... on MirrorValue 
        {{display_value}}}}'''

        query = f'''{{boards(ids: {board_id}) {{groups(ids: "{group_id}") {{items_page(limit: 8 query_params: {{rules: 
        {{column_id: "{column_id}", compare_value: ["{start_date}", "{end_date}"], compare_attribute: "START_DATE", 
        operator: between}}}}) {{cursor items {{{item_attributes}}}}}}}}}}}'''
        data = {'query': query}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            items_page = response["data"]["boards"][0]["groups"][0]["items_page"]
            items = items_page["items"]
            cursor = items_page["cursor"]
            if cursor is None:
                return items
            all_items = self.client.get_next_page(cursor, items, item_attributes)
            return all_items
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_items_page_between_date(self, board_id, group_id, columns, column_id, start_date, end_date):
        """
        Get Items page between a specified date range. Supports Date columns and start dates.
        :param board_id: UUID of the board the items are on.
        :param group_id: UUID of the group the items are in.
        :param columns: List of column IDs.
        :param column_id: UUID of the date column to filter on.
        :param start_date: Start of date range.
        :param end_date: End of date range.
        :return: Array containing Item IDs. Return None or error message on API call failure.
        """
        column_string = ", ".join(f"\"{column}\"" for column in columns)
        item_attributes = f'''name id parent_item{{id name}} column_values(ids: [{column_string}]) {{text value column
        {{id title}} ... on BoardRelationValue {{display_value linked_items {{id}}}} ... on MirrorValue 
        {{display_value}}}}'''

        query = f'''{{boards(ids: {board_id}) {{groups(ids: "{group_id}") {{items_page(limit: 500 query_params: {{rules:
        {{column_id: "{column_id}", compare_value: ["{start_date}", "{end_date}"], operator: between}}}}) {{cursor items
        {{{item_attributes}}}}}}}}}}}'''

        data = {'query': query}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            items_page = response["data"]["boards"][0]["groups"][0]["items_page"]
            items = items_page["items"]
            cursor = items_page["cursor"]
            if cursor is None:
                return items
            all_items = self.client.get_next_page(cursor, items, item_attributes)
            return all_items
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_item_ids_between_dates(self, board_id, group_id, column_id, start_date, end_date):
        """
        Get Item IDs between a specified date range. Supports Timeline columns and start dates.
        :param board_id: UUID of the board the items are on.
        :param group_id: UUID of the group the items are in.
        :param column_id: UUID of the timeline column to filter on.
        :param start_date: Start of date range.
        :param end_date: End of date range.
        :return: Array containing Item IDs. Return None or error message on API call failure.
        """
        item_attributes = "id"
        query = f'''{{boards(ids: {board_id}) {{groups(ids: "{group_id}") {{items_page(limit: 500, 
            query_params: {{rules: {{column_id: "{column_id}", compare_value: ["{start_date}", "{end_date}"], 
            compare_attribute: "START_DATE", operator: between}}}}) {{cursor items {{{item_attributes}}}}}}}}}}}'''

        data = {'query': query}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            items = response['data']['boards'][0]['groups'][0]['items_page']['items']
            cursor = response['data']['boards'][0]['groups'][0]['items_page']['cursor']
            item_ids = [item['id'] for item in items]
            if cursor is None:
                return item_ids
            all_item_ids = self.client.get_next_page(cursor, items, item_attributes)
            return [int(item['id']) for item in all_item_ids]
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_item_ids_between_date(self, board_id, group_id, column_id, start_date, end_date):
        """
        Get Item IDs between a specified date range. Supports Date columns.
        :param board_id: UUID of the board the items are on.
        :param group_id: UUID of the group the items are in.
        :param column_id: UUID of the date column to filter on.
        :param start_date: Start of date range.
        :param end_date: End of date range.
        :return: Array containing Item IDs. Return None or error message on API call failure.
        """
        item_attributes = "id"
        query = f'''{{boards(ids: {board_id}) {{groups(ids: "{group_id}") {{items_page(limit: 500, 
            query_params: {{rules: {{column_id: "{column_id}", compare_value: ["{start_date}", "{end_date}"], 
            operator: between}}}}) {{cursor items {{{item_attributes}}}}}}}}}}}'''

        data = {'query': query}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            items = response['data']['boards'][0]['groups'][0]['items_page']['items']
            cursor = response['data']['boards'][0]['groups'][0]['items_page']['cursor']
            item_ids = [item['id'] for item in items]
            if cursor is None:
                return item_ids
            all_item_ids = self.client.get_next_page(cursor, items, item_attributes)
            return [int(item['id']) for item in all_item_ids]
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def get_item_columns(self, item_list, column_id_list):
        """
        Get column values of items on a board.
        :param item_list: Array of item IDs to query. Item IDs must be submitted as integers.
        :param column_id_list: Array of column UUIDs. Column IDs must be submitted as strings.
        :return: Array of dictionaries containing item and column values. Return None or error message on API call failure.
        """
        asyncio.run(self.client.column_task_handler(item_list, column_id_list))

        current_results = self.client.results
        self.client.results = []

        # Handle API response
        if not current_results:
            return None
        try:
            return [item['data']['items'][0] for item in current_results]
        except (TypeError, KeyError, IndexError):
            return current_results


    ####################################################################################################################
    def create_item(self, board, group, item_name):
        """
        Create a new item within a group on a specific board.
        :param board: UUID of the board to create the item on.
        :param group: UUID of the group to create the item in.
        :param item_name: Name of the new item to be created.
        :return: UUID of the newly created item. Return None or error message on API call failure.
        """
        query = f'''mutation {{create_item (board_id: {board}, group_id: "{group}", item_name: "{item_name}") {{id}}}}'''
        data = {'query': query}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['create_item']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def create_item_with_column_values(self, board, group, item_name, column_dict):
        """
        Create a new item within a group on a board and populate specific column values on item creation.
        :param board: UUID of the board to create the item on.
        :param group: UUID of the group to create the item in.
        :param item_name: Name of the new item.
        :param column_dict: Dictionary of column values to set when item is created.
        Example: {"text": {"type": "text", "values": ["Hello World"]}}
        :return: UUID of the newly created item. Return None or error message on API call failure.
        """
        column_string = self.client.column_id_formatter(column_dict)
        query = f'''mutation {{create_item (board_id: {board}, group_id: "{group}", item_name: "{item_name}", 
            column_values: "{column_string}") {{id}}}}'''
        data = {'query': query}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['create_item']['id']
        except (TypeError, KeyError, TypeError):
            return response

    ####################################################################################################################
    def delete_item(self, item_id):
        """
        Delete an item from the platform.
        :param item_id: UUID of the item to delete.
        :return: Confirmation message or error message.
        """
        query = f'''mutation {{delete_item (item_id: {item_id}) {{id}}}}'''
        data = {"query": query}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            if response['data']['delete_item']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - get_items_by_column_values
    def get_items_by_column_values(self, board_id, column_filters, limit=100):
        """
        Retrieve all items from a board that match specific column values using pagination.
        :param board_id: The ID of the board to retrieve items from.
        :param column_filters: List of dictionaries with keys 'column_id' and 'column_values' to filter items
        (for supported columns see https://developer.monday.com/api-reference/reference/items-page-by-column-values).
        :param limit: The number of items to return per page (maximum 500). Defaults to 100.
        :return: List of all items that match the specified filters. Return None or error message on API call failure.
        """

        # Ensure column_values are formatted correctly for GraphQL
        def format_column_values(values):
            return ", ".join(f'"{v}"' for v in values)  # Ensure double quotes for each value

        # Prepare column filters for GraphQL syntax
        columns_str = ', '.join([f'{{column_id: "{col_filter["column_id"]}", '
                f'column_values: [{format_column_values(col_filter["column_values"])}]}}'
                for col_filter in column_filters])

        # Initial request with columns
        query = f'''query {{items_page_by_column_values(board_id: {board_id}, columns: [{columns_str}], limit: {limit}) 
        {{cursor items {{ id name column_values {{ id text }} }}}}}}'''

        payload = {"query": query}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            # Extract initial items and cursor
            next_data = response["data"]["items_page_by_column_values"]
            all_items = next_data["items"]
            cursor = next_data.get("cursor")

            # Fetch remaining pages if cursor exists
            while cursor:
                query = f'''query {{items_page_by_column_values(board_id: {board_id}, limit: {limit}, 
                cursor: "{cursor}") {{cursor items {{ id name column_values {{ id text }}}}}}}}'''
                payload = {"query": query}
                response = self.client.send_post_request(payload)

                if not response:
                    return all_items  # Return collected items if no response
                try:
                    next_data = response["data"]["items_page_by_column_values"]
                    all_items.extend(next_data["items"])
                    cursor = next_data.get("cursor")
                except (KeyError, TypeError, IndexError):
                    break

            return all_items
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - archive_item
    def archive_item(self, item_id):
        """
        Archive an item on a board.
        :param item_id: The unique identifier of the item to archive.
        :return: JSON response confirming the archiving of the item. Return None or error message on API call failure.
        """
        mutation = f'''mutation {{archive_item (item_id: {item_id}) {{id}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            if response['data']['archive_item']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - duplicate_item
    def duplicate_item(self, board_id, item_id, with_updates=True):
        """
        Duplicate an item, including its updates.
        :param board_id: The unique identifier of the board to duplicate the item in.
        :param item_id: The unique identifier of the item to duplicate.
        :param with_updates: Boolean indicating whether to include updates in the duplication.
        :return: UUID of the duplicated item. Return None or error message on API call failure.
        """

        mutation = f'''mutation {{duplicate_item (board_id: {board_id}, item_id: {item_id}, with_updates: 
            {str(with_updates).lower()}) {{id}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['duplicate_item']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - move_item_to_board
    def move_item_to_board(self, item_id, target_board_id, target_group_id, column_mapping=None):
        """
        Move an item to a different board with optional column mapping.
        :param item_id: ID of the item to move.
        :param target_board_id: ID of the target board.
        :param target_group_id: ID of the target group within the target board.
        :param column_mapping: Optional list of dictionaries mapping source columns to target columns.
        :return: UUID of the moved item. Return None or error message on API call failure.
        """
        # Construct the column mapping argument if provided
        if column_mapping:
            columns_mapping = ', '.join(
                f'{{source: "{source}", target: "{target}"}}' for source, target in column_mapping.items())
        else:
            columns_mapping = ''

        mutation = f'''mutation {{move_item_to_board (board_id: {target_board_id}, group_id: "{target_group_id}",
                item_id: {item_id}, columns_mapping: [{columns_mapping}]) {{id}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['move_item_to_board']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################