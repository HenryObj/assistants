# ************************************************************************************************
# ****************************************** IMPORTS *********************************************

from utilities import *
import os 
import psycopg2
from psycopg2 import pool
from urllib.parse import urlparse
import time

from contextlib import contextmanager

from werkzeug.security import generate_password_hash

# *************************************************************************************************
# ****************************************** DB SETUP *********************************************
# *************************************************************************************************

if 'DATABASE_URL' in os.environ:
    database_url = os.environ['DATABASE_URL']
    url = urlparse(database_url)
else:
    database_url = None

def open_connection():
    """
    Opens a connection with the PostGreSQL DB. Returns a connection object.
    We sets the parameters here and here only.
    Later, we can have the parameters as param of the function if multiple connections type.
    """
    connection = psycopg2.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
    )
    return connection

class CursorContextManager:
    def __init__(self, connection: Any):
        self.connection = connection

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()

db_pool = pool.SimpleConnectionPool(
    1,
    MAX_CONNECTIONS,
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    application_name="NAME OF YOUR APPLICATION"
)    
        
# Context manager to handle getting and putting back connections
@contextmanager
def get_db_connection():
    connection = None
    try:
        for attempt in range(MAX_RETRIES):
            try:
                connection = db_pool.getconn()
                yield connection
                break
            except pool.PoolError as pool_error:
                if attempt == MAX_RETRIES - 1:
                    log_issue(pool_error, get_db_connection, "PoolError after max retries and backoff")
                time.sleep((2 ** attempt) * 0.1)  # exponential backoff
    except Exception as e:
        log_issue(e, get_db_connection, "Failed to get or yield a connection")
    finally:
        if connection is not None:
            db_pool.putconn(connection)

# To get the connection in the route without opening and closing it
def get_connection_dependency():
    with get_db_connection() as connection:
        yield connection

# *************************************************************************************************
# **************************************** CLIENT FUNC ********************************************
# *************************************************************************************************

def add_client_in_db(connection: Any, client_name: str, client_company=None, client_domain=None, client_email=None, client_pss=None, client_logo= None) -> tuple:
    """
    Insert a new client in the DB.

    Returns:
        (str, int): A tupple with the status and the id of the client. The id is None if there is an error.
    """
    test = get_client_id(connection, client_name)
    if test: return ("old", test)
    # If we have a client password, hash it not to store the info in clear 
    hashed_pss = generate_password_hash(client_pss, method='pbkdf2:sha256:600000') if client_pss else None
    tup_values = (client_name, client_company, client_domain, client_email, hashed_pss, client_logo)

    query = "INSERT INTO clients (client_name, client_company, client_domain, client_email, client_pss, client_logo) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, tup_values)
            new_client_id = cursor.fetchone()[0]
        connection.commit()
        return ("new", new_client_id)
    except Exception as e:
        log_issue(e, add_client_in_db, f"For the Client: {client_name}. Provided info: Company: {client_company}. Domain: {client_domain}. Email: {client_email}. Pswd info: {check__if_password_safe(client_pss)} ")
        return ("issue", None)
    
def delete_client_from_db(connection: Any, client_id: int) -> str:
    """
    Delete a client from the DB based on client_id.

    Returns:
        (str): Status of the operation ('deleted', 'not found', or 'error').
    """
    query = "DELETE FROM clients WHERE id = %s RETURNING id;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (client_id,))
            res = cursor.fetchone()
            connection.commit()
            return 'deleted' if res else 'not found'
    except Exception as e:
        log_issue(e, delete_client_from_db, f"For client ID: {client_id}")
        return 'error'
    
def get_client_data(connection: Any, client_id: int) -> Optional[dict]:
    """
    Retrieve client data from the DB based on client_id.

    Returns:
        (dict): Client data. None if error or not found.
    """
    query = "SELECT * FROM clients WHERE id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (client_id,))
            res = cursor.fetchone()
            if res:
                keys = ['id', 'client_name', 'client_company', 'client_domain', 'client_email', 'client_pss', 'client_logo', 'total_file_size_in_mb', 'last_connection']
                return dict(zip(keys, res))
    except Exception as e:
        log_issue(e, get_client_data, f"For client ID: {client_id}")

