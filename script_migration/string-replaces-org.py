import openpyxl
import pandas as pd
import os
import re

def replace_strings(excel_path, repo_path, repository):
    # Load Excel file
    df = pd.read_excel(excel_path)

    # Fetching destination organization based on input repository.
    destination_org = df[df['Repository'] == repository]['Target Organization'].values[0]

    # Fetching all exclude strings
    exclude_strings = df['Exclude Strings'].values
    print(f"Exclude Strings: {exclude_strings}")
    
    # exclude_patterns = []
    # for exclude_string in exclude_strings:
    #     exclude_patterns.extend(exclude_string.split('|'))

    # Escape exclude strings for regex
    exclude_patterns = [re.escape(pattern) for pattern in exclude_strings]
    print(f"Exclude Patterns: {exclude_patterns}")
    
    # List of directories to exclude
    exclude_dirs = [
        os.path.abspath(os.path.join(repo_path, 'input_migration')),
        os.path.abspath(os.path.join(repo_path, '.git')),
        os.path.abspath(os.path.join(repo_path, 'script_migration'))
    ]

    # List of file extensions to exclude
    exclude_extensions = {'.gif', '.jpeg', '.png', '.ico', '.pdf', '.jpg'}

    # Get list of all files in repository (excluding specified directories)
    all_files = []
    for dp, dn, filenames in os.walk(repo_path):
        abs_dp = os.path.abspath(dp)
        if not any(abs_dp == exclude_dir or abs_dp.startswith(exclude_dir + os.sep) for exclude_dir in exclude_dirs):
            for f in filenames:
                if not any(f.endswith(ext) for ext in exclude_extensions):
                    all_files.append(os.path.join(dp, f))

    print(f"All files: {all_files}")
    
    # Iterate through all files
    for file_path in all_files:
        print(f"Processing file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace strings in file content
            def replace_func(match):
                matched_string = match.group(0)
                if any(re.search(re.escape(pattern), matched_string) for pattern in exclude_patterns):
                    return matched_string  # Return the original if it matches any exclude pattern
                else:
                    return matched_string.replace('gk-aks-Digital', destination_org)

            content_new = re.sub(r'gk-aks-Digital\S*', replace_func, content)

            # Write back to the file if changes were made
            if content != content_new:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content_new)
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")

if __name__ == "__main__":
    excel_file = os.getenv('EXCEL_FILE')
    repo_path = os.getenv('GITHUB_WORKSPACE')
    repository = os.getenv('REPOSITORY')

    replace_strings(excel_file, repo_path, repository)
