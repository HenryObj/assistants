# ************************************************************************************************
# ****************************************** IMPORTS *********************************************

import argparse
from ast_db_base import get_assistant_list_from_db, get_db_connection, CursorContextManager, get_files_from_library, get_thread_list
from ast_base import PATH, log_issue, oai_delete_assistant, oai_delete_file, oai_delete_thread

# ****** PATHS & GLOBAL VARIABLES *******

# *************************************************************************************************
# ****************************************** FUNCTIONS *********************************************
# *************************************************************************************************

# You need to modify this if you want to do this operations for multiple clients, as each client have different API_KEY
def delete_from_OAI():
    '''
    Will delete all files, assistant and threads from OAI.
    '''
    try:
        with get_db_connection() as connection:
            ### DELETE FILES ###
            try:
                file_list = get_files_from_library(connection=connection)
                for file_id, file_name, date_added in file_list:
                    oai_delete_file(file_id=file_id)
            except:
                log_issue(e, delete_from_OAI, f"Error in delete file.")
            
            ### DELETE ASSISTANTS ###
            try:
                assistant_list = get_assistant_list_from_db(connection=connection, client_id=1) # need to do logic for multiple clients in future
                for assistant_details in assistant_list:
                    oai_delete_assistant(assistant_id=assistant_details.get('id'))
            except:
                log_issue(e, delete_from_OAI, f"Error in delete assistants.")
            
            ### DELETE THREADS ###
            try:
                thread_list = get_thread_list(connection=connection)
                for thread_details in thread_list:
                    oai_delete_thread(thread_id=thread_details.get('id'))
            except:
                log_issue(e, delete_from_OAI, f"Error in delete threads.")

    except Exception as e:
        print(e)
        log_issue(e, delete_from_OAI, "Error in delete files, assistant and threads")

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
    parser = argparse.ArgumentParser(description='Database delete script')
    delete_from_OAI()
    delete_all_tables()