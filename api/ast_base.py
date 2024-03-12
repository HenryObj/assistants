# ************************************************************************************************
# ****************************************** IMPORTS *********************************************
from utilities import *
from functools import wraps
import os
import time

# *************************************************************************************************
# ******************************** DECORATOR FOR WRITTEN LOG ************************************
# *************************************************************************************************


def log_function_execution_time(log_file: str = "") -> Callable:
    """
    Decorator function to log the execution time and output of a wrapped function.

    Args:
        log_file (str): The name of the log file. If not specified, it will create "results_current_time.py" in a "logs" folder.

    Returns:
        Callable: The decorated function.
    """
    if not log_file:
        now = get_now(True)
        log_directory = "logs"
        if not os.path.exists(log_directory):
            os.mkdir(log_directory)
        log_file = f"{log_directory}/results_{now}.py"
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            function_name = func.__name__
            try:
                result = func(*args, **kwargs)
                function_output = f"{result}"
            except Exception as e:
                log_issue(e, func, f"{function_name} execution failed")
                result = None
                function_output = "Error occurred"
            end_time = time.time()
            execution_time = round((end_time - start_time), 2)
            log_message = f"# {function_name}: Execution Time: {execution_time} sc ** Output: {function_output}\n"   
            with open(log_file, 'a') as file:
                file.write(log_message)
            return result
        return wrapper
    return decorator

# *************************************************************************************************
# ******************************** ASSISTANT & FILES FUNCTIONS ************************************
# *************************************************************************************************

@log_function_execution_time()
def oai_create_assistant(
    name: str,
    instructions: str,
    model: str,
    option_retrieval: bool = True,
    option_code_interpreter: bool = False,
) -> Optional[str]:
    """
    Creates an assistant.

    Args:
    - name (str): The name of the assistant.
    - instructions (str): The instructions for the assistant.
    - model (str): The model to be used.

    Returns:
        (str) The ID of the created assistant. None if there is an error.
    """
    tools = [{"type": "retrieval"}] if option_retrieval else []
    if option_code_interpreter:
        tools.append({"type": "code_interpreter"})
    try:
        assistant = client.beta.assistants.create(
            name=name, instructions=instructions, tools=tools, model=model
        )
        return assistant.id
    except Exception as e:
        log_issue(e, oai_create_assistant, f"Name: {name}, Model: {model}")
        return None

@log_function_execution_time()
def oai_update_assistant(assistant_id: str,name: str, instructions: str, model: str) -> Optional[dict]:
    """
    update an assistant, avaialble options are name, model, description, instructions, tools, file_ids.

    Args:
        assistant_id (str): The id of the assistant.
        name (str): The name to update for the assistant.

    Returns:
        (bool) True if the updation was successful. None otherwise.
    """

    try:
        result= client.beta.assistants.update(
            assistant_id=assistant_id,
            name=name,
            instructions=instructions,
            model=model
        )
        return result
    except Exception as e:
        log_issue(e, oai_update_assistant, f"Name: {name}")
        return None

@log_function_execution_time()
def oai_delete_assistant(assistant_id: str) -> bool:
    """
    Deletes an assistant.

    Args:
        assistant_id (str): The ID of the assistant to be deleted.

    Returns:
        (bool) True if the deletion was successful. False otherwise.
    """
    try:
        client.beta.assistants.delete(assistant_id)
        print(f"Assistant {assistant_id} deleted 👌")
        return True
    except Exception as e:
        log_issue(e, oai_delete_assistant, f"Assistant ID: {assistant_id}")
        return False

@log_function_execution_time()
def oai_list_assistants(order: str = "desc", limit: int = 20) -> Optional[dict]:
    """
    Lists all assistants.

    Parameters:
    - order (str): The order of the list ('asc' or 'desc').
    - limit (int): The maximum number of assistants to return.

    Returns:
        (dict) Dict of the assistants_id as keys and assistant_name as value. None if there is an error.
    """
    try:
        assistants = client.beta.assistants.list(order=order, limit=limit)
        details = {assistant.id:assistant.name for assistant in assistants}
        return details
    except Exception as e:
        log_issue(e, oai_list_assistants)
        return None

