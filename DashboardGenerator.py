import sys
import requests
import xml.etree.ElementTree as ET
import subprocess
import os
import json
from createFormMsg4 import createFormMsg
from formtypelist import get_formtypelist, get_FormTemplate
from weekDashboardConverter import weekDashboardConverter
from userLogon import login_dialog
from userConfirmation import user_confirmation

url = "https://dms.asite.com/apilogin/"
email, password = login_dialog()

if not email or not password:
    print("Login canceled")
    sys.exit()

# create a dictionary of data to be sent in the POST request
data = {
    "emailId": email,
    "password": password
}

# make a POST request to the API and store the response
response = requests.post(url, data=data)

app_builder_id = None
selected_uri = None

# parse the XML response and get the Sessionid
root = ET.fromstring(response.content)
session_id = root.find(".//Sessionid").text

# save the session_id to a file
with open("ASessionID.txt", "w") as f:
    f.write(session_id)

# use curl to get the list of workspaces and save it to a file
curl_cmd = f'curl --insecure --cookie ASessionID="{session_id}" https://dmsak.asite.com/api/workspace/workspacelist > WorkspaceList.xml'
subprocess.run(curl_cmd, shell=True)
print("Workspace list saved to WorkspaceList.xml")

# parse the WorkspaceList.xml file and create a numbered list of workspaces
tree = ET.parse("WorkspaceList.xml")
root = tree.getroot()
workspaces = root.findall(".//workspaceVO")
for i, workspace in enumerate(workspaces):
    print(f"{i+1}. {workspace.find('Workspace_Name').text}")

selected_workspace = None
for workspace in workspaces:
    workspace_name = workspace.find('Workspace_Name').text
    if "Development" in workspace_name:
        selected_workspace = workspace
        break

if selected_workspace is None:
    print("No workspace with the word 'Development' found.")
    workspace_num = int(input("Select a workspace by number: "))
    selected_workspace = workspaces[workspace_num-1]

workspace_id = selected_workspace.find("Workspace_Id").text
workspace_uris = selected_workspace.findall("URI")

# # create a numbered list of workspace URIs
# uri_list = []
# for i, uri in enumerate(workspace_uris):
#     uri_str = uri.text
#     uri_name = uri_str.split("/")[-1]
#     if uri_name in ["formtypelist", "getWorkspaceUsers", "createFormMsg", "getProjectCustomAttributeSet", "getProjectCustomAttributes", "saveCustomAttributeSet", "saveCustomAttributes", "getWorkspaceroles"]:
#         uri_list.append(uri_str)
#         print(f"{len(uri_list)}. {uri_name}")

# # ask the user to select a URI by number
# uri_num = int(input("Select a URI by number: "))
# selected_uri = uri_list[uri_num-1]

selected_uri = None
for uri in workspace_uris:
    uri_str = uri.text
    uri_name = uri_str.split("/")[-1]
    if uri_name == "formtypelist":
        selected_uri = uri_str
        break

if selected_uri is None:
    print("No 'formtypelist' URI found in the workspace URIs.")
    # create a numbered list of workspace URIs
    uri_list = []
    for i, uri in enumerate(workspace_uris):
        uri_str = uri.text
        uri_name = uri_str.split("/")[-1]
        if uri_name in ["formtypelist", "getWorkspaceUsers", "createFormMsg", "getProjectCustomAttributeSet", "getProjectCustomAttributes", "saveCustomAttributeSet", "saveCustomAttributes", "getWorkspaceroles"]:
            uri_list.append(uri_str)
            print(f"{len(uri_list)}. {uri_name}")
    
    # ask the user to select a URI by number
    uri_num = int(input("Select a URI by number: "))
    selected_uri = uri_list[uri_num-1]


# save the selected_uri to a file
with open("SelectedURI.XML", "w") as f:
    f.write(selected_uri)

# (The rest of the main.py file remains the same)

# save the curl_cmd to a file
with open("curl_cmd.XML", "w") as f:
    f.write(curl_cmd)

if selected_uri.endswith("formtypelist"):
    # Call get_formtypelist to obtain the app_builder_id for the selected form type
    app_builder_id = get_formtypelist(session_id, workspace_id, selected_uri)

    # Use the app_builder_id to download the form template
    get_FormTemplate(session_id, workspace_id, app_builder_id)

# Check for user confirmation before calling createFormMsg
if __name__ == "__main__":
    weekDashboardConverter()  # This should be called before user_confirmation()

    if user_confirmation():
        createFormMsg()
    else:
        print("Operation cancelled by user.")

