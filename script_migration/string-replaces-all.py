import openpyxl
import sys
import os
import glob

def replace_strings(excel_path, repo_path):
    # Load Excel file
    wb = openpyxl.load_workbook(filename=excel_path, read_only=True)
    sheet = wb.active

    # List of directories to exclude
    exclude_dirs = [os.path.join(repo_path, 'input_migration'), os.path.join(repo_path, '.git/'), os.path.join(repo_path, 'script_migration')]

    # Get list of all files in repository (excluding .git directory)
    all_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(repo_path) for f in filenames if not any(os.path.abspath(dp).startswith(os.path.abspath(exclude_dir)) for exclude_dir in exclude_dirs)]

    print(f"All files: {all_files}")

    # Iterate through all files
    for file_path in all_files:
        print(f"Processing file: {file_path}")  # Print the file pat
        # Iterate through all files
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Iterate through Excel rows
            for row in sheet.iter_rows(min_row=2, values_only=True):
                original_string = row[0]
                replacement_string = row[1]

                # Replace strings in file content
                content = content.replace(original_string, replacement_string)

            # Write back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")

if __name__ == "__main__":
    excel_file = os.getenv('EXCEL_FILE')
    github_workspace = os.getenv('GITHUB_WORKSPACE')

    replace_strings(excel_file, github_workspace)