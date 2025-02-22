# pymonday/methods/tags.py

########################################################################################################################
# TAGS CLASS
########################################################################################################################
class Tags:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    # New - create_or_get_tag
    def create_or_get_tag(self, tag_name, board_id=None):
        """
        Create a new tag or get an existing tag by name. Optionally associate the tag with a specific board.
        :param tag_name: The name of the tag to be created or retrieved.
        :param board_id: Optional. The ID of the board to associate the tag with.
        :return: The UUID of the created or retrieved tag. Return None or error message on API call failure.
        """
        mutation = f'''mutation {{create_or_get_tag (tag_name: "{tag_name}"{f', board_id: {board_id}' 
        if board_id else ''}) {{id name}}}}'''
        payload = {'query': mutation}

        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['create_or_get_tag']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################