# pymonday/methods/activity_logs.py
from datetime import datetime

########################################################################################################################
# ACTIVITY LOGS CLASS
########################################################################################################################
class ActivityLogs:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    # New - get_activity_logs
    def get_activity_logs(self, board_id, user_ids=None, limit=25, page=1, from_date=None, to_date=None,
                          column_ids=None, group_ids=None, item_ids=None):
        """
        Retrieve activity logs for a specific board.
        Required Scope: `activity:read`
        :param board_id: ID of the board to retrieve activity logs for.
        :param user_ids: List of user IDs to filter the logs (optional).
        :param limit: Number of activity logs to retrieve (default: 25).
        :param page: Page number to retrieve, starts from 1 (default: 1).
        :param from_date: Start date in 'dd.mm.yyyy' format (optional).
        :param to_date: End date in 'dd.mm.yyyy' format (optional).
        :param column_ids: List of column IDs to filter logs by (optional).
        :param group_ids: List of group IDs to filter logs by (optional).
        :param item_ids: List of item IDs to filter logs by (optional).
        :return: List of activity logs. None or error message if the request fails.
        """

        def convert_to_iso(date_str):
            try:
                return datetime.strptime(date_str, "%d.%m.%Y").isoformat() + "Z"
            except ValueError:
                print(f"Invalid date format: {date_str}. Expected format: dd.mm.yyyy")
                return None

        filters = []
        if user_ids:
            user_ids_string = ", ".join(map(str, user_ids))
            filters.append(f"user_ids: [{user_ids_string}]")
        if from_date:
            iso_from_date = convert_to_iso(from_date)
            if iso_from_date:
                filters.append(f'from: "{iso_from_date}"')
        if to_date:
            iso_to_date = convert_to_iso(to_date)
            if iso_to_date:
                filters.append(f'to: "{iso_to_date}"')
        if column_ids:
            column_ids_string = ", ".join(f'"{col_id}"' for col_id in column_ids)
            filters.append(f'column_ids: [{column_ids_string}]')
        if group_ids:
            group_ids_string = ", ".join(f'"{group_id}"' for group_id in group_ids)
            filters.append(f'group_ids: [{group_ids_string}]')
        if item_ids:
            item_ids_string = ", ".join(map(str, item_ids))
            filters.append(f'item_ids: [{item_ids_string}]')

        filters_string = ", ".join(filters)

        query = f'''query {{boards(ids: [{board_id}]) {{activity_logs(limit: {limit}, page: {page}{", " + filters_string 
        if filters_string else ""}) {{id event data account_id user_id created_at entity}}}}}}'''

        payload = {"query": query}
        response = self.client.send_post_request(payload)

        if not response:
            return None
        try:
            return response["data"]["boards"][0]["activity_logs"]
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################