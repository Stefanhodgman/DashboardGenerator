import requests
import xml.etree.ElementTree as ET

def list_commands(workspace_uri):
    url = f"https://{workspace_uri}/api/ws/commandlist"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    commands = root.findall(".//Command")
    command_list = []
    for command in commands:
        command_name = command.find("Name").text
        command_list.append(command_name)
    return command_list
