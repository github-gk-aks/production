import openpyxl
import pandas as pd
import os
import re

def replace_strings(excel_path, repo_path, repository):
    # Load Excel file
    df = pd.read_excel(excel_path)

    # Fetching destination organization based on input repository.
    destination_org = df[df['Repository'] == repository]['Target Organization'].values[0]

    # List of directories to exclude
    exclude_dirs = [
        os.path.abspath(os.path.join(repo_path, 'input_migration')),
        os.path.abspath(os.path.join(repo_path, '.git')),
        os.path.abspath(os.path.join(repo_path, 'script_migration'))
    ]

    # List of file extensions to exclude
    exclude_extensions = {'.gif', '.jpeg', '.png', '.ico', '.pdf', '.jpg'}

    # List of exclude strings
    exclude_patterns = df['Exclude Strings'].dropna().tolist()
    exclude_regex = '|'.join(re.escape(pattern) for pattern in exclude_patterns)

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
        print(f"Processing file: {file_path}")  # Print the file path
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace standalone gk-aks-Digital not followed by exclude patterns
            pattern = re.compile(r'gk-aks-Digital(?!/({}))'.format(exclude_regex))
            content_new = pattern.sub(destination_org, content)

            # Replace gk-aks-Digital/whatever unless in exclude list
            if exclude_regex:
                pattern_exclude = re.compile(r'gk-aks-Digital/(?!({})).*?'.format(exclude_regex))
                content_new = pattern_exclude.sub(lambda x: x.group(0).replace('gk-aks-Digital', destination_org), content_new)
            else:
                # If no exclude patterns, just replace all occurrences
                content_new = content_new.replace('gk-aks-Digital', destination_org)

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