@log_function_execution_time()
def oai_upload_file(filepath: str) -> Optional[tuple]:
    """
    Uploads a file to the OAI storage for use with an assistant, checking both individual and total organization file size limits.
    If a file with the same name exists, checks for content difference before deciding to upload.

    Args:
        filepath (str): Path to the file to be uploaded.

    Returns:
        (tuple) The ID and name of the file. None if there is an error.
    """
    if not os.path.exists(filepath):
        return None
    file_size = os.path.getsize(filepath)
    if file_size > (INDIVIDUAL_FILE_SIZE_LIMIT * 1024 * 1024):  # 512 MB
        print(f"File size exceeds individual limit of {INDIVIDUAL_FILE_SIZE_LIMIT} MB: {filepath}")
        return None
    total_org_file_size = oai_check_organization_file_usage()
    if total_org_file_size is not None and (total_org_file_size + file_size) > (ORGANIZATION_FILE_SIZE_LIMIT * 1024 * 1024):  # 100 GB
        print(f"Uploading this file will exceed the total organization limit of {ORGANIZATION_FILE_SIZE_LIMIT} GB")
        return None
    filename = os.path.basename(filepath)
    try:
        matching_files = client.files.list()
        for file in matching_files:
            if file.filename == filename and file.bytes == file_size:
                # Temporary logic to match bytes size
                return (file.id, file.filename)
        # Upload new file if no match found
        with open(filepath, "rb") as file:
            uploaded_file = client.files.create(file=file, purpose="assistants")
        return (uploaded_file.id, uploaded_file.filename)
    except Exception as e:
        log_issue(e, oai_upload_file, f"For the filepath: {filepath}")
        return None

@log_function_execution_time()
def oai_delete_file(file_id: str) -> bool:
    """
    Deletes a file from the OAI hosting. No assistant will be able to access it anymore.

    Returns:
        (bool): True if it deleted it well. False otherwise
    """
    try:
        client.files.delete(file_id)
        return True
    except Exception as e:
        log_issue(e, oai_delete_file, f"For this file_id ({type(file_id)}): {file_id}")
        return False

def oai_get_name_file(file_id: str) -> Optional[str]:
    """
    Returns the filename of a file from an ID.
    """
    try:
        files = client.files.list()
        for file in files:
            if file.id == file_id: return file.filename
        return None
    except Exception as e:
        log_issue(e, oai_delete_file, f"For this file_id ({type(file_id)}): {file_id}")
        return False

def oai_list_all_files_attached(assistant_id: str) -> Optional[str]:
    """
    Lists the files attached to the assistant.

    Returns:
        The list of all the files attached to a given assistant. None if error.
    """
    try:
        list_files = client.beta.assistants.files.list(assistant_id=assistant_id)
        if list_files.data and isinstance(list_files.data, list):
            return list_files.data
    except Exception as e:
        log_issue(e,oai_list_all_files_attached,f"For this assistant_id ({type(assistant_id)}): {assistant_id}")
        return None

@log_function_execution_time()
def oai_list_all_files() -> Optional[dict]:
    """
    Lists the files of the current organization.

    Returns:
        (dict) The list of all the files for the current organization as dictionnary with key-value pair "name: id". None if error.
    """
    # @ Mayur, we might want to add the organization as a parameter.
    try:
        files = client.files.list()
        results = {}
        if files and list(files):
            for file in files:
                results[file.filename] = file.id
            return results
    except Exception as e:
        log_issue(e,oai_list_all_files)
        return None

@log_function_execution_time()
def oai_attach_file(assistant_id: str, file_id: str) -> bool:
    """
    Attaches an uploaded file to a specific assistant.

    Returns:
        (bool) True if the file was correctly attached. False otherwise
    """
    try:
        data = client.beta.assistants.files.create(assistant_id=assistant_id, file_id=file_id)
        return data
    except Exception as e:
        log_issue(e,oai_attach_file,f"For this assistant_id ({type(assistant_id)}): {assistant_id} and this file_id ({type(file_id)}): {file_id}")
        return False
    
@log_function_execution_time()
def oai_detach_file(assistant_id: str, file_id: str) -> bool:
    """
    Detaches a file from an assistant. The assistant can no longer reference this file.

    Returns:
        (bool) True if it detached it well. False otherwise
    """
    try:
        client.beta.assistants.files.delete(assistant_id=assistant_id, file_id=file_id)
        return True
    except Exception as e:
        log_issue(e,oai_detach_file,f"For this assistant_id ({type(assistant_id)}): {assistant_id} and this file_id ({type(file_id)}): {file_id}")
        return False

