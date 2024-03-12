# ************************************************************************************************
# ****************************************** IMPORTS *********************************************

from utilities import *

from pydantic import BaseModel
from enum import Enum
from ast_db_base import get_db_connection

# ************************************************************************************************
# ****************************************** CLASSES *********************************************
# ************************************************************************************************

# Client
class Client(BaseModel):
    client_name: str
    client_company: Optional[str] = None
    client_domain: Optional[str] = None
    client_email: Optional[str] = None  
    client_pss: Optional[str] = None
    client_logo: Optional[str] = None

class UpdateClientInput(BaseModel):
    client_id: int
    client_name: Optional[str] = None
    client_company: Optional[str] = None
    client_domain: Optional[str] = None
    client_email: Optional[str] = None  
    client_pss: Optional[str] = None
    client_logo: Optional[str] = None

class ClientInput(BaseModel):
    client_id: int

# Users
class User(BaseModel):
    client_id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_email: Optional[str] = None  
    user_pss: Optional[str] = None
    lang: Optional[str] = None
    ip: Optional[str] = None

class UpdateUserInput(BaseModel):
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_email: Optional[str] = None  
    user_pss: Optional[str] = None
    lang: Optional[str] = None
    ip: Optional[str] = None
    
class UserInput(BaseModel):
    user_id: int

class AskQuestion(BaseModel):
    user_id: str
    assistant_id:str
    thread_id: Optional[str] = ""
    question: str

class Assistant(BaseModel):
    user_id: int
    assistant_name: str
    instructions: str
    gpt_model: str

class ThreadRequest(BaseModel):
    assistant_id: str
    user_id: int

class ThreadMessageRequest(BaseModel):
    thread_id: str
    message: str
    role: str = "user"

class RunRequest(BaseModel):
    thread_id: str
    assistant_id: str

class GetAllMessage(BaseModel):
    thread_id: str

class UploadFiles(BaseModel):
    files: list[str]
    client_id: int

class AssistantFilesModificationRequest(BaseModel):
    assistant_id: str
    attach_file_ids: Optional[list[str]]
    detach_file_ids: Optional[list[str]]

# ALL RESPONSES follow the below structure
class ResultsStatus(str, Enum):
    conflict = 'conflict'
    error = 'error'
    record_not_found = 'record not found'
    success = 'success'
    unauthorized = 'unauthorized'

class GeneralResponse(BaseModel):
    status: ResultsStatus
    message: str
    data: Optional[Any] = None

class AttachFilesRequest(BaseModel):         
    assistant_id: str
    file_ids: list[str]

class EditAssistantRequest(BaseModel):
    assistant_id: str
    name: str
    model: str
    instructions: str

# *************************************************************************************************
# ****************************************** FUNCTIONS *********************************************
# *************************************************************************************************

# To get the connection in the route without opening and closing it
def get_connection_dependency():
    with get_db_connection() as connection:
        yield connection


# *************************************************************************************************
# *************************************************************************************************

if __name__ == "__main__":
    pass
