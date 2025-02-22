# pymonday/methods/account.py

########################################################################################################################
# ACCOUNT CLASS
########################################################################################################################
class Account:
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    # New - get_account_details
    def get_account_details(self):
        """
        Retrieve the details of the account.
        Required Scope: `account:read`

        :return: Dictionary containing the account details. None or error message if the request fails.
        """
        query = '''query {users {account {id name logo active_members_count country_code first_day_of_the_week 
        show_timeline_weekends tier slug plan {period} products {id kind} sign_up_product_kind}}}'''
        payload = {"query": query}
        response = self.client.send_post_request(payload)  # Use the existing client's session

        if not response:
            return None
        try:
            return response["data"]["users"][0]["account"]
        except (TypeError, KeyError, IndexError):
            return response

    ####################################################################################################################