@log_function_execution_time()
def oai_check_file_usage(assistant_id: str) -> Optional[int]:
    """
    Checks the total size of files associated with a specific assistant.

    Parameters:
        assistant_id (str): The ID of the assistant.

    Returns:
        (int) Total size of files in MB. None if there is an error.
    """
    try:
        total_size = 0
        files = client.beta.assistants.files.list(assistant_id=assistant_id)
        for file in files:
            file_info = client.files.retrieve(file.id)
            total_size += file_info.bytes      # @henry, replaced size with bytes to avoid KeyError: size
        return total_size / (1024 * 1024)  # Convert to MB     # @henry, with // it gives 0 file size for very small file, so i changed it to / - Thank you
    except Exception as e:
        log_issue(e,oai_check_file_usage,f"For this assistant_id ({type(assistant_id)}): {assistant_id}")
        return None

@log_function_execution_time()
def oai_check_organization_file_usage() -> Optional[int]:
    """
    Checks the total size of files uploaded by the organization.

    Returns:
        (int) Total size of files in MB. None if there is an error.
    """
    try:
        total_size = 0
        files = client.files.list()
        for file in files:
            total_size += file.bytes         # replaced the size with bytes because it was giving KeyError: size
        return total_size / (1024 * 1024)  # Convert to MB
    except Exception as e:
        log_issue(e, oai_check_organization_file_usage)
        return None

@log_function_execution_time()
def oai_get_number_of_files_attached(assistant_id: str) -> Optional[int]:
    """
    Retrieves the number of files attached to a specific assistant.

    Returns:
        (int) The number of files attached. None if there is an error.
    """
    try:
        files = client.beta.assistants.files.list(assistant_id=assistant_id)
        return len(files.data)
    except Exception as e:
        log_issue(e, oai_get_number_of_files_attached, f"For this assistant_id ({type(assistant_id)}): {assistant_id}")
        return None

@log_function_execution_time()
def oai_get_files_attached(assistant_id: str) -> Optional[list[dict]]:
    """
    Retrieves the files attached to a specific assistant.

    Returns:
        (List(dict)) The list of files attached. None if there is an error.
    """
    try:
        files = client.beta.assistants.files.list(assistant_id=assistant_id)
        return [
            {
                "id": files.id,
                "object": files.object,
                "created_at": files.created_at,
                "assistant_id": files.assistant_id
            }
            for files in files.data
        ]
    except Exception as e:
        log_issue(e, oai_get_number_of_files_attached, f"For this assistant_id ({type(assistant_id)}): {assistant_id}")
        return []

@log_function_execution_time()
def oai_get_assistant_details(assistant_id: str) -> Optional[dict]:
    """
    Retrieves details about a specific assistant.

    Returns:
        (dict) Dictionary with assistant details. None if there is an error.
    """
    try:
        assistant = client.beta.assistants.retrieve(assistant_id)
        details = {
            "id": assistant.id,
            "name": assistant.name,
            "model": assistant.model,
            "instructions": assistant.instructions,
        }
        return details
    except Exception as e:
        log_issue(e, oai_get_assistant_details, f"Assistant ID: {assistant_id}")
        return None

@log_function_execution_time()
def oai_get_assistant_file_details(assistant_id: str, file_id: str) -> Optional[dict]:
    """
    Retrieves details about a specific assistant file.

    Returns:
        (dict) Dictionary with assistant file details. None if there is an error.
    """
    try:
        files = client.beta.assistants.files.retrieve(assistant_id=assistant_id, file_id=file_id)
        details = {
            "id": files.id,
            "object": files.object,
            "created_at": files.created_at,
            "assistant_id": files.assistant_id,
        }
        return details
    except Exception as e:
        log_issue(e, oai_get_assistant_file_details, f"Assistant ID: {assistant_id} with File_ID: {file_id}")
        return None

# @henry, haven't added a test case for this. because i am not sure, we will need it or not in future.
@log_function_execution_time()
def oai_get_message_file_details(thread_id: str, message_id: str, file_id: str) -> Optional[dict]:
    """
    Retrieves details about a specific message file.

    Returns:
        (dict) Dictionary with message file details. None if there is an error.
    """
    try:
        message_file = client.beta.threads.messages.files.retrieve(thread_id=thread_id, message_id=message_id, file_id=file_id)
        return {
            "id": message_file.id,
            "object": message_file.object,
            "created_at": message_file.created_at,
            "message_id": message_file.message_id,
        }
    except Exception as e:
        log_issue(e, oai_get_message_file_details, f"Thread ID: {thread_id} with Message ID: {message_id} and File ID: {file_id}")
        return None

