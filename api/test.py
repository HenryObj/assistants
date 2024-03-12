# ************************************************************************************************
# ****************************************** IMPORTS *********************************************

from ast_base import *
import requests

# ****** PATHS & GLOBAL VARIABLES *******

BASE_URL = "CHANGE_TO_THE_URL_OF_YOUR_API"  # Update if we change the address of the API

# *************************************************************************************************
# ****************************************** FUNCTIONS *********************************************
# *************************************************************************************************

def create_client(client_data):
    response = requests.post(f"{BASE_URL}/clients", json=client_data)
    return response.json()

def list_clients():
    response = requests.get(f"{BASE_URL}/get-client-list")
    return response.json()

def client_data(client_id):
    response = requests.get(f"{BASE_URL}/get-client-data", params={"client_id": client_id})
    return response.json()

def delete_client(client_id):
    response = requests.delete(f"{BASE_URL}/clients", json={"client_id": client_id})
    return response.json()

def update_client(client_data):
    response = requests.put(f"{BASE_URL}/clients", json=client_data)
    return response.json()

def create_user(user_data):
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    return response.json()

def list_users():
    response = requests.get(f"{BASE_URL}/get-user-list")
    return response.json()

def user_data(user_id):
    response = requests.get(f"{BASE_URL}/get-user-data", params={"user_id": user_id})
    return response.json()

def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users", json={"user_id": user_id})
    return response.json()

def update_user(user_data):
    response = requests.put(f"{BASE_URL}/users", json=user_data)
    return response.json()

# *************************************************************************************************
# *************************************************************************************************

if __name__ == "__main__":
    # print("Listing clients:")
    # print(list_clients())
    # print("\n")
    # y = input("Choose the ID of client you want the data for - press 'X' if you want to skip:")

    # if y.isdigit():  # Check if the input is all digits (a number)
    #     client_id = int(y)  # Convert the string to an integer
    #     print(client_data(client_id))
    # else:
    #     print("Skipping fetching data.")
    # x = input("Choose the ID of client you want to delete - press 'X' if you want to skip:")
    # if isinstance(x, int):
    #     print(delete_client(x))
    # else:
    # #     print("Skipping deletion")
    # x = input("Choose the ID of client you want to delete - press 'X' if you want to skip:")

    # if x.isdigit():  # Check if the input is all digits (a number)
    #     client_id = int(x)  # Convert the string to an integer
    #     print(delete_client(client_id))
    # else:
    #     print("Skipping deletion")

    w = input("Choose the ID of client you want to delete - press 'X' if you want to skip:")
    if w.isdigit():  # Check if the input is all digits (a number)
        client_id = int(w)  # Convert the string to an integer
        print(delete_client(client_id))
    else:
        print("Skipping deletion")


    x= input("Choose the ID of client you want data for - press 'X' if you want to skip:")
    if x.isdigit():  # Check if the input is all digits (a number)
        client_id = int(x)  # Convert the string to an integer
        print(client_data(client_id))
    else:
        print("Skipping deletion")


    # print("Listing users:")
    # print(list_users())



    y = input("Choose the ID of user you want the data for - press 'X' if you want to skip:")

    if y.isdigit():  # Check if the input is all digits (a number)
        user_id = int(y)  # Convert the string to an integer
        print(user_data(user_id))
    else:
        print("Skipping fetching data.")

    
    z = input("Choose the ID of user you want the delete - press 'X' if you want to skip:")

    if y.isdigit():  # Check if the input is all digits (a number)
        user_id = int(y)  # Convert the string to an integer
        print(delete_user(user_id))
    else:
        print("Skipping fetching data.")
    


    # client_data = {
    #     "client_name": "New Client2222",
    #     "client_company": "New Company2222",
    #     "client_domain": "newdomain2222.com",
    #     "client_email": "contact2222@newdomain.com",
    #     "client_pss": "12345",
    #     "client_logo": ""

    # }
    # print("\nCreating a client:")
    # print(create_client(client_data))

    # user_data = {
    #     "client_id": 3,
    #     "username": "newuser325",
    #     "first_name": "New234",
    #     "last_name": "User2332",
    #     "user_email": "newuser2@domain.com",
    #     "user_pss": "userpassword2",
    #     "lang": "eng4",
    #     "ip": "192.168.21.1"
    # }
    # print("\nCreating a user:")
    # print(create_user(user_data))
        



    client_data = {
        "client_id": 7,
        "client_name": "Cena John 66",
        "client_company": "New Cena",
        "client_domain": "newcena.com",
        "client_email": "cena@newdomain.com",
        "client_pss": "12345",
        "client_logo": ""
    }

    print("\nUpdating a client:")
    print(update_client(client_data))

    # print("\nUpdating a client:")
    # response = update_client(client_data)

    # Check if the update was successful
    # print("\nUpdating a client:")
    # response = update_client(client_data)
    # print(response)  # Print the response for debugging

    # if response['status'] == 'success':
    #     print("Client information updated successfully.")
    # else:
    #     print("Failed to update client information.")
        


    user_data = {
        "user_id": 4,
        "client_id": 3,
        "username": "hello",
        "first_name": "New234",
        "last_name": "User2332",
        "user_email": "newuser2@domain.com",
        "user_pss": "userpassword2",
        "lang": "eng4",
        "ip": "192.168.21.1"
    }
    print("\nUpdating a user:")
    print(update_user(user_data))
