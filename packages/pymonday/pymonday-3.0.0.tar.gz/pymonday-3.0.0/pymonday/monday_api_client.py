# pymonday/monday_api_client.py

########################################################################################################################
# IMPORTS
########################################################################################################################
import httpx
import asyncio
import time
from .config import monday_api_URL, monday_file_URL, MAX_RETRIES
from .columns import column_formats

# Import all method groups
from .methods.account import Account
from .methods.activity_logs import ActivityLogs
from .methods.boards import Boards
from .methods.columns import Columns
from .methods.docs import Docs
from .methods.doc_blocks import DocBlocks
from .methods.files import Files
from .methods.folders import Folders
from .methods.groups import Groups
from .methods.items import Items
from .methods.notifications import Notifications
from .methods.subitems import Subitems
from .methods.tags import Tags
from .methods.teams import Teams
from .methods.updates import Updates
from .methods.users import Users
from .methods.workspaces import Workspaces

########################################################################################################################
# MONDAY API CLIENT
########################################################################################################################
class MondayAPIClient:
    """
    Client for interacting with the Monday.com GraphQL API.
    """

    def __init__(self, api_key):
        self.access_token = api_key
        self.session = httpx.Client()
        self.column_values = column_formats
        self.results = []
        self.session.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "API-Version": "2025-01"
        }

        # Initialize modules, passing self so they share the same session
        self.account = Account(self)
        self.activity_logs = ActivityLogs(self)
        self.boards = Boards(self)
        self.columns = Columns(self)
        self.docs = Docs(self)
        self.doc_blocks = DocBlocks(self)
        self.files = Files(self)
        self.folders = Folders(self)
        self.groups = Groups(self)
        self.items = Items(self)
        self.notifications = Notifications(self)
        self.subitems = Subitems(self)
        self.tags = Tags(self)
        self.teams = Teams(self)
        self.updates = Updates(self)
        self.users = Users(self)
        self.workspaces = Workspaces(self)

    ####################################################################################################################
    # MONDAY API CLIENT CLASS METHODS
    ####################################################################################################################
    def send_post_request(self, payload):
        """
        API POST Request using HTTPX Session
        :param payload: JSON query string
        :return: JSON formatted data from the HTTP response. Returns None on API call failure.
        """
        for _ in range(MAX_RETRIES):
            response = self.session.post(url=monday_api_URL, json=payload, timeout=30.0)
            if response.status_code == 200:
                return response.json()
            print(response.content)
            time.sleep(5)

    ####################################################################################################################
    def upload_file(self, payload, files):
        """
        API POST Request for file uploads.
        :param payload: JSON GraphQL query string.
        :param files: Files to be uploaded.
        :return: JSON response from API call.
        """
        file_headers = {'Authorization': self.access_token, "API-Version": "2024-07"}
        for _ in range(MAX_RETRIES):
            response = httpx.request(
                method="POST", url=monday_file_URL, data=payload, files=files, headers=file_headers)
            if response.status_code == 200:
                return response.json()
            print(response.content)
            time.sleep(5)

    ####################################################################################################################
    async def async_post(self, payload):
        """
        Asynchronous API call with concurrency limit handling.
        """
        async with httpx.AsyncClient(headers=self.session.headers) as client:
            for _ in range(MAX_RETRIES):
                response = await client.post(url=monday_api_URL, json=payload, timeout=60)
                if response.status_code == 200:
                    self.results.append(response.json())
                    return

                if response.status_code == 429 or "maxConcurrencyExceeded" in response.text:
                    error_data = response.json()
                    retry_seconds = error_data.get("errors", [{}])[0].get("extensions", {}).get("retry_in_seconds", 15)
                    print(f"Concurrency limit exceeded. Retrying in {retry_seconds} seconds...")
                    await asyncio.sleep(retry_seconds)
                else:
                    print(response.content)
                    await asyncio.sleep(5)

        print("Max retries exceeded.")
        return None

    ####################################################################################################################
    def get_next_page(self, cursor, items, item_attributes):
        """
        Get the next set of 100 records using cursor-based pagination.
        :param cursor: Token-based cursor for retrieving the next set of records.
        :param items: Initial items list.
        :param item_attributes: Attributes to retrieve.
        :return: List of item data.
        """
        while cursor is not None:
            subsequent_query = f'''query
            {{next_items_page (limit: 100, cursor: "{cursor}") {{cursor items {{{item_attributes}}}}}}}'''
            next_data = {'query': subsequent_query}
            next_response = self.send_post_request(next_data)

            if not next_response:
                return None
            next_items = [item for item in next_response['data']['next_items_page']['items']]
            items = items + next_items
            cursor = next_response['data']['next_items_page']['cursor']

        return items

    ####################################################################################################################
    async def column_task_handler(self, item_ids, columns):
        """
        Async task handler for column value retrieval.
        :param item_ids: UUID of the Item to retrieve column values for.
        :param columns: UUID of the columns values to retrieve.
        :return: Json formatted Data from the HTTP response. Return None on API call failure.
        """
        column_string = ""
        for column in columns:
            column_string = column_string + f"\"{column}\", "
        column_string = column_string[:-2]
        column_string = f"[{column_string}]"

        tasks = []
        for each_item in item_ids:
            query_string = f'''
            {{items(ids: {each_item}) {{id name parent_item{{id name}}column_values(ids: {column_string}) 
            {{id text value column{{id title}} 
            ... on MirrorValue{{display_value}} 
            ... on BoardRelationValue{{display_value linked_items{{id}}}}}}}}}}'''
            payload = {'query': query_string}
            tasks.append(self.async_post(payload))
        await asyncio.gather(*tasks)

    ####################################################################################################################
    def column_id_formatter(self, column_dictionary):
        """
        Takes the column values dictionary and converts it into a correctly formatted GraphQL query string.
        :param column_dictionary: Dictionary containing column id, column type, and required values for the query.
        :return: JSON formatted GraphQL query for column values.
        """
        query_string = "{"
        for (key, value) in column_dictionary.items():
            value_arguments = [key]
            for each_value in value['values']:
                value_arguments.append(each_value)
            column_string = self.column_values[value['type']].format(*value_arguments)
            query_string += f"{column_string}, "

        query_string = query_string.rstrip(", ")  # Remove the last comma
        query_string += "}"
        return query_string

    ####################################################################################################################