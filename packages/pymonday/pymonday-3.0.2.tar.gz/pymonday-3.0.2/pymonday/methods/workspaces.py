# pymonday/methods/workspaces.py

########################################################################################################################
# WORKSPACES CLASS
########################################################################################################################
class Workspaces:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def get_workspaces(self):
        """
        Get all monday.com workspaces
        :return: List of dictionaries containing workspaces IDs and names. Returns None or error message on API call failure.
        """
        query_string = f'''query {{workspaces {{id name kind description}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            workspace_data = response['data']['workspaces']
            return workspace_data
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - create_workspace
    def create_workspace(self, name, kind='open', description=None):
        """
        Create a new workspace.
        :param name: The name of the new workspace.
        :param kind: The type of workspace ('open' or 'closed'). Default is 'open'.
        :param description: Optional description of the workspace.
        :return: UUID of the newly created workspace. Return None or error message on API call failure.
        """
        mutation = f'''mutation {{create_workspace (name: "{name}", kind: {kind.lower()}
                {f', description: "{description}"' if description else ''}) {{id name description}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            return response['data']['create_workspace']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - add_users_to_workspace
    def add_users_to_workspace(self, workspace_id, user_ids, kind='subscriber'):
        """
        Add users to a workspace.
        :param workspace_id: The ID of the workspace.
        :param user_ids: List of user IDs to add to the workspace.
        :param kind: The role of the users in the workspace ('subscriber' or 'owner'). Default is 'subscriber'.
        :return: JSON response confirming the addition of users.
        """
        user_ids_str = ', '.join(map(str, user_ids))
        mutation = f'''mutation {{add_users_to_workspace (workspace_id: {workspace_id}, user_ids: [{user_ids_str}],
                kind: {kind.lower()}) {{id}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            return response['data']['add_users_to_workspace']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - delete_workspace
    def delete_workspace(self, workspace_id):
        """
        Delete a workspace.
        :param workspace_id: The ID of the workspace to delete.
        :return: True if successful. Return None or error message on API call failure.
        """
        mutation = f'''mutation {{delete_workspace (workspace_id: {workspace_id}) {{id}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            if response['data']['delete_workspace']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - delete_users_from_workspace
    def delete_users_from_workspace(self, workspace_id, user_ids):
        """
        Remove users from a workspace.
        :param workspace_id: The ID of the workspace.
        :param user_ids: List of user IDs to remove from the workspace.
        :return: True if successful. Return None or error message on API call failure.
        """
        user_ids_str = ', '.join(map(str, user_ids))
        mutation = f'''mutation {{delete_users_from_workspace (workspace_id: {workspace_id}, user_ids: [{user_ids_str}]
            ) {{id}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            if response['data']['delete_users_from_workspace']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - add_teams_to_workspace
    def add_teams_to_workspace(self, workspace_id, team_ids, kind="subscriber"):
        """
        Add teams to a workspace.
        :param workspace_id: The ID of the workspace.
        :param team_ids: List of team IDs to add to the workspace.
        :param kind: The subscriber's role ('owner' or 'subscriber'). Default is 'subscriber'.
        :return: True if successful. Return None or error message on API call failure.
        """
        # Convert team_ids list to GraphQL array format
        team_ids_str = ', '.join(map(str, team_ids))

        mutation = f'''mutation {{add_teams_to_workspace (workspace_id: {workspace_id}, team_ids: [{team_ids_str}],
                kind: {kind.lower()}) {{id}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            if response['data']['add_teams_to_workspace']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - delete_teams_from_workspace
    def delete_teams_from_workspace(self, workspace_id, team_ids):
        """
        Remove teams from a workspace.
        :param workspace_id: The ID of the workspace.
        :param team_ids: List of team IDs to remove from the workspace.
        :return: True if successful. Return None or error message on API call failure.
        """
        # Convert team_ids list to GraphQL array format
        team_ids_str = ', '.join(map(str, team_ids))

        mutation = f'''mutation {{delete_teams_from_workspace (workspace_id: {workspace_id}, team_ids: [{team_ids_str}]
            ) {{id}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            if response['data']['delete_teams_from_workspace']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - update_workspace
    def update_workspace(self, workspace_id, name=None, description=None):
        """
        Update the attributes of a workspace.
        :param workspace_id: The ID of the workspace.
        :param name: The new name for the workspace (optional).
        :param description: The new description for the workspace (optional).
        :return: The updated workspace data. Return None or error message on API call failure.
        """
        # Build the attributes object dynamically based on provided arguments
        attributes = []
        if name:
            attributes.append(f'name: "{name}"')
        if description:
            attributes.append(f'description: "{description}"')
        attributes_str = ', '.join(attributes)

        mutation = f'''mutation {{update_workspace (id: {workspace_id}, attributes: {{ {attributes_str} }}
            ) {{id name description}}}}'''
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            return response['data']['update_workspace']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################