@log_function_execution_time()
def oai_modify_message(message_id: str, thread_id: str, **modification_info) -> bool:
    """
    Modify the details for a specific message.

    Returns:
        (bool) True if the updation was successful. False otherwise.
    """
    try:
        client.beta.threads.messages.update(message_id=message_id, thread_id=thread_id, metadata=modification_info)
        return True
    except Exception as e:
        log_issue(e, oai_modify_message, f"message_id: {message_id} with thread_id: {thread_id}")
        return False

@log_function_execution_time()
def oai_modify_thread(thread_id: str, **modification_info) -> bool:
    """
    Modify the details for a specific thread.

    Returns:
        (bool) True if it update it well. False otherwise
    """
    try:
        client.beta.threads.update(thread_id=thread_id,  metadata=modification_info)
        return True
    except Exception as e:
        log_issue(e, oai_modify_thread, f"Thread ID: {thread_id}")
        return False

@log_function_execution_time()
def oai_delete_thread(thread_id: str) -> bool:
    """
    Delete a specific thread.

    Returns:
        (bool) True if it deleted it well. False otherwise
    """
    try:
        client.beta.threads.delete(thread_id=thread_id)
        return True
    except Exception as e:
        log_issue(e, oai_delete_thread, f"Thread ID: {thread_id}")
        return False

@log_function_execution_time()
def oai_modify_run(thread_id: str, run_id: str, **modification_info) -> bool:
    """
    Modifies the details of a specific run.

    Returns:
        (bool) True if the updation was successful. False otherwise.
    """
    try:
        client.beta.threads.runs.update(thread_id=thread_id, run_id=run_id, metadata=modification_info)
        return True
    except Exception as e:
        log_issue(e, oai_modify_run, f"Thread ID: {thread_id} with Run ID:{run_id}")
        return False
 
@log_function_execution_time()
def oai_get_list_of_run_steps(thread_id: str, run_id: str) -> Optional[list[dict]]:
    """
    Retrieves list of run steps belonging to a specific run.

    Returns:
        (dict) Dictionary with details about the list of run steps . None if there is an error.
    """
    try:
        run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run_id)
        return [
            { "id": run_step.id, "run_id": run_step.run_id, "type": run_step.type }
            for run_step in run_steps
        ]
    except Exception as e:
        log_issue(e, oai_get_list_of_run_steps, f"Thread ID: {thread_id} with Run ID:{run_id}")
        return None

# *************************************************************************************************
# ******************************** THREAD & RUN FUNCTIONS ******************************************
# *************************************************************************************************

@log_function_execution_time()
def oai_create_thread() -> Optional[str]:
    """
    Creates a new thread.

    Returns:
    (str) The ID of the file. None if there is an error.
    """
    try:
        empty_thread = client.beta.threads.create()
        return empty_thread.id
    except Exception as e:
        log_issue(e, oai_create_thread)

@log_function_execution_time()
def oai_add_message_to_thread(
    thread_id: str, message: str, role: str = "user"
) -> Optional[str]:
    """
    Adds a message to a given thread.

    Returns:
        (str) The ID of the message. None if there is an error.
    """
    try:
        thread_message = client.beta.threads.messages.create(
            thread_id=thread_id, role=role, content=message
        )
        return thread_message.id
    except Exception as e:
        log_issue(e,oai_add_message_to_thread,f"For this thread_id ({type(thread_id)}): {thread_id} and message: {message}")
        return None

@log_function_execution_time()
def oai_get_message_details(thread_id: str,message_id: str) -> Optional[dict]:
    """
    Retrive a message information using thread_id and message_id

    Returns:
        (dict) id, content and role of the message as dict. None if there is an error.
    """
    try:
        message = client.beta.threads.messages.retrieve(thread_id=thread_id, message_id=message_id)
        return {
            "id": message.id,
            "content": message.content[0].text.value,
            "role": message.role
        }
    except Exception as e:
        log_issue(e, oai_get_message_details, f"Message ID: {message_id}")
        return None

@log_function_execution_time()
# Function to retrieve all messages from a thread
def oai_get_all_messages_from_thread(thread_id: str) -> Optional[list[dict]]:
    """
    Retrieves all thread message information using thread_id.

    Returns:
        (list) id, content and role of the message as list of dict. None if there is an error.
    """
    try:
        messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc")
        return [
            {"id": msg.id, "content": msg.content[0].text.value, "role": msg.role}
            for msg in messages.data
        ]
    except Exception as e:
        log_issue(e, oai_get_all_messages_from_thread, f"Thread ID: {thread_id}")
        return None
    
