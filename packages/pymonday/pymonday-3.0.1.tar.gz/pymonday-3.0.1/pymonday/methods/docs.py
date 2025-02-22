# pymonday/methods/docs.py

########################################################################################################################
# DOCS CLASS
########################################################################################################################
class Docs:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    # New - fetch_docs
    def fetch_docs(self, object_ids=None, limit=25, page=1):
        """
        Fetch metadata for docs with pagination.
        :param object_ids: Specific doc IDs to return (optional).
        :param limit: Limit on the number of docs to retrieve (default: 25, max: 100).
        :param page: Page number to fetch (default: 1).
        :return: List of dictionaries containing doc details. None or error message if the request fails.
        """
        object_ids_string = f"object_ids: {object_ids}" if object_ids else ""
        query = f'''query {{docs ({object_ids_string}, limit: {limit}, page: {page}) {{id object_id settings created_by 
        {{id name}}}}}}'''
        payload = {'query': query}
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            return response['data']['docs']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - create_doc
    def create_doc(self, workspace_id, name, kind="private"):
        """
        Create a new doc in a workspace.
        :param workspace_id: ID of the workspace.
        :param name: Name of the new doc.
        :param kind: Doc kind ('private', 'public', or 'share').
        :return: UUID of the newly created doc. Return None or error message on API call failure.
        """
        # Validate and format `kind`
        kind = kind.lower()
        if kind not in {"private", "public", "share"}:
            raise ValueError("Invalid 'kind'. Must be 'private', 'public', or 'share'.")

        # Construct the GraphQL mutation
        mutation = (f'mutation {{ create_doc (location: {{ workspace: {{ workspace_id: {workspace_id}, name: "{name}", '
                    f'kind: {kind} }} }} ) {{ id }} }}')
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            return response['data']['create_doc']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################