def get_client_list(connection: Any) -> Optional[dict]:
    """
    Retrieve client list.

    Returns:
        (dict): Client list. None if error or not found.
    """
    query = "SELECT id, client_name FROM clients"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            clients = [{"client_id": row[0], "client_name": row[1]} for row in rows]
            return clients
    except Exception as e:
        log_issue(e, get_client_list, "Error while fetching client list")
        return []

def get_client_id(connection: Any, client_name: str) -> Optional[int]:
    """
    Get the ID of the client based on the client name.

    Returns:
    - (int): The client_id. None if error.
    """
    query = "SELECT id FROM clients WHERE client_name = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (client_name,))
            res = cursor.fetchone()
            if res: return res[0]
    except Exception as e:
        log_issue(e, get_client_id, f"For the Client: {client_name}")

def update_client_info_in_db(connection: Any, client_id: int, updates: dict) -> bool:
    """
    Update client information in the DB.

    Args:
    - updates: A dictionary where keys are column names and values are the new values.

    Returns:
    - bool: True if update was successful, False otherwise.
    """
    updates.pop('client_id', None)
    updates = {k: v for k, v in updates.items() if v is not None and v != ''}
    if not updates: return False
    if 'client_pss' in updates:
        updates['client_pss'] = generate_password_hash(updates['client_pss'], method='pbkdf2:sha256:600000')
    set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
    values = list(updates.values()) + [client_id]
    query = f"UPDATE clients SET {set_clause} WHERE id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, values)
        connection.commit()
        return True
    except Exception as e:
        log_issue(e, update_client_info_in_db, f"Client ID: {client_id}, Updates: {updates}")
        return False

# *************************************************************************************************
# ****************************************** USER FUNC ********************************************
# *************************************************************************************************

def add_ip_to_user_in_db(connection: Any, user_id: int, ip: str) -> bool:
    """
    Add an IP to the list of IP used by the user.
    Format is ["IP1", "IP2", etc.]

    Returns:
    - bool: True if the user exists, False otherwise.
    """
    # Retrieve the current list of IPs
    query = "SELECT ip FROM user WHERE id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            current_ips = result[0] if result else ''

        # Update with new IP
        new_ips = current_ips + ',' + ip if current_ips else ip
        return update_user_info_in_db(connection, user_id, {"ip": new_ips})
    except Exception as e:
        log_issue(e, add_ip_to_user_in_db, f"User ID: {user_id}, IP: {ip}")
        return False

def add_user_in_db(connection: Any, client_id: int, username: str, first_name=None, last_name=None, user_email=None, user_pss=None, lang=None, ip=None) -> tuple:
    """
    Add a new user to the DB.

    Returns:
    - (tuple): Status of the operation ('added', 'exists', or 'error').
    """
    try:
        if check_user_in_db(connection, client_id, username):
            return ("exists", username)
        hashed_pss = generate_password_hash(user_pss, method='pbkdf2:sha256:600000') if user_pss else None
        user_values = (client_id, username, first_name, last_name, user_email, hashed_pss, lang, ip)
        query = "INSERT INTO users (client_id, username, first_name, last_name, user_email, user_pss, lang, ip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"

        with CursorContextManager(connection) as cursor:
            cursor.execute(query, user_values)
            new_user_id = cursor.fetchone()[0]
        connection.commit()
        return ("added", new_user_id)

    except Exception as e:
        log_issue(e, add_user_in_db, f"For user: {username}. Client ID: {client_id}")
        return ("error", None)

def check_user_in_db(connection: Any, client_id: int, username: str) -> bool:
    """
    Check if a user exists in the database.

    Returns:
    - (bool): True if the user exists, False otherwise.
    """
    query = "SELECT id FROM users WHERE client_id = %s AND username = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (client_id, username))
            return cursor.fetchone() is not None
    except Exception as e:
        log_issue(e, check_user_in_db, f"Client ID: {client_id}, Username: {username}")
        return False

def delete_user_from_db(connection: Any, user_id: int) -> bool:
    """
    Delete a user from the DB.

    Returns:
    - (bool): True if deletion was successful, False otherwise.
    """
    query = "DELETE FROM users WHERE id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (user_id,))
        connection.commit()
        return True
    except Exception as e:
        log_issue(e, delete_user_from_db, f"User ID: {user_id}")
        return False

