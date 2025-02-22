# pymonday/config.py

########################################################################################################################
# GLOBAL VARIABLES
########################################################################################################################

# API ENDPOINTS:
monday_api_URL = 'https://api.monday.com/v2'
monday_file_URL = 'https://api.monday.com/v2/file'

# API RETRY STRATEGY:
MAX_RETRIES = 3

# GLOBAL VARIABLES
from pymonday.columns import column_formats
column_values = column_formats