@log_function_execution_time()
# Function to retrieve all messages from a thread
def oai_get_all_files_from_message(thread_id: str, message_id:str) -> Optional[list[dict]]:
    """
    Retrieve all files using thread_id and message_id

    Args:
    - thread_id (str): The ID of the thread.
    - message_id (str): The ID of the message

    Returns:
        (list) id of the file as list of dict. None if there is an error.
    """
    try:
        message_files = client.beta.threads.messages.files.list(thread_id=thread_id, message_id=message_id)
        return [ 
            {"id": file.id}
            for file in message_files.data 
        ]
    except Exception as e:
        log_issue(e, oai_get_all_files_from_message, f"Thread ID: {thread_id}")
        return None

@log_function_execution_time()
# Function to cancel a run
def oai_cancel_run(thread_id: str, run_id: str) -> Optional[bool]:
    """
    Cancel a run for a given thread with a specified run_id.

    Returns:
        (bool) True if run cancelled successfully. False if there is an error.
    """
    try:
        client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
        return True
    except Exception as e:
        log_issue(e, oai_cancel_run, f"Thread ID: {thread_id}, Run ID: {run_id}")
        return False

@log_function_execution_time()
# Then we create a run which takes the thread id and the assistant id as input
def oai_create_run(thread_id: str, assistant_id: str) -> Optional[str]:
    """
    Creates a run for a given thread with a specified assistant.

    Returns:
    - (str) The ID of the run. None if there is an error.
    """
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id
        )
        if run.status == "requires_action":
            # TODO SOMETHING - Implement logic to handle 'requires_action' state
            pass
        return run.id
    except Exception as e:
        log_issue(e,oai_create_run,f"For this thread_id ({type(thread_id)}): {thread_id} and assistant_id: {assistant_id}")
        return None

@log_function_execution_time()
def oai_wait_on_run(thread_id: str, run_id: str) -> Optional[str]:
    """
    Waits for a run to complete and returns its status.

    Returns:
    - (str) The status of the run. None if there is an error.
    """
    try:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id,
        )
        while run.status in ["queued", "in_progress"]:
            time.sleep(0.02)  # Doing steps of 0.02 seconds @Mayur - let's do something better here
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
        return run.status
    except Exception as e:
        log_issue(e,oai_wait_on_run,f"For this thread_id ({type(thread_id)}): {thread_id} and run_id: {run_id}")
        return None

@log_function_execution_time()
def oai_get_latest_message(thread_id: str) -> Optional[str]:
    """
    Retrieves the latest message from a thread, optimized for large threads.

    Returns:
    - (str) The content of the latest message. None if there is an error.
    """
    try:
        messages = client.beta.threads.messages.list(thread_id=thread_id, limit=1, order='desc')
        if messages and messages.data:
            return messages.data[0].content[0].text.value
        return None
    except Exception as e:
        log_issue(e, oai_get_latest_message, f"For this thread_id ({type(thread_id)}): {thread_id}")
        return None
    
@log_function_execution_time()  
def oai_get_latest_message_id(thread_id: str) -> Optional[str]:
    """
    Retrieves the latest message id from a thread, optimized for large threads.

    Returns:
    - (str) The message id of the latest message. None if there is an error.
    """
    try:
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,limit=1, order="desc"
        )
        if messages and messages.data:
            return messages.data[0].id
        return None
    except Exception as e:
        log_issue(e,oai_get_latest_message_id,f"For this thread_id ({type(thread_id)}): {thread_id}")
        return None

@log_function_execution_time()
def oai_extract_annotations_and_process_message(thread_id: str, message_id: str) -> Optional[dict]:
    """
    Extracts annotations from a given message and processes the message content accordingly.

    Returns:
    - (dict) A dictionary with processed message content and extracted annotations. None if there is an error.
    """
    try:
        message = client.beta.threads.messages.retrieve(
            thread_id=thread_id, message_id=message_id
        )
        message_content = message.content[0].text
        annotations = message.content[0].text.annotations
        citations = []

        for index, annotation in enumerate(annotations):
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citation_text = (
                    f" [{index}] {file_citation.quote} from {cited_file.filename}"
                )
                citations.append(citation_text)
                message_content.value = message_content.value.replace(
                    annotation.text, citation_text
                )
            elif file_path := getattr(annotation, "file_path", None):
                cited_file = client.files.retrieve(file_path.file_id)
                file_link = f" [{index}] Click <here> to download {cited_file.filename}"
                citations.append(file_link)
                message_content.value = message_content.value.replace(
                    annotation.text, file_link
                )

        processed_message = {"message": message_content.value, "citations": citations}
        return processed_message
    except Exception as e:
        log_issue(e,oai_extract_annotations_and_process_message,f"For this message_id ({type(message_id)}): {message_id} and thread_id ({type(thread_id)}): {thread_id}")
        return None

