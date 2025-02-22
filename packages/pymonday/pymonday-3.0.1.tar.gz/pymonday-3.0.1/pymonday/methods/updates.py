# pymonday/methods/updates.py

########################################################################################################################
# UPDATES CLASS
########################################################################################################################
class Updates:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def get_item_updates(self, item_id):
        """
        Get the updates from an item.
        :param item_id: UUID of the item.
        :return: Array of Dictionaries containing the update data. Return None or error message on API call failure.
        """
        query_string = f'''{{items(ids:{item_id})
        {{updates {{id text_body, updated_at created_at creator_id 
        replies {{text_body created_at creator_id}} 
        assets {{id public_url}}}}}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            return response['data']['items'][0]['updates']
        except (KeyError, IndexError, TypeError):
            return response

    ####################################################################################################################
    def create_update(self, item_id, update_text):
        """
        Create an update on an item.
        :param item_id: UUID of the item to leave the update on.
        :param update_text: Body of the update.
        :return: UUID of the update. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{create_update (item_id: {item_id}, body: "{update_text}") {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            return response['data']['create_update']['id']
        except (KeyError, IndexError, TypeError):
            return response

    ####################################################################################################################
    def create_reply(self, item_id, update_text, parent_id):
        """
        Create an update on an item.
        :param item_id: UUID of the item to leave the update on.
        :param update_text: Body of the update.
        :param parent_id: UUID of the update to leave a reply on.
        :return: UUID of the Reply. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{
        create_update (item_id: {item_id}, body: "{update_text}", parent_id: {parent_id}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            return response['data']['create_update']['id']
        except (KeyError, IndexError, TypeError):
            return response

    ####################################################################################################################
    def delete_update(self, update_id):
        """
        Delete an update on an item.
        :param update_id: UUID of the item.
        :return: True on success. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{delete_update (id: {update_id}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            if response['data']['delete_update']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    def clear_updates(self, item_id):
        """
        Clear all updates from an item.
        :param item_id: UUID of the item.
        :return: True on success. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{clear_item_updates (item_id: {item_id}) {{id}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)
        if not response:
            return None
        try:
            if response['data']['clear_item_updates']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################