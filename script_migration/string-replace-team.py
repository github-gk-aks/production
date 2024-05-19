import openpyxl
import pandas as pd
import os

def replace_strings(source_excel_path, target_excel_path, repo_path):
    # Load source Excel file
    source_df = pd.read_excel(source_excel_path, usecols=['Source GitHub Team Name'])
    source_team_names = source_df['Source GitHub Team Name'].tolist()

    # Load target Excel file
    target_df = pd.read_excel(target_excel_path, usecols=['Full Repository Name', 'Repository Name', 'Full Team Name Digital', 'Full Team Name EMU'])

    # List of directories to exclude
    #exclude_dirs = [os.path.join(repo_path, 'input_migration'), os.path.join(repo_path, '.git'), os.path.join(repo_path, 'script_migration')]

    # List of directories to exclude
    exclude_dirs = [
        os.path.abspath(os.path.join(repo_path, 'input_migration')),
        os.path.abspath(os.path.join(repo_path, '.git')),
        os.path.abspath(os.path.join(repo_path, 'script_migration'))
    ]

    # List of file extensions to exclude
    exclude_extensions = {'.gif', '.jpeg', '.png', '.ico'}

    # Get list of all files in repository (excluding specified directories)
    #all_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(repo_path) for f in filenames if not any(os.path.abspath(dp).startswith(os.path.abspath(exclude_dir)) for exclude_dir in exclude_dirs)]

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
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Iterate through source team names
            for source_team_name in source_team_names:
                # Find matching rows in the target DataFrame
                matches = target_df[(target_df['Repository Name'] == os.getenv('REPOSITORY')) & (target_df['Full Team Name Digital'] == source_team_name)]
                
                if not matches.empty:
                    target_team_name = matches.iloc[0]['Full Team Name EMU']
                    
                    # Replace strings in file content
                    content = content.replace(source_team_name, target_team_name)

            # Write back to the file if changes were made
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")

if __name__ == "__main__":
    excel_file_source = os.getenv('EXCEL_FILE_SOURCE')
    excel_file_target = os.getenv('EXCEL_FILE_TARGET')
    github_workspace = os.getenv('GITHUB_WORKSPACE')

    replace_strings(excel_file_source, excel_file_target, github_workspace)