def update_user_info_in_db(connection: Any, user_id: int, updates: dict) -> bool:
    """
    Update user information in the DB.

    Args:
    - updates: A dictionary where keys are column names and values are the new values.

    Returns:
    - (bool): True if update was successful, False otherwise.
    """
    updates.pop('user_id', None)
    updates = {k: v for k, v in updates.items() if v is not None and v != ''}
    if not updates: return False
    if 'user_pss' in updates:
        updates['user_pss'] = generate_password_hash(updates['user_pss'], method='pbkdf2:sha256:600000')
    
    set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
    values = list(updates.values()) + [user_id]
    query = f"UPDATE users SET {set_clause} WHERE id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, values)
        connection.commit()
        return True
    except Exception as e:
        log_issue(e, update_user_info_in_db, f"User ID: {user_id}, Updates: {updates}")
        return False

def get_user_list(connection: Any) -> Optional[dict]:
    """
    Retrieve user list.

    Returns:
        (dict): User list. None if error or not found.
    """
    query = "SELECT id, username FROM users"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            users = [{"user_id": row[0], "username": row[1]} for row in rows]
            return users
    except Exception as e:
        log_issue(e, get_user_list, "Error while fetching user list")
        return []
    
def get_user_data(connection: Any, user_id: int) -> Optional[dict]:
    """
    Retrieve user data from the DB based on user_id.

    Returns:
        (dict): User data. None if error or not found.
    """
    query = "SELECT * FROM users WHERE id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (user_id,))
            res = cursor.fetchone()
            if res:
                keys = ['id', 'client_id', 'username', 'first_name', 'last_name', 'user_email', 'user_pss', 'lang', 'ip', 'date_added', 'last_visit']
                return dict(zip(keys, res))
    except Exception as e:
        log_issue(e, get_user_data, f"For client ID: {user_id}")


# *************************************************************************************************
# ****************************************** ASSISTANT FUNC ********************************************
# *************************************************************************************************


def add_assistant_in_db(connection: Any, id: str, client_id: int, assistant_name: str, instructions: str, gpt_model:str) -> str:
    """
    Add a new user to the DB.

    Args:
    - id (str): id of the assistant.
    - client_id (int): client id to add assistant's details.
    - assistant_name (str): name of the assistant.
    - instructions (str): instructions for the assistant.
    - gpt_model (str): gpt model for the assistant.

    Returns:
    - (str): Status of the operation ('added' or 'error').
    """
    assistant_values = (id, client_id, assistant_name, instructions, gpt_model)
    query = "INSERT INTO assistants (id, client_id, assistant_name, instructions, gpt_model) VALUES (%s, %s, %s, %s, %s);"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, assistant_values)
        connection.commit()
        return "added"
    except Exception as e:
        log_issue(e, add_user_in_db, f"For assistant: {assistant_name}. Client ID: {client_id}")
        return "error"
    
def check_thread_in_db(connection: Any, thread_id: int) -> bool:
    """
    Check if a thread_id exists in the database.

    Returns:
    - (bool): True if the thread_id exists, False otherwise.
    """
    query = "SELECT id FROM threads WHERE id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (thread_id,))
            return cursor.fetchone() is not None
    except Exception as e:
        log_issue(e, check_user_in_db, f"Thread Id: {thread_id}")
        return False

def add_thread_details_in_db(connection: Any, id: str, assistant_id: str, user_id: int, first_words: str="") -> str:
    """
    Adds thread details to the database.

    Args:
    - id: Thread ID.
    - assistant_id: Assistant ID associated with the thread.
    - user_id: User ID associated with the thread.
    - first_words: words of first messages.

    Returns:
        (str) Status of the operation ('upserted', 'error').
    """
    query = """
    INSERT INTO threads (id, assistant_id, user_id, first_words) 
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) 
    DO UPDATE SET first_words = EXCLUDED.first_words;
    """
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (id, assistant_id, user_id, first_words))
        connection.commit()
        return "upserted"
    except Exception as e:
        log_issue(e, add_thread_details_in_db, f"For thread ID: {id}")
        return "error"

