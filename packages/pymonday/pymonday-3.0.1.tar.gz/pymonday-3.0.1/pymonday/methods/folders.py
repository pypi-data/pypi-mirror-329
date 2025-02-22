# pymonday/methods/folders.py

########################################################################################################################
# FOLDERS CLASS
########################################################################################################################
class Folders:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def get_folders(self, workspace_id):
        """
        Get all folders in a workspace.
        :param workspace_id: UUID of the workspace.
        :return: Array of Dictionaries containing folder data. Return None or error message on API call failure.
        """
        query_string = f'''query {{folders (workspace_ids: {workspace_id}) {{name id children {{id name}}}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['folders']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def create_folder(self, name, workspace_id, **kwargs):
        """
        Create a folder in a workspace. Pass keyword arguments to configure folder attributes. **Keywords must be passed
        exactly as defined below. Folder colors can be found here:
        https://asset.cloudinary.com/monday-platform-dev/3e39afb2309b512f4f53cc9173554d48
        :param name: The Folders name (Required)
        :param workspace_id: The unique identifier of the workspace to create the new folder in (Required)
        :param kwargs:
            color: The Folders color
            parent_folder_id: The ID of the folder you want to nest the new one under. Nesting is limited to 1 Tier.
        :return: UUID of the newly created folder. Return None or error message on API call failure.
        """

        folder_name = f"\"{name}\""
        arg_string = f'name: {folder_name}, workspace_id: {workspace_id}, '
        for key, value in kwargs.items():
            arg_string = arg_string + f"{key}: {value}, "
        arg_string = arg_string[:-2]
        query_string = f'''mutation {{create_folder ({arg_string}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['create_folder']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def update_folder(self, folder_id, **kwargs):
        """
        Update a folder in a workspace. Pass keyword arguments to configure folder attributes. **Keywords must be passed
        exactly as defined below. Folder colors can be found here:
        https://asset.cloudinary.com/monday-platform-dev/3e39afb2309b512f4f53cc9173554d48
        :param folder_id: UUID of the folder to update. (Required)
        :param kwargs:
            name: Updated name of the folder
            color: Updated folder color
            parent_folder_id: The ID of the folder you want to nest the updated one under.
        :return: UUID of the updated folder. Return None or error message on API call failure.
        """
        if 'name' in kwargs.keys():
            kwargs['name'] = f"\"{kwargs['name']}\""
        arg_string = f"folder_id: {folder_id}, "
        for key, value in kwargs.items():
            arg_string = arg_string + f"{key}: {value}, "
        arg_string = arg_string[:-2]
        query_string = f'''mutation {{update_folder ({arg_string}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['update_folder']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def delete_folder(self, folder_id):
        """
        Delete a folder from a workspace
        :param folder_id: UUID of the folder to delete
        :return: True if successful. Return None or error message on API call failure
        """
        query_string = f'''mutation {{delete_folder (folder_id: {folder_id}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            if response['data']['delete_folder']['id']:
                return True
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################