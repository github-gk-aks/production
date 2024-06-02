import sys
import pandas as pd

repository_name = sys.argv[1]  # Repository name passed as a command line argument

# Read Excel file
excel_data = pd.read_excel('data/Repository-List.xlsx', header=None)
repository_names = excel_data.iloc[:, 0].tolist()

# Check if the current repository name is in the list
allow_access = repository_name in repository_names

# Output 'true' or 'false' to be used in the subsequent step
print(f"::set-output name=allowAccess::{str(allow_access).lower()}")
