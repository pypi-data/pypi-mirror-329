# Monday.com API Client

A Python client for interacting with the [Monday.com GraphQL API](https://developer.monday.com/api-reference/reference/about-the-api-reference).

## 🚀 Features
- Supports all Monday.com API endpoints.
- Organized by method groups (e.g., `Boards`, `Items`, `Users`, etc.).
- Uses **GraphQL queries** for efficient data fetching.
- Implements **async requests** where necessary.
- Handles API rate limits with retries.
- Supports **column formatting** for easy data manipulation.

---

## 📂 Project Structure
```
.
├── .gitignore                  # Specifies intentionally untracked files to ignore
├── LICENSE                     # License file for open-source usage
├── README.md                   # Project documentation and usage guide
├── requirements.txt            # List of dependencies required for the project
├── setup.py                    # Installation and package setup script
├── pymonday/                   # Main package directory
│   ├── __init__.py             # Marks pymonday as a package
│   ├── monday_api_client.py    # Core API client handling authentication and requests
│   ├── config.py                # Global settings, API endpoints, and constants
│   ├── columns.py              # Column-related utilities and formatting functions
│   ├── methods/                # API method groups (organized by functionality)
│   │   ├── __init__.py         # Marks methods as a subpackage
│   │   ├── account.py          # Methods related to account management
│   │   ├── activity_logs.py    # Methods for retrieving activity logs
│   │   ├── boards.py           # Methods for managing boards
│   │   ├── columns.py          # Methods for column operations
│   │   ├── doc_blocks.py       # Methods for handling document blocks
│   │   ├── docs.py             # Methods related to Monday.com docs
│   │   ├── files.py             # Methods for file uploads and attachments
│   │   ├── folders.py          # Methods for folder management
│   │   ├── groups.py           # Methods for managing groups within boards
│   │   ├── items.py            # Methods for managing items (tasks, records)
│   │   ├── notifications.py     # Methods for handling notifications
│   │   ├── subitems.py         # Methods for managing subitems
│   │   ├── tags.py             # Methods for managing tags
│   │   ├── teams.py            # Methods for managing teams
│   │   ├── updates.py          # Methods for managing item updates
│   │   ├── users.py            # Methods for user management
│   │   ├── workspaces.py       # Methods for managing workspaces

```

---

## 🔧 Installation

```sh
pip install pymonday
```

---

## 🎯 Usage Examples

### Initialize the Client
```python
from pymonday import MondayAPIClient

api_key = "your_monday_api_key"
monday = MondayAPIClient(api_key)
```

### Fetch Account Details
```python
account_info = monday.account.get_account_details()
print(account_info)
```

### Create a New Item
```python
new_item_id = monday.items.create_item(board=1234567890, group="group_id", item_name="New Task")
print(f"Created Item ID: {new_item_id}")
```

### Duplicate an Item
```python
duplicated_item = monday.items.duplicate_item(board_id=1234567890, item_id=9876543210)
print(f"Duplicated Item ID: {duplicated_item}")
```

---

## 📄 Method Overview

| Class             | Method Name                   | Method Type | Category | Created in Version |
|-------------------|------------------------------|-------------|----------|--------------------|
| **Account**       | get_account_details          | Public      | Getter   | v2                |
| **Activity Log**  | get_activity_logs            | Public      | Getter   | v3                |
| **Boards**        | get_all_boards               | Public      | Getter   | v2                |
| **Boards**        | get_board_info               | Public      | Getter   | v2                |
| **Boards**        | get_board_groups             | Public      | Getter   | v2                |
| **Boards**        | get_board_from_item          | Public      | Getter   | v2                |
| **Boards**        | get_board_views              | Public      | Getter   | v3                |
| **Boards**        | create_board                 | Public      | Setter   | v2                |
| **Boards**        | update_board_description     | Public      | Setter   | v2                |
| **Boards**        | archive_board                | Public      | Deleter  | v2                |
| **Boards**        | duplicate_board              | Public      | Setter   | v3                |
| **Boards**        | delete_board                 | Public      | Deleter  | v2                |
| **Columns**       | get_column_metadata          | Public      | Getter   | v3                |
| **Columns**       | column_id_formatter          | Static      | Getter   | v2                |
| **Columns**       | create_column                | Public      | Setter   | v3                |
| **Columns**       | change_column_values         | Public      | Setter   | v2                |
| **Columns**       | change_column_title          | Public      | Setter   | v3                |
| **Columns**       | clear_column                 | Public      | Deleter  | v3                |
| **Doc Blocks**    | fetch_doc_blocks             | Public      | Getter   | v3                |
| **Doc Blocks**    | create_doc_block             | Public      | Setter   | v3                |
| **Doc Blocks**    | update_doc_block             | Public      | Setter   | v3                |
| **Doc Blocks**    | delete_doc_block             | Public      | Deleter  | v3                |
| **Docs**          | fetch_docs                   | Public      | Getter   | v3                |
| **Docs**          | create_doc                   | Public      | Setter   | v3                |
| **Files**         | get_assets                   | Public      | Getter   | v2                |
| **Files**         | upload_file_to_column        | Public      | Setter   | v2                |
| **Files**         | add_file_to_update           | Public      | Setter   | v2                |
| **Folders**       | get_folders                  | Public      | Getter   | v2                |
| **Folders**       | create_folder                | Public      | Setter   | v2                |
| **Folders**       | update_folder                | Public      | Setter   | v2                |
| **Folders**       | delete_folder                | Public      | Deleter  | v2                |
| **Groups**        | create_group                 | Public      | Setter   | v2                |
| **Groups**        | move_item_to_group           | Public      | Setter   | v2                |
| **Groups**        | update_group                 | Public      | Setter   | v3                |
| **Groups**        | duplicate_group              | Public      | Setter   | v3                |
| **Groups**        | is_group_empty               | Public      | Getter   | v3                |
| **Groups**        | archive_group                | Public      | Deleter  | v2                |
| **Groups**        | delete_group                 | Public      | Deleter  | v2                |
| **Items**         | get_item_ids_from_group      | Public      | Getter   | v2                |
| **Items**         | get_items_page_from_group    | Public      | Getter   | v2                |
| **Items**         | get_items_from_column        | Public      | Getter   | v2                |
| **Items**         | get_items_with_status        | Public      | Getter   | v2                |
| **Items**         | get_items_page_between_dates | Public      | Getter   | v2                |
| **Items**         | get_items_page_between_date  | Public      | Getter   | v2                |
| **Items**         | get_item_ids_between_dates   | Public      | Getter   | v2                |
| **Items**         | get_item_ids_between_date    | Public      | Getter   | v2                |
| **Items**         | get_item_columns             | Public      | Getter   | v2                |
| **Items**         | get_items_by_column_values   | Public      | Getter   | v3                |
| **Items**         | create_item                  | Public      | Setter   | v2                |
| **Items**         | create_item_with_column_values | Public      | Setter   | v2                |
| **Items**         | archive_item                 | Public      | Deleter  | v3                |
| **Items**         | duplicate_item               | Public      | Setter   | v3                |
| **Items**         | move_item_to_board           | Public      | Setter   | v3                |
| **Items**         | delete_item                  | Public      | Deleter  | v2                |
| **Notifications** | create_notification          | Public      | Setter   | v2                |
| **Subitems**      | get_subitems                 | Public      | Getter   | v2                |
| **Subitems**      | get_subitem_names            | Public      | Getter   | v2                |
| **Subitems**      | get_subitem_info             | Public      | Getter   | v2                |
| **Subitems**      | create_subitem               | Public      | Setter   | v2                |
| **Tags**          | create_or_get_tag            | Public      | Setter   | v3                |
| **Teams**         | get_teams                    | Public      | Getter   | v2                |
| **Teams**         | get_team_members             | Public      | Getter   | v2                |
| **Updates**       | get_item_updates             | Public      | Getter   | v2                |
| **Updates**       | create_update                | Public      | Setter   | v2                |
| **Updates**       | create_reply                 | Public      | Setter   | v2                |
| **Updates**       | clear_updates                | Public      | Deleter  | v2                |
| **Updates**       | delete_update                | Public      | Deleter  | v2                |
| **Users**         | get_all_users                | Public      | Getter   | v2                |
| **Users**         | get_user_info                | Public      | Getter   | v2                |
| **Users**         | add_user_to_board            | Public      | Setter   | v2                |
| **Users**         | remove_user_from_board       | Public      | Deleter  | v2                |
| **Workspaces**    | get_workspaces               | Public      | Getter   | v2                |
| **Workspaces**    | create_workspace             | Public      | Setter   | v3                |
| **Workspaces**    | add_users_to_workspace       | Public      | Setter   | v3                |
| **Workspaces**    | add_teams_to_workspace       | Public      | Setter   | v3                |
| **Workspaces**    | update_workspace             | Public      | Setter   | v3                |
| **Workspaces**    | delete_workspace             | Public      | Deleter  | v3                |
| **Workspaces**    | delete_users_from_workspace  | Public      | Deleter  | v3                |
| **Workspaces**    | delete_teams_from_workspace  | Public      | Deleter  | v3                |


---

## 📌 Return Behavior

The following table outlines the expected return values for different types of methods in the API client.

| **Method Type**       | **Success Return Value**          | **Failure Return Value**         |
|----------------------|-----------------------------------|--------------------------------|
| **Getters** (Retrieve Data) | `dict` / `list` of retrieved data | `None` or `response` (error) |
| **Setters** (Create/Update) | Item UUID                         | `None` or `response` (error) |
| **Delete Methods**   | `True` (if deleted successfully)  | `None` or `response` (error) |


---

## 📄 Documentation
https://pymonday.readthedocs.io/en/latest/

---

## 📜 License
This project is licensed under GNU General Public Licence.