def get_assistant_list_from_db(connection: Any, client_id: str) -> list[dict[str, Union[str, int]]]:
    """
    Fetch a list of assistants from the DB.

    Args:
        client_id (str): client id for the operation.

    Returns:
        List[Dict[str, Union[str, int]]]: A list of dictionaries with assistant 'id' and 'assistant_name'.
    """
    query = "SELECT id, assistant_name FROM assistants where client_id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query,(client_id,))
            results = cursor.fetchall()
        return [{"id": row[0], "name": row[1]} for row in results]
    except Exception as e:
        log_issue(e, get_assistant_list_from_db)
        return []

def get_last_thread_id_from_db(connection: Any, assistant_id: str) -> list[str]:
    """
    Fetch a list of assistants from the DB.

    Args:
        assistant_id (str): assistant id for the operation.

    Returns:
        If thread exists then last thread id, Else [] response
    """
    query = "SELECT id FROM threads WHERE assistant_id = %s ORDER BY date_added DESC LIMIT 1;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query,(assistant_id,))
            results = cursor.fetchall()
        
        if results:
            last_thread_id = results[0][0]
            return [last_thread_id]
        else:
            return []
    except Exception as e:
        log_issue(e, get_assistant_list_from_db)
        return []
    
def get_threads_by_date_with_first_words(connection:Any, user_id:int) -> Union[list[dict[str, Any]], str]:
    """
    Retrieves the thread_id and first_words of that thread id.

    Args:
        user_id (int): user id for the get history.
    
    Returns:
        (dict) Dict containing the thread_id,first_words, time and assistant_id for that assistant. String error otherwise.
    """
    query = """
    SELECT 
        id as thread_id, 
        first_words,
        CASE 
            WHEN date_added >= CURRENT_DATE THEN 'today'
            WHEN date_added >= CURRENT_DATE - INTERVAL '1 day' AND date_added < CURRENT_DATE THEN 'yesterday'
            WHEN date_added >= CURRENT_DATE - INTERVAL '7 days' AND date_added < CURRENT_DATE - INTERVAL '1 day' THEN 'previous_7_days'
            WHEN date_added >= CURRENT_DATE - INTERVAL '30 days' AND date_added < CURRENT_DATE - INTERVAL '7 days' THEN 'previous_30_days'
            ELSE 'Older'
        END as time_category,
        assistant_id
    FROM 
        threads
    WHERE user_id= %s
    ORDER BY 
        date_added DESC;
    """

    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (user_id,))
            threads_data = cursor.fetchall()
        return threads_data
    except Exception as e:
        log_issue(e, get_threads_by_date_with_first_words)
        return "error"


def insert_file_into_library(connection: Any, id: str, client_id: int, file_name: str) -> Union[tuple, str]:
    """
    Inserts a file record into the library database.

    Args:
    - id: File ID.
    - client_id: Client ID associated with the file.
    - file_name: Name of the file.

    Returns:
        File ID and file name if successful, 'error' otherwise.
    """
    file_values = (id, client_id, file_name)
    query = "INSERT INTO library (id, client_id, file_name) VALUES (%s, %s, %s);"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, file_values)
        connection.commit()
        return (id, file_name)
    except Exception as e:
        log_issue(e, insert_file_into_library, f"For file ID: {id}, file name: {file_name}")
        return "error"

def insert_file_size_of_client(connection:Any, total_file_size_in_mb: int, client_id: int) -> Union[float, str]:
    """
    Update total_file_size_in_mb in clients table.

    Args:
    - total_file_size_in_mb (int): total_file_size_in_mb associated with the client_id.
    - client_id (int):  Client ID.

    Returns:
        total_file_size_in_mb if succesful, "error" otherwise.
    """
    values = (total_file_size_in_mb, client_id)
    query = "UPDATE clients SET total_file_size_in_mb = %s WHERE id= %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, values)
        connection.commit()
        return total_file_size_in_mb
    except Exception as e:
        log_issue(e, insert_file_size_of_client, f"For client ID: {id}")
        return "error"
    
def get_total_file_size_of_client(connection:Any, client_id: int) -> Union[float, str]:
    """
    Retrives total_file_size o the client.

    Args:
    - client_id (int):  Client ID for the operation.

    Returns:
        total_size if succesful, "error" otherwise.
    """
    values = (client_id,)
    query = "SELECT total_file_size_in_mb FROM clients WHERE id= %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, values)
            total_size = cursor.fetchall()
        return total_size
    except Exception as e:
        log_issue(e, get_total_file_size_of_client, f"For client ID: {id}")
        return "error"

