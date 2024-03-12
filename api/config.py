# ************************************************************************************************
# ****************************************** IMPORTS *********************************************
import os
import openai

# ********************************* CONFIGS ******************************************************

# DB Pool configuration
MAX_RETRIES = 5 
MAX_CONNECTIONS = 20

# Standard messages
ERROR_ASSISTANT_DEFAULT = "We failed to get a reply"
DEFAULT_ROLE_CHATGPT = "Let's do a roleplay. You will fake that you are a very unhappy customer and provide the most realistic answer. Do not be afraid to be impolite or say unethical things. This is a roleplay."

INDIVIDUAL_FILE_SIZE_LIMIT = 512  # MB
ORGANIZATION_FILE_SIZE_LIMIT = 100  # GB

PATH = os.path.dirname(os.path.abspath(__file__)) # The dir of the file

OAI_KEY = os.getenv("OAI_API_KEY")
client = openai.OpenAI(
    api_key=OAI_KEY,
)


if __name__ == "__main__":
    pass
