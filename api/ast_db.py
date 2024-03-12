# ************************************************************************************************
# ****************************************** IMPORTS *********************************************

from ast_db_base import *

# *************************************************************************************************
# ****************************************** DB SETUP *********************************************
# *************************************************************************************************

def modify_user_to_fraudulent(connection: Any, user_id: int, fraudulent: bool) -> bool:
    """
    If a user has been acting in a fraudulent manner.

    Returns:
        (bool): True if the update was successful, False otherwise.
    """
    return update_user_info_in_db(connection, user_id, {"fraudulent": fraudulent})

def update_user_last_visit_in_db(connection: Any, user_id: int, last_visit: datetime) -> bool:
    """
    Update the last visit timestamp of a user in the DB.

    Returns:
        (bool): True if the update was successful, False otherwise.
    """
    return update_user_info_in_db(connection, user_id, {"last_visit": last_visit})

def update_client_last_visit_in_db(connection: Any, client_id: int, last_visit_timestamp: datetime) -> bool:
    """
    Update the last visit timestamp of a client in the DB.

    Returns:
        (bool): True if the update was successful, False otherwise.
    """
    return update_client_info_in_db(connection, client_id, {'last_connection': last_visit_timestamp})
