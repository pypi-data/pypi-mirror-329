# pymonday/methods/notifications.py

########################################################################################################################
# NOTIFICATIONS CLASS
########################################################################################################################
class Notifications:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    def create_notification(self, user_id, target, body, target_type):
        """
        Send a notification to a user.
        :param user_id: UUID of the user to send the notification to.
        :param target: The target's unique identifier. The value depends on the target_type
        :param body: The notification's text.
        :param target_type: the target's type: Project or Post.
            - Project: sends a notification referring to a specific item or board
            - Post : sends a notification referring to a specific item's update or reply
        :return: Text of the notification. Return None or error message on API call failure.
        """
        query_string = f'''mutation {{create_notification 
        (user_id: {user_id}, target_id: {target}, text: "{body}", target_type: {target_type}) {{text}}}}'''
        data = {'query': query_string}
        response = self.client.send_post_request(data)

        # Handle API response
        if not response:
            return None
        try:
            return response['data']['create_notification']['text']
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################