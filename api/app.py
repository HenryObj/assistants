# ************************************************************************************************
# ****************************************** IMPORTS *********************************************

from app_classes import *
from ast_db_base import *
from ast_base import *
from ast_main import *

from fastapi import FastAPI, Depends, File, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

# ****************************************** APP INIT **********************************************

app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# *************************************************************************************************
# ****************************************** ENDPOINTS ********************************************
# *************************************************************************************************


# ******************************************** CLIENT **********************************************

@app.post("/clients", response_model= GeneralResponse)
async def post_client(input_data: Client,
    connection=Depends(get_connection_dependency)) -> dict:
    """
    Create a new client in the database.

    Returns:
        dict: Status indicating if the client was added successfully, already existed, or there was an error.
    """
    verbose = True
    if verbose: print(f"\n@ We enter the add client endpoint. Input Data:\n{input_data}")
    status, client_id = add_client_in_db(connection, input_data.client_name, input_data.client_company, input_data.client_domain, input_data.client_email,  input_data.client_pss, input_data.client_logo)
    if status == "new":
        return GeneralResponse(status=ResultsStatus.success, message='Client added to the DB', data={'client_id': str(client_id)})
    elif status =="old":
        return GeneralResponse(status=ResultsStatus.success, message='Client already exists in the DB', data={'client_id': str(client_id)})
    else:
        return GeneralResponse(status=ResultsStatus.error, message='Error while adding the client to the DB')

@app.delete("/clients", response_model=GeneralResponse)
async def delete_client(input_data: ClientInput, connection=Depends(get_connection_dependency)) -> dict:
    """
    Delete a client from the database based on client_id.

    Args:
        client_id (int): The ID of the client to delete.

    Returns:
        dict: Status indicating the outcome of the delete operation.
    """
    verbose = True
    client_id = input_data.client_id
    if verbose: print(f"\n@ Deleting client with ID: {client_id}")

    result = delete_client_from_db(connection, client_id)
    if result == 'deleted':
        return GeneralResponse(status=ResultsStatus.success, message='Client deleted successfully')
    elif result == 'not found':
        return GeneralResponse(status=ResultsStatus.error, message='Client not found')
    else:
        return GeneralResponse(status=ResultsStatus.error, message='Error while deleting the client')

@app.put("/clients", response_model=GeneralResponse)
async def update_client_information(input_data: UpdateClientInput, connection=Depends(get_connection_dependency)) -> dict:
    """
    Update client information based on the provided details.

    Args:
        client_id (int): The ID of the client to update.
        input_data (UpdateClientInput): The new client data.

    Returns:
        dict: Status indicating the outcome of the update operation.
    """
    verbose = True
    client_id = input_data.client_id
    if verbose: print(f"\n@ Updating client {client_id}. Input Data:\n{input_data}")

    result = update_client_info_in_db(connection, client_id, input_data.dict(exclude_unset=True))
    if result:
        return GeneralResponse(status=ResultsStatus.success, message="Client information updated successfully")
    else:
        return GeneralResponse(status=ResultsStatus.error, message=f"Failed to update client information for client with id {client_id}")

@app.get("/get-client-data", response_model=GeneralResponse)
async def get_client_data_from_db(client_id: int, connection=Depends(get_connection_dependency)) -> dict:
    """
    Get client data from the database.

    Args:
        client_id (int): The ID of the client to get the data.

    Returns:
        (dict): Status indicating the success or failure of the operation. 
    """
    data = get_client_data(connection=connection, client_id=client_id)
    if data:
        return GeneralResponse(status=ResultsStatus.success, message='Client data retrival successful', data=data)
    else:
        return GeneralResponse(status=ResultsStatus.error, message='Error while retriving client data.')
    
@app.get("/get-client-list", response_model=GeneralResponse)
async def get_client_list_from_db(connection=Depends(get_connection_dependency)) -> dict:
    """
    Get client list from the database.

    Returns:
        (dict): Status indicating the success or failure of the operation. 
    """
    data = get_client_list(connection=connection)
    if data:
        return GeneralResponse(status=ResultsStatus.success, message='Client list retrival successful', data=data)
    else:
        return GeneralResponse(status=ResultsStatus.error, message='Error while retriving client list')

# ******************************************** USER ***********************************************
    
@app.post("/users", response_model= GeneralResponse)
async def add_user(input_data: User, connection=Depends(get_connection_dependency)) -> dict:
    """
    Create a new user in the database.

    Returns:
        (dict): Status indicating if the user was added successfully, already existed, or there was an error.
    """
    verbose = True
    if verbose: print(f"\n@ We enter the add client endpoint. Input Data:\n{input_data}")
    status, username = add_user_in_db(connection, input_data.client_id, input_data.username, input_data.first_name, input_data.last_name,  input_data.user_email, input_data.user_pss, input_data.lang, input_data.ip)
    if status == "added":
        return GeneralResponse(status=ResultsStatus.success, message='User added to the DB', data={'username': str(username)})
    elif status =="exists":
        return GeneralResponse(status=ResultsStatus.error, message='User already exists', data={'username': str(username)})
    else:
        return GeneralResponse(status=ResultsStatus.error, message='Error while adding the user')

@app.delete("/users", response_model=GeneralResponse)
async def delete_user(input_data: UserInput, connection=Depends(get_connection_dependency)) -> dict:
    """
    Delete a user from the database.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        (dict): Status indicating the outcome of the delete operation.
    """
    verbose = True
    user_id = input_data.user_id
    if verbose: print(f"\n@ Deleting user with ID: {user_id}")

    result = delete_user_from_db(connection, user_id)
    if result:
        return GeneralResponse(status=ResultsStatus.success, message='User deleted successfully')
    else:
        return GeneralResponse(status=ResultsStatus.error, message='Error while deleting the user')

@app.put("/users", response_model=GeneralResponse)
async def update_user_information(input_data: UpdateUserInput, connection=Depends(get_connection_dependency)) -> dict:
    """
    Update user information based on the provided details.

    Args:
    - user_id (int): The ID of the user to update.
    - input_data (UpdateUserInput): The new user data.

    Returns:
        (dict): Status indicating the outcome of the update operation.
    """
    user_id = input_data.user_id
    verbose = True
    if verbose: print(f"\n@ Updating User {user_id}. Input Data:\n{input_data}")

    result = update_user_info_in_db(connection, user_id, input_data.dict(exclude_unset=True))
    if result:
        return GeneralResponse(status=ResultsStatus.success, message="User information updated successfully")
    else:
        return GeneralResponse(status=ResultsStatus.error, message=f"Failed to update user information for user with id {user_id}")
    
@app.get("/get-user-list", response_model=GeneralResponse)
async def get_user_list_from_db(connection=Depends(get_connection_dependency)) -> dict:
    """
    Get user list from the database.

    Returns:
        (dict): Status indicating the success or failure of the operation. 
    """
    data = get_user_list(connection=connection)
    if data:
        return GeneralResponse(status=ResultsStatus.success, message='User list retrival successful', data=data)
    else:
        return GeneralResponse(status=ResultsStatus.error, message='Error while retriving user list')

@app.get("/get-user-data", response_model=GeneralResponse)
async def get_user_data_from_db(user_id: int, connection=Depends(get_connection_dependency)) -> dict:
    """
    Get user data from the database.

    Args:
        user_id (int): The ID of the user to get the data.

    Returns:
        (dict): Status indicating the success or failure of the operation. 
    """
    data = get_user_data(connection=connection, user_id=user_id)
    if data:
        return GeneralResponse(status=ResultsStatus.success, message='User data retrival successful', data=data)
    else:
        return GeneralResponse(status=ResultsStatus.error, message='Error while retriving user data.')

# ******************************************** ASSISTANTS ***********************************************
 
