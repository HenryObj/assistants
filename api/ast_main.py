# ************************************************************************************************
# ****************************************** IMPORTS *********************************************

from ast_base import *

# *************************************************************************************************
# ************************************* FUNCTIONS ********************************************
# *************************************************************************************************

@log_function_execution_time()
def oai_ask_question_assistant(question: str, assistant_id: str, thread_id:str="") -> list:
    """
    Asks a question to an assistant.

    Returns:
        (list) [response, thread_id]: response being the response from the assistant

    Notes:
    - Specify the thread_id if the question is a continuation of an existing conversation.
    - If the thread_id is not specify, we will create a new conversation (new thread)
    """
    if thread_id == "": thread_id = oai_create_thread()
    result = [ERROR_ASSISTANT_DEFAULT, thread_id]
    oai_add_message_to_thread(thread_id, question)
    run_id = oai_create_run(thread_id, assistant_id)
    run_status = oai_wait_on_run(thread_id, run_id)
    # guard clause
    if run_status != "completed": return result, thread_id
    latest_message_id = oai_get_latest_message_id(thread_id=thread_id)
    result[0] = oai_extract_annotations_and_process_message(thread_id=thread_id, message_id=latest_message_id)
    return [result, thread_id]

@log_function_execution_time()
def oai_upload_file_and_attach_with_assistant(assistant_id: str, file_path: str)-> Union[str, bool]:
    """
    Attach a file to the assistant

    Returns:
        (str): the file_id of the uploaded file. False if something went wrong.
    """
    file_id = oai_upload_file(filepath=file_path)
    if file_id:
        return oai_attach_file(assistant_id=assistant_id, file_id=file_id) 
    return False

@log_function_execution_time()
def oai_detach_file_and_delete(assistance_id: str, file_id:str) -> bool:
    """
    Detach the file from assistant and delete it 

    Returns:
        (bool) True if file is successfuly detached and deleted. Fase otherwise.
    """
    return oai_detach_file(assistant_id=assistance_id, file_id=file_id) and oai_delete_file(file_id=file_id)


# @Mayur - this function is useless as you are returning the parameters. Review it 
"""@log_function_execution_time()
def oai_thread_and_message_details(thread_id: str, message_id: str) -> str:
    '''
    Get thread and message details

    Returns:
        thread_id and message_id of the detail
    '''
    oai_get_thread_details(thread_id=thread_id)
    oai_get_message_details(thread_id=thread_id, message_id=message_id)
    return thread_id, message_id"""

@log_function_execution_time()
def oai_delete_thread_and_assistant(thread_id: str, assistance_id: str) -> bool:
    """
    Get thread and message details

    Returns:
        (bool) True if successfuly detleted the thread and message. False otherwise.
    """
    return oai_delete_thread(thread_id=thread_id) and oai_delete_assistant(assistant_id=assistance_id)
    

if __name__ == "__main__":
    pass

# Tests
# questions = ["uncondition love is a myth?","what to do without thinking?","what is the outcome of this book?"]
"""thread_id=""
questions = ["who is Grayson?","what is the nick name given to her?","where mom and dad spent entire week?"]
role=DEFAULT_ROLE_CHATGPT
ast_id = oai_create_assistant("Test_assistant", instructions=role, model=MODEL_CHAT, option_retrieval=True, option_code_interpreter=True)

#attach a file to assistant
file_id= oai_upload_file_and_attach_with_assistant(assistant_id=ast_id,file_path="/home/hp/Documents/C Professional/Projects/henry/git/assistants/assistants/Untitled document (2).pdf") # place a file path
for question in questions:
    result, thread_id = oai_ask_question_assistant(question,ast_id, thread_id=thread_id)
    
    print(test_normal_endpoint(question, role))
latest_message_id = oai_get_latest_message_id(thread_id=thread_id)
oai_detach_file_and_delete(assistance_id=ast_id, file_id=file_id)
oai_delete_thread_and_assistant(thread_id=thread_id, assistance_id=ast_id)"""




