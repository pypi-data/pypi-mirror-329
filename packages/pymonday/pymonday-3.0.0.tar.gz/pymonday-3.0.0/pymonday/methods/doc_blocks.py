# pymonday/methods/doc_blocks.py

########################################################################################################################
# IMPORTS
########################################################################################################################
import json


########################################################################################################################
# DOC BLOCKS CLASS
########################################################################################################################
class DocBlocks:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    # New - fetch_doc_blocks
    def fetch_doc_blocks(self, doc_id, limit=50, page=1):
        """
        Fetch metadata for all blocks within a specific doc with pagination.
        :param doc_id: ID of the doc.
        :param limit: Number of blocks to retrieve per request (default: 50, max: 100).
        :param page: Page number to fetch (default: 1).
        :return: JSON response containing block details. Return None or error message on API call failure.
        """
        query = f'''query {{docs (ids: {doc_id}) {{blocks (limit: {limit}, page: {page}) {{id type content}}}}}}'''
        payload = {'query': query}

        # Send request and validate response
        response = self.client.send_post_request(payload)
        if not response:
            return None
        try:
            return response['data']['docs'][0]['blocks']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - create_doc_block
    def create_doc_block(self, doc_id, block_type, content, after_block_id=None):
        """
        Create a new block within a specific doc.
        :param doc_id: ID of the doc (required).
        :param block_type: Type of the block (required, e.g., 'normal_text', 'table').
        :param content: JSON-formatted string or dictionary representing the block content (required)
        (for content field information check https://developer.monday.com/api-reference/reference/blocks).
        :param after_block_id: ID of the block that will be above the new block (optional).
        :return: Created block's ID. Return None or error message on API call failure.
        """
        # Ensure `content` is properly JSON-encoded
        formatted_content = json.dumps(content) if isinstance(content, dict) else content

        # Escape double quotes in the JSON content to ensure compatibility with GraphQL
        escaped_content = formatted_content.replace('"', '\\"')

        # Build the mutation as a single concatenated string
        mutation = (f'mutation {{ create_doc_block (type: {block_type}, doc_id: {doc_id}, ' +
                    (f'after_block_id: "{after_block_id}", ' if after_block_id else '') +
                    f'content: "{escaped_content}") {{ id }} }}')


        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['create_doc_block']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - update_doc_block
    def update_doc_block(self, block_id, content):
        """
        Update the content of an existing block.
        :param block_id: ID of the block to update (required).
        :param content: New content for the block. Must be a valid JSON object or string (required)
        (for content field information check https://developer.monday.com/api-reference/reference/blocks).
        :return: Updated block's ID. Return None or error message on API call failure.
        """
        # Ensure `content` is properly JSON-encoded
        formatted_content = json.dumps(content) if isinstance(content, dict) else content

        # Escape double quotes in the JSON content for GraphQL compatibility
        escaped_content = formatted_content.replace('"', '\\"')

        # Construct the mutation
        mutation = f'mutation {{ update_doc_block (block_id: "{block_id}", content: "{escaped_content}") {{ id }} }}'
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['update_doc_block']['id']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################
    # New - delete_doc_block
    def delete_doc_block(self, block_id):
        """
        Delete a block from a doc.
        :param block_id: ID of the block to delete (required).
        :return: True if successful. Return None or error message on API call failure.
        """
        # Ensure the block_id is properly quoted for GraphQL
        mutation = f'mutation {{ delete_doc_block (block_id: "{block_id}") {{ id }} }}'
        payload = {'query': mutation}
        response = self.client.send_post_request(payload)

        if not response:
            return None
        try:
            if response['data']['delete_doc_block']['id']:
                return True
            else:
                return response
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################