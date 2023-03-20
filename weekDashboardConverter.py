import sys
import csv
import json
import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def weekDashboardConverter():
    def select_excel_file():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
        return file_path

    def excel_to_csv(excel_file):
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file, dtype=str)

        # Convert the date columns in the header to the desired date format
        new_columns = []
        for col in df.columns:
            try:
                new_col = pd.to_datetime(col).strftime('%d-%b-%y')
                new_columns.append(new_col)
            except ValueError:
                new_columns.append(col)
        df.columns = new_columns

        # Convert the date columns in the DataFrame to the desired date format
        date_columns = ['Week_Start_Date']
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%b-%y')

        # Fill the empty cells with '-'
        #df = df.fillna('-')

        # Create the CSV file name by appending '_Converted.csv' to the original file name
        csv_file = os.path.join(os.getcwd(), 'Week Dashboard_Converted.csv')

        # Write the DataFrame to a comma-delimited CSV file with UTF-8 encoding
        df.to_csv(csv_file, index=False, sep=';', encoding='utf-8')

        # Return the specified CSV file name
        return csv_file

    def csv_to_json(csv_file, json_file):
        def process_value(value):
            if value.lstrip('-').isdigit():
                return int(value)
            return value

        # Read hashProjectId from workspace_id.txt
        with open("workspace_id.txt", "r") as workspace_id_file:
            hash_project_id = workspace_id_file.read().strip()

        # Read hashInstanceGroupId from WBHO-WDB_Template.json
        with open("WBHO-WDB_Template.json", "r") as instance_group_file:
            instance_group_data = json.load(instance_group_file)
            hash_instance_group_id = instance_group_data["instanceGroupID"]

        with open(csv_file, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            csv_content = [row for row in reader if row]

            site = csv_content[1][0]
            form_title = csv_content[1][1]
            week_start_date = csv_content[1][2].replace('-', ' ')

            data = []
            for row in csv_content[1:]:
                current_row = row
                status_data = {f"StatusDD_{i}": process_value(value) for i, value in enumerate(current_row[12:52:2], start=1)}
                zone_data = {f"ZoneDD_{i}": process_value(value) for i, value in enumerate(current_row[13:54:2], start=1)}

                row_data = {
                    **status_data,
                    **zone_data,
                    "Level": current_row[3],
                    "Element": current_row[4],
                    "Subcontractor": current_row[5],
                    "Resource": current_row[6],
                    "Action": current_row[7],
                    "Who": current_row[8],
                    "Obstacle": current_row[9],
                    "Days" : current_row[10],
                }
                data.append(row_data)

        dates = {f"Datepicker_{i+1}": process_value(value) for i, value in enumerate(csv_content[0][11:60:2])}

        output = {
            "fieldJson": {
                "myFields": {
                    "Site": site,
                    "ORI_FORMTITLE": form_title,
                    "DS_CLOSE_DUE_DATE": "2030-03-01",
                    "Week_Start_Date": week_start_date,
                    **dates,
                    "Repeating_Table_Parent1": {
                        "table_header": [{}],
                        "table_footer": [{}],
                        "value": data,
                    }
                },
            },
            "hashProjectId": hash_project_id,
            "hashInstanceGroupId": hash_instance_group_id,
        }

        with open(json_file, "w") as outfile:
            json.dump(output, outfile, indent=4)


    def main():
            excel_file_path = select_excel_file()
            if not excel_file_path:
                print('No file selected.')
                return
            csv_file_path = excel_to_csv(excel_file_path)
            json_file_path = os.path.join(os.getcwd(), "output.json")  # Replace this line
            csv_to_json(csv_file_path, json_file_path)

    main()

if __name__ == "__main__":
    # Remove or comment out the following line:
    # weekDashboardConverter()
    pass