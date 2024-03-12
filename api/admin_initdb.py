# IMPORTANT NOTE:
# This script will initialize the database by default
# But if you pass the -rm flag, it will delete the database instead.

# ************************************************************************************************
# ****************************************** IMPORTS *********************************************

from ast_db_base import get_db_connection, CursorContextManager
from ast_base import PATH, log_issue

import argparse

# ****** PATHS & GLOBAL VARIABLES *******

# *************************************************************************************************
# ****************************************** FUNCTIONS *********************************************
# *************************************************************************************************

def init_tables(schema_name="public"):
    try:
        with get_db_connection() as connection:
            with CursorContextManager(connection) as cursor:
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
            connection.commit()
            with open(f"{PATH}/schema.sql") as schema_file:
                script = schema_file.read()
            with CursorContextManager(connection) as cursor:
                cursor.execute(script)
            connection.commit()
        print("All tables were successfully created ✅")
    except Exception as e:
        print(e)
        log_issue(e, init_tables, "")

def delete_all_tables(schema_name = "public"):
    '''
    Will delete all tables and their content. Be careful with this function.
    I am using it in dev.
    '''
    try:
        with get_db_connection() as connection:
            inp = input("Are you sure that you want to delete everything? Enter 'yes' to confirm:  ")
            if inp == 'yes':
                with CursorContextManager(connection) as cursor:
                    cursor.execute(f"DROP SCHEMA {schema_name} CASCADE;")
                connection.commit()
                print("✅ Everything has been deleted")
            else:
                print("Operation aborted")
    except Exception as e:
        log_issue(e, delete_all_tables, f"Schema: {schema_name}")

# *************************************************************************************************
# *************************************************************************************************

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Database initialization script')
    parser.add_argument('-rm', '--remove', action='store_true', help='Remove the database')
    args = parser.parse_args()
    if args.remove:
        delete_all_tables()
    else:
        init_tables()