@log_function_execution_time()
def oai_get_run_history(thread_id: str, limit: int = 20) -> Optional[list[dict]]:
    """
    Retrieves the history of runs for a specific assistant.

    Parameters:
    - thread_id (str): Thread_id of the openapi
    - limit (int): The number of runs to retrieve.

    Returns:
    - List of dictionaries containing run details. None if there is an error.
    """
    try:
        runs = client.beta.threads.runs.list(thread_id=thread_id, limit=limit)
        run_history = [
            {"run_id": run.id, "status": run.status, "created_at": run.created_at}
            for run in runs
        ]
        return run_history
    except Exception as e:
        log_issue(e,oai_get_run_history,f"For this thread_id ({type(thread_id)}): {thread_id}")
        return None

@log_function_execution_time()
def oai_get_thread_details(thread_id: str) -> Optional[dict]:
    """
    Retrieves details about a specific thread.

    Returns:
    - Dictionary with thread details. None if there is an error.
    """
    try:
        thread = client.beta.threads.retrieve(thread_id)
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        details = {
            "id": thread.id,
            "messages": [msg.content[0].text.value for msg in messages.data],
        }
        return details
    except Exception as e:
        log_issue(e, oai_get_thread_details, f"Thread ID: {thread_id}")
        return None

@log_function_execution_time()
def oai_get_run_status(thread_id: str, run_id: str) -> Optional[str]:
    """
    Retrieves the status of a specific run.

    Returns:
    - (str) The status of the run. None if there is an error.
    """
    try:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        return run.status
    except Exception as e:
        log_issue(e, oai_get_run_status, f"Thread ID: {thread_id}, Run ID: {run_id}")
        return None

# *************************************************************************************************
# ******************************** LOG SUPPORT FUNCTIONS ******************************************
# *************************************************************************************************

def print_files_and_attached_files(assistant_id: str) -> None:
    """
    Prints all the files uploaded to the OAI storage and the files attached to a specific assistant.

    Parameters:
    - assistant_id (str): The ID of the assistant.
    """
    try:
        # Print all uploaded files
        all_files = client.files.list()
        print("All Uploaded Files:")
        for file in all_files:
            print(f"File ID: {file.id}, File Name: {file.filename}")
        # Print files attached to the assistant
        attached_files = client.beta.assistants.files.list(assistant_id=assistant_id)
        if not len(list(attached_files)):
            print("\nNo File Attached to the Assistant:")
        else:
            print("\nFiles Attached to the Assistant:")
            for file in attached_files:
                print(f"    File ID: {file.id}")
            print()
    except Exception as e:
        log_issue(e,print_files_and_attached_files,f"For this assistant_id ({type(assistant_id)}): {assistant_id}")

def print_assistants_and_attached_file() -> None:
    """
    Prints all the assistants, their info and the files attached to each assistants.

    Parameters:
    - assistant_id (str): The ID of the assistant.
    """
    try:
        assistants = client.beta.assistants.list(order="desc")
        for i, assistant in enumerate(assistants):
            assistant_name = assistant.name
            print(f"***** Assistant # {i+1} *****")
            print(f"Assistant name: {assistant_name}")
            print(f"ID: {assistant.id}\nModel: {assistant.model}\nInstructions: {assistant.instructions}\n")
            attached_files = client.beta.assistants.files.list(assistant_id=assistant.id)
            if not len(list(attached_files)):
                print(f"* No File Attached to {assistant_name}:")
            else:
                print(f"Files Attached to {assistant_name}")
                for file in attached_files:
                    print(f"  ID: {file.id} - Name: {oai_get_name_file(file.id)}")
            print("\n")
    except Exception as e:
        log_issue(e,print_assistants_and_attached_file)

# *************************************************************************************************
# *************************************************************************************************

if __name__ == "__main__":
    print(oai_list_all_files())