@app.post("/create-assistant", response_model=GeneralResponse)
async def create_assistant(request: Assistant, connection=Depends(get_connection_dependency)) -> dict:
    """
    Creates a new assistant.

    Args:
    - name (str): The name of the assistant.
    - instructions (str): The instructions to the assistant.
    - model (str): The model of assistant

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        assistant_id = oai_create_assistant(
            name=request.assistant_name, 
            instructions=request.instructions, 
            model=request.gpt_model
        )

        if assistant_id:
            result = add_assistant_in_db(connection= connection, id= assistant_id, client_id=request.user_id,assistant_name=request.assistant_name, instructions= request.instructions, gpt_model=request.gpt_model)
            if result == "added":
                return GeneralResponse(status=ResultsStatus.success, message='Assistant created successfully.', data =assistant_id)
            else:
                return GeneralResponse(status=ResultsStatus.error, message='Error while adding the assistant')
        else:
            return GeneralResponse(status=ResultsStatus.error, message='Error while adding the assistant')
    except Exception as e:
        log_issue(e, create_assistant, f"For Args {request}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.get("/assistant-list", response_model=GeneralResponse)
async def assistant_list(client_id: int, connection: Any = Depends(get_connection_dependency))->dict:
    """
    Retrieves a list of assistants with their ID and name.

    Args:
        client_id (int): client id to get assistants list.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        assistants = get_assistant_list_from_db(connection=connection, client_id=client_id)
        if assistants:
            data = {"assistant_details": assistants}
            return GeneralResponse(status=ResultsStatus.success, message="Assistant list retrieved successfully", data=data)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="No assistants found.")
    except Exception as e:
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.post("/edit-assistant", response_model=GeneralResponse)
async def edit_assistant(request: EditAssistantRequest, connection=Depends(get_connection_dependency))->dict:
    """
    Edits an assistant.

    Args:
        request (EditAssistantRequest): The request containing assistant ID, name, instructions, and model.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        updated = oai_update_assistant(
            assistant_id=request.assistant_id,
            name=request.name,
            instructions=request.instructions,
            model=request.model
        )
        if updated:
            data = edit_assistant_in_db(connection=connection, id=request.assistant_id, assistant_name=request.name, instructions=request.instructions, gpt_model=request.model)
            return GeneralResponse(status=ResultsStatus.success, message="Assistant edited successfully.", data=updated)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Failed to update assistant")
    except Exception as e:
        log_issue(e, edit_assistant, f"For Args {request}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.get("/get-assistant-details", response_model=GeneralResponse)
async def get_assistant_details(assistant_id: str)->dict:
    """
    Retrieves the details of an assistant.

    Args:
        assistant_id (str): The ID of the assistant.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        result = oai_get_assistant_details(assistant_id=assistant_id)
        if result:
            return GeneralResponse(status=ResultsStatus.success, message="Assistant details retrieved successfully.", data=result)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Failed to get assistant details.")
    except Exception as e:
        log_issue(e, get_assistant_details, f"For Args {assistant_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

# ******************************************** FILES ***********************************************

@app.post("/upload-multiple-files", response_model=GeneralResponse)
async def upload_multiple_files(client_id: int, files: list[UploadFile] = File(...), connection=Depends(get_connection_dependency)) -> dict:
    """
    Uploads multiple files.

    Args:
    - client_id (int): client_id to upload the files.
    - files (List[UploadFile]): The list of files to be uploaded.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        uploaded_files = []
        for file in files:
            file_location = f"{temp_dir}/{file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())

            file_info = oai_upload_file(file_location)
            if file_info is None:
                return GeneralResponse(status=ResultsStatus.error, message=f"File upload failed for {file.filename}")

            uploaded_files.append({
                "file_id": file_info[0], 
                "file_name": file_info[1]
            })
            result = insert_file_into_library(connection=connection, client_id=client_id, id=file_info[0], file_name=file_info[1])
            if not result:
                return GeneralResponse(status=ResultsStatus.error, message="Failed to insert file details into database.")
        total_size = oai_check_organization_file_usage()
        if total_size is not None and uploaded_files:
            update_result = insert_file_size_of_client(connection=connection, client_id=client_id, total_file_size_in_mb=total_size)
            if update_result == "error":
                return GeneralResponse(status=ResultsStatus.error, message="Failed to update file size in database.")
            
            return GeneralResponse(status=ResultsStatus.success, message="Files uploaded successfully and file size updated in database.", data=uploaded_files)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Error while uploading files or updating file size in database.")
    except Exception as e:
        log_issue(e, upload_multiple_files, f"For Args {client_id} and {files}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.get("/total-file-size", response_model=GeneralResponse)
async def get_files_size(client_id: int, connection=Depends(get_connection_dependency)) -> dict:
    """
    Retrives the total file size.

    Args:
        client_id (int): client id to get the total file size of that client

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        total_size = get_total_file_size_of_client(connection=connection, client_id=client_id)
        if total_size:
            return GeneralResponse(status=ResultsStatus.success, message="Total file size.", data= total_size)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Error to get total size of uploaded files.")
    except Exception as e:
        log_issue(e, get_files_size, f"For Args {client_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))
    
@app.get("/assistant-file-list", response_model=GeneralResponse)
async def get_assistant_file_list(assistant_id: str) -> dict:
    """
    Retrives the list of files attached to the assistant.

    Args:
        assistant_id (str): assistant id to get the list of all attached files to that assistant.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        data = oai_get_files_attached(assistant_id=assistant_id)
        if data:
            return GeneralResponse(status=ResultsStatus.success, message="assistant list retrival successful.", data= data)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Error getting assistant list.")
    except Exception as e:
        log_issue(e, get_assistant_file_list, f"For Args {assistant_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))
    
# @@@ Mayur - we should do it for the org ID (here you don't have any args)
@app.get("/get-files", response_model=GeneralResponse)
async def get_files(connection=Depends(get_connection_dependency)) -> dict:
    """
    Retrieves a list of all files from the library.

    Returns:
        A JSON response with the list of files.
    """
    try:
        file_list = get_files_from_library(connection=connection)
        if file_list == "error":
           return GeneralResponse(status=ResultsStatus.error, message="Error retrieving files from database")

        data = [{"file_id": file_id, "file_name": file_name, "date_added": date_added, "formatted_date": f"""Uploaded on {date_added.strftime('%d/%m/%Y')}"""} for file_id, file_name, date_added in file_list]
        return GeneralResponse(status=ResultsStatus.success, message="File list retrieved successfully.", data=data)
    except Exception as e:
        log_issue(e, get_files)
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.delete("/detach-delete-file", response_model=GeneralResponse)
async def detach_delete_file(assistant_id: str, file_id: str) -> dict:
    """
    Detaches a file from an assistant and then deletes it.

    Args:
    - assistant_id (str): The ID of the assistant from which the file is detached.
    - file_id (str): The ID of the file to be detached and deleted.

    Returns:
        A JSON response indicating the success or failure of the operation.
    """
    try:
        result = oai_detach_file_and_delete(assistant_id=assistant_id, file_id=file_id)
        if result:
            return GeneralResponse(status=ResultsStatus.success, message="File detached and deleted successfully", data =None)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Failed to detach and delete file")
    except Exception as e:
        log_issue(e, detach_delete_file, f"For Args {file_id} and {assistant_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.post("/upload-attach-file", response_model=GeneralResponse)
async def upload_attach_file(assistant_id: str, file: UploadFile = File(...)) -> dict:
    """
    Uploads a file and attaches it to an assistant.

    Args:
    - assistant_id (str): The ID of the assistant to attach the file.
    - file (UploadFile): The file to be uploaded and attached.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    try:
        file_id = oai_upload_file_and_attach_with_assistant(assistant_id=assistant_id, file_location=file_location)
        data= {"file_id": file_id}
        return GeneralResponse(status=ResultsStatus.success, message="File attached successfully", data=data)
    except Exception as e:
        log_issue(e, upload_attach_file, f"For Args {assistant_id} and {file}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.post("/attach-files-to-assistant", response_model=GeneralResponse)
async def attach_files_to_assistant(assistant_id: str, file_ids: list[str])->dict:
    """
    Attaches multiple files to an assistant.

    Args:
    - assistant_id (str): The ID of the assistant to attach files.
    - file_ids (List[str]): List of file IDs to be attached.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        successfully_attached = []
        for file_id in file_ids:
            result = oai_attach_file(assistant_id=assistant_id, file_id=file_id)
            if result:
                successfully_attached.append(file_id)

        if successfully_attached:
            return GeneralResponse(status=ResultsStatus.success, message="Files attached to the assistant successfully.", data={"attached_files": successfully_attached})
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Failed to attach files to the assistant.")
    except Exception as e:
        log_issue(e, attach_files_to_assistant, f"For Args {assistant_id} and {file_ids}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))
    
@app.post("/detach-files-from-assistant", response_model=GeneralResponse)
async def detach_files_from_assistant(assistant_id: str, file_ids: list[str])->dict:
    """
    Detaches multiple files from an assistant.

    Args:
    - assistant_id (str): The ID of the assistant from which files are to be detached.
    - file_ids (List[str]): List of file IDs to be detached.

   Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        successfully_detached = []
        for file_id in file_ids:
            result = oai_detach_file(assistant_id=assistant_id, file_id=file_id)
            if result:
                successfully_detached.append(file_id)

        if successfully_detached:
            return GeneralResponse(status=ResultsStatus.success, message="Files detached from the assistant successfully.", data={"detached_files": successfully_detached})
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Failed to detach files from the assistant.")
    except Exception as e:
        log_issue(e, detach_files_from_assistant, f"For Args {assistant_id} and {file_ids}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))
    
@app.post("/modify-assistant-files", response_model=GeneralResponse)
async def modify_assistant_files(request: AssistantFilesModificationRequest) -> dict:
    """
    Modifies the files attached to an assistant.

    Args:
    - request (AssistantFilesModificationRequest): The request containing the assistant ID, and lists of file IDs to attach and detach.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        # Attach Files
        for file_id in request.attach_file_ids:
            oai_attach_file(assistant_id= request.assistant_id, file_id=file_id)
                
        # Detach files
        for file_id in request.detach_file_ids:
            oai_detach_file(assistant_id=request.assistant_id, file_id=file_id)

        return GeneralResponse(status=ResultsStatus.success,message="Assistant files modified successfully.", data={})
    except Exception as e:
        log_issue(e, modify_assistant_files, f"For Args {request}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.delete("/delete-file", response_model=GeneralResponse)
async def delete_file(file_id: str, connection=Depends(get_connection_dependency))->dict:
    """
    Deletes a file.

    Args:
    - file_id (str): The ID of the file to be deleted.

   Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try: 
        # Attempt to delete the file from OpenAI
        oai_result = oai_delete_file(file_id=file_id)
        if not oai_result:
            return GeneralResponse(status=ResultsStatus.error, message='Failed to delete the file')

        # Delete the file from the local database
        db_result = delete_file_from_library(connection=connection, file_id=file_id)
        if db_result != "error":
            return GeneralResponse(status=ResultsStatus.success, message="File deleted successfully", data={"file_id": file_id})
        else:
            return GeneralResponse(status_code=500, detail="Failed to delete file from local database")
    except Exception as e:
        log_issue(e, delete_file, f"For Args {file_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

# ******************************************** THREADS ***********************************************

@app.post("/create-thread", response_model=GeneralResponse)
async def create_thread(request: ThreadRequest, connection=Depends(get_connection_dependency)) -> dict:
    """
    Creates a new thread.

    Args:
        request (ThreadRequest): Request object containing assitant_id and user_id.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        thread_id = oai_create_thread()
        if thread_id:
            result = add_thread_details_in_db(connection=connection, id= thread_id, assistant_id=request.assistant_id, user_id= request.user_id)
            if result :
                return GeneralResponse(status=ResultsStatus.success, message='Thread created successfully.', data = result)
            else:
                return GeneralResponse(status=ResultsStatus.error, message='Error while creating the thread')
        else:
            return GeneralResponse(status=ResultsStatus.error, message='Error while creating the thread')
    except Exception as e:
        log_issue(e, create_thread, f"For Args {request}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e)) 

@app.get("/retrieve-thread", response_model=GeneralResponse)
async def retrieve_thread(thread_id: str) -> dict:
    """
    Retrieves a thread details.

    Args:
        (str) thread_id: The id of thread to retrieve.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        thread_details = oai_get_thread_details(thread_id= thread_id)
        if thread_details:
            return GeneralResponse(status=ResultsStatus.success, message="Thread retrived", data=thread_details)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Error in thread retrived")
    except Exception as e:
        log_issue(e, retrieve_thread, f"For Args {thread_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.delete("/delete-thread-assistant", response_model=GeneralResponse)
async def delete_thread_assistant(thread_id: str, assistant_id: str)->dict:
    """
    Deletes a thread and an assistant.

    Args:
    - thread_id (str): The ID of the thread to be deleted.
    - assistant_id (str): The ID of the assistant to be deleted.

    Returns:
        A JSON response indicating the success or failure of the operation.
    """
    try:
        result = oai_delete_thread_and_assistant(thread_id=thread_id, assistant_id=assistant_id)
        if result:
            return GeneralResponse(status=ResultsStatus.success, message="Thread and assistant deleted successfully", data = None)
        else:
            return GeneralResponse(status=ResultsStatus.success, message="Failed to delete thread and assistant")
    except Exception as e:
        log_issue(e, delete_thread_assistant, f"For Args {thread_id} and {assistant_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))
    
@app.post("/add-message-to-thread", response_model=GeneralResponse)
async def add_message_to_thread(request: ThreadMessageRequest) -> dict:
    """
    Adds a message to a specified thread.

    Args:
        request (ThreadMessageRequest): Request object containing thread_id, message, and role.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        message_id = oai_add_message_to_thread(
            thread_id=request.thread_id, 
            message=request.message, 
            role=request.role
        )
        if message_id:
            data = oai_get_message_details(thread_id=request.thread_id, message_id= message_id)
            return GeneralResponse(status=ResultsStatus.success, message="Message added to thread successfully.", data=data)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Failed to add message to thread.")
    except Exception as e:
        log_issue(e, add_message_to_thread, f"For Args {request}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.get("/get-all-message-of-thread", response_model=GeneralResponse)
async def get_all_message_of_thread(thread_id: str) -> dict:
    """
    Gets all the messages of a given thread.

    Args:
        thread_id (str): thread id to get the content of all messages of that thread.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        messages = oai_get_all_messages_from_thread(thread_id=thread_id)
        if messages:
            return GeneralResponse(status=ResultsStatus.success, message="All message retrival successful.", data=messages)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="Failed to retrive all messages.")
    except Exception as e:
        log_issue(e, get_all_message_of_thread, f"For Args {thread_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

@app.get("/get-last-thread-id", response_model=GeneralResponse)
async def get_thread_id(assistant_id: str, connection: Any = Depends(get_connection_dependency)) -> dict:
    """
    Retrieves a list of assistants with their ID and name.

    Args:
        assistant_id (str): assistant id to get the last theead id attached to the assistant.

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        assistants = get_last_thread_id_from_db(connection=connection, assistant_id=assistant_id)
        if assistants:
            data = assistants
            return GeneralResponse(status=ResultsStatus.success, message="Thread id retrieve successfully", data=data)
        else:
            return GeneralResponse(status=ResultsStatus.error, message="No thread attached to this assistant.")
    except Exception as e:
        log_issue(e, get_thread_id, f"For Args {assistant_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))    

@app.get("/get-threads-by-date-with-first-words", response_model=GeneralResponse)
async def get_threads_by_date_with_first_words_endpoint(user_id:int,connection=Depends(get_connection_dependency)):
    """
    Get the thread and words list

    Returns:
        A JSON response indicating the success of the operation and details otherwise error.
    """
    try:
        threads_data = get_threads_by_date_with_first_words(user_id=user_id,connection=connection)
        
        if threads_data == "error":
            return GeneralResponse(status=ResultsStatus.error, message="Error retrieving threads from database", data=None)

        categorized_threads = {}
        for thread_id, first_words, time_category, assistant_id in threads_data:
            thread_info = {"thread_id": thread_id, "first_words": first_words, "assistant_id": assistant_id}
            if time_category not in categorized_threads:
                categorized_threads[time_category] = []
            categorized_threads[time_category].append(thread_info)
        
        return GeneralResponse(status=ResultsStatus.success, message="Threads with first words fetched successfully.", data=categorized_threads)
    except Exception as e:
        log_issue(e, get_threads_by_date_with_first_words_endpoint, f"For Args {user_id}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))

# ******************************************** CHAT ***********************************************

@app.post("/ask-question", response_model=GeneralResponse)
async def ask_question(request: AskQuestion, connection=Depends(get_connection_dependency)) -> dict:
    """
    Asks a question to an assistant and gets a response.

    Args:
    - assistant_id (str): The ID of the assistant to which the question is asked.
    - question (str): The question to be asked.
    - thread_id (str, optional): The thread ID if it's a continuation of a conversation. Defaults to "".

    Returns:
        A JSON response containing the assistant's answer and the thread ID.
    """
    try:
        response, thread_id = oai_ask_question_assistant(question= request.question, assistant_id= request.assistant_id, thread_id= request.thread_id)
        data= {"response": response, "thread_id": thread_id}
        if thread_id:
            result = add_thread_details_in_db(connection=connection, id= thread_id, assistant_id=request.assistant_id, user_id= request.user_id, first_words=request.question[:30])
            # if result == "exists" or result == "added":
            if result == "upserted":
                return GeneralResponse(status=ResultsStatus.success, message='Question asked successfully.', data = data)
            else:
                return GeneralResponse(status=ResultsStatus.error, message='Error while creating the thread')
        else:
            return GeneralResponse(status=ResultsStatus.error, message='Error while creating the thread')
    except Exception as e:
        log_issue(e, ask_question, f"For Args {request}")
        return GeneralResponse(status=ResultsStatus.error, message=str(e))
    
# ****************** API Welcome ******************

@app.get("/")
def read_root():
    return GeneralResponse(status=ResultsStatus.success, message="Welcome to the API!")

# ****************** Handling other errors ******************

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handles general exceptions and returns a consistent response format.
    """
    return JSONResponse(
        status_code=500,
        content=GeneralResponse(status=ResultsStatus.error, message=str(exc), data=None).dict(),
    )

# *************************************************************************************************
# *************************************************************************************************

if __name__ == "__main__":
    uvicorn.run(app, port=8030)
