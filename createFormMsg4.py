import pandas as pd
import json
import openpyxl
import requests
from userConfirmation import user_confirmation

def get_value_from_text_file(file_name):
    with open(file_name, "r") as file:
        return file.read().strip()

def createFormMsg():

    # Read session_id from ASessionID.txt
    session_id = get_value_from_text_file("ASessionID.txt")

    # Read form_data from output.json
    with open("output.json", "r") as file:
        form_data = json.load(file)

    url = "https://adoddleak.asite.com/commonapi/form/createFormMsg"
    headers = {
        "ASessionID": session_id
    }
    files = {
        "formMetaData": (None, json.dumps(form_data), "application/json"),
    }

    # Print request details to the console
    print("Request URL:", url)
    print("Request headers:", headers)
    print("Request payload:", json.dumps(form_data, indent=2))

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        print("Form message created successfully")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    createFormMsg()