def get_files_from_library(connection: Any) -> Union[list, str]:
    """
    Retrieves all file records from the library database.

    Returns:
        (list) List of tuples containing file ID, file name, and date added if successful, 'error' otherwise.
    """
    query = "SELECT id, file_name, date_added FROM library;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query)
            file_data = cursor.fetchall()
        return file_data
    except Exception as e:
        log_issue(e, get_files_from_library)
        return "error"

def edit_assistant_in_db(connection: Any, id: str, assistant_name: str, instructions: str, gpt_model: str) -> str:
    """
    Edit an existing assistant in the DB.

    Args:
    - id (str): ID of the assistant to update.
    - assistant_name (str): Updated name of the assistant.
    - instructions (str): Updated instructions for the assistant.
    - gpt_model (str): Updated GPT model for the assistant.

    Returns:
        (str): Status of the operation ('updated', 'not found', or 'error').
    """
    query = """
        UPDATE assistants 
        SET assistant_name = %s, instructions = %s, gpt_model = %s
        WHERE id = %s;
    """
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (assistant_name, instructions, gpt_model, id))
            if cursor.rowcount == 0:
                return "not found"
            connection.commit()
            return "updated"
    except Exception as e:
        log_issue(e, edit_assistant_in_db, f"ID: {id}, Assistant Name: {assistant_name}")
        return "error"

def delete_file_from_library(connection: Any, file_id: str) -> str:
    """
    Deletes a file record from the library database.

    Args:
        file_id: The ID of the file to be deleted.

    Returns:
        (str) Success message if successful, 'error' otherwise.
    """
    query = "DELETE FROM library WHERE id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (file_id,))
        connection.commit()
        return f"File with ID {file_id} deleted successfully from library."
    except Exception as e:
        log_issue(e, delete_file_from_library, f"For file ID: {file_id}")
        return "error"

# @henry need to modify this when we have to extract it based on user_id
def get_thread_list(connection: Any) -> list[dict[str, Union[str, str]]]:
    """
    Fetch a list of threads from the DB.

    Returns:
        List[Dict[str, Union[str, str]]]: A list of dictionaries with thread id and assistant_id.
    """
    query = "SELECT id, assistant_id FROM threads"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return [{"id": row[0], "assistant_id": row[1]} for row in results]
    except Exception as e:
        log_issue(e, get_assistant_list_from_db)
        return []

# *************************************************************************************************
# ****************************************** TO USE LATER *****************************************
# *************************************************************************************************

# For that we will need to do a login_history table
def get_user_login_count(connection: Any, user_id: int) -> int:
    """
    TBD
    """
    query = "SELECT COUNT(*) FROM login_history WHERE user_id = %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
    except Exception as e:
        log_issue(e, get_user_login_count, f"User ID: {user_id}")
        return 0

def search_clients_in_db(connection: Any, search_term: str) -> list[dict]:
    """
    TBD
    """
    query = "SELECT * FROM clients WHERE client_name LIKE %s OR client_company LIKE %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
            rows = cursor.fetchall()
            keys = ['id', 'client_name', 'client_company', 'client_domain', 'client_email', 'client_pss', 'last_connection']
            return [dict(zip(keys, row)) for row in rows]
    except Exception as e:
        log_issue(e, search_clients_in_db, f"Search Term: {search_term}")
        return []

def search_users_in_db(connection: Any, search_term: str) -> list[dict]:
    """
    TBD
    """
    query = "SELECT * FROM user WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s;"
    try:
        with CursorContextManager(connection) as cursor:
            cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
            rows = cursor.fetchall()
            keys = ['id', 'client_id', 'username', 'first_name', 'last_name', 'user_email', 'user_pss', 'lang', 'ip', 'fraudulent', 'date_added', 'last_visit']
            return [dict(zip(keys, row)) for row in rows]
    except Exception as e:
        log_issue(e, search_users_in_db, f"Search Term: {search_term}")
        return []

# *************************************************************************************************
# *************************************************************************************************

if __name__ == "__main__":
    pass
