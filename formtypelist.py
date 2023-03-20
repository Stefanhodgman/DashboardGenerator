import json
import xml.etree.ElementTree as ET
import subprocess

def get_formtypelist(session_id, workspace_id, selected_uri):
    # follow the selected URI using CURL and save the response to a file
    curl_cmd = f'curl --insecure --cookie ASessionID="{session_id}" "{selected_uri}" > "FormTypeList.xml"'
    subprocess.run(curl_cmd, shell=True)
    print("Response saved to FormTypeList.xml")

    # parse the FormTypeList.xml file and create a numbered list of form types
    tree = ET.parse("FormTypeList.xml")
    root = tree.getroot()
    form_types = root.findall(".//FormType")
    for i, form_type in enumerate(form_types):
        print(f"{i+1}. {form_type.find('FormName').text}")

    # Try to find the "Week Dashboard" form type and automatically select it
    app_builder_id = None
    for form_type in form_types:
        form_name = form_type.find('FormName').text
        if form_name == "Week Dashboard":
            app_builder_id = form_type.find("AppBuilderID").text
            break

    # If "Week Dashboard" is not found, ask the user to select a form type by number
    if app_builder_id is None:
        print("No 'Week Dashboard' form type found.")
        form_type_num = int(input("Select a form type by number: "))
        form_type = form_types[form_type_num-1]
        app_builder_id = form_type.find("AppBuilderID").text

    return app_builder_id


def get_FormTemplate(session_id, workspace_id, app_builder_id):
    form_template_url = "https://adoddleak.asite.com/commonapi/form/getFormTemplate"
    curl_cmd = f'curl --insecure --cookie ASessionID="{session_id}" --data "projectId={workspace_id}&appBuilderCode={app_builder_id}" {form_template_url} > {app_builder_id}_Template.json'
    subprocess.run(curl_cmd, shell=True)
    print(f"Form template saved to {app_builder_id}_Template.xml")

    # save the app_builder_id to a file
    with open("app_builder_id.txt", "w") as f:
        f.write(app_builder_id)

    # save the workspace_id to a file
    with open("workspace_id.txt", "w") as f:
        f.write(workspace_id)

