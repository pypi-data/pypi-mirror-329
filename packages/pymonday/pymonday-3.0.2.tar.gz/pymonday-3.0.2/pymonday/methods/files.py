# pymonday/methods/files.py

########################################################################################################################
# IMPORTS
########################################################################################################################
import os


########################################################################################################################
# FILES CLASS
########################################################################################################################
class Files:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def get_assets(self, item_id):
        """
        Get the assets(files) associated with an item.
        :param item_id: UUID of the item.
        :return: Array of dictionaries containing asset data. Return None or full error message if request fails.
        """
        query_string = f'''{{items(ids:{item_id}){{assets {{id name file_size created_at public_url url}}}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            return response['data']['items'][0]['assets']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def upload_file_to_column(self, item_id, column_id, filepath):
        """
        Upload a local file to a file type column of an item. Remote files not supported.
        :param item_id: UUID of the item
        :param column_id: Column ID to upload the file to.
        :param filepath: Absolute Path to file on the local system. File Extension required.
        :return: UUID of the asset. Return None or full error message if request fails.
        """
        file_name = os.path.basename(filepath)
        payload = {
            'query': f'mutation add_file($file: File!) {{add_file_to_column (item_id: {item_id}, '
                     f'column_id: "{column_id}" file: $file) {{id}}}}', 'map': '{"column_file": "variables.file"}'}
        files = [('column_file', (f'{file_name}', open(filepath, 'rb'), 'application/octet-stream'))]

        response = self.client.upload_file(payload, files)
        if not response:
            return None
        try:
            return response['data']['add_file_to_column']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def add_file_to_update(self, update_id, file_path):
        """
        Upload a local file to an update. Remote files not supported.
        :param update_id: UUID of the update.
        :param file_path: Absolute Path to the local file. File Extension Required.
        :return: UUID of the asset. Return None or full error message if request fails.
        """
        file_name = os.path.basename(file_path)
        payload = {
            'query': f'mutation ($file: File!) {{add_file_to_update(file: $file, update_id: {update_id}) {{id}}}}',
            'map': '{"update_file":"variables.file"}'}
        files = [('update_file', (f'{file_name}', open(f'{file_path}', 'rb'), 'application/octet-stream'))]
        response = self.client.upload_file(payload, files)
        if not response:
            return None
        try:
            return response['data']['add_file_to_update']['id']
        except (TypeError, KeyError, IndexError):
            return response

        ####################################################################################################################