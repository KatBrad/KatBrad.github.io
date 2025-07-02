import os
import re
import csv

# Set your folder path
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\April\Rename"

# Loop through all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        try:
            # Open CSV and read first row
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                first_row = next(reader)

                # Get the 13th element (M1)
                if len(first_row) >= 13:
                    new_name_raw = first_row[12]
                else:
                    print(f"[Skipped] '{filename}': Less than 13 columns in row 1.")
                    continue

            if new_name_raw is None or str(new_name_raw).strip() == "":
                print(f"[Skipped] '{filename}': M1 is empty")
                continue

            # Sanitize new filename
            safe_name = re.sub(r'[\\/:"*?<>|]+', "", str(new_name_raw).strip())
            new_file_path = os.path.join(folder_path, f"{safe_name}.csv")

            # Check for name conflict
            if os.path.exists(new_file_path):
                print(f"[Skipped] '{filename}': '{safe_name}.csv' already exists")
                continue

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"[Renamed] {filename} → {safe_name}.csv")

        except Exception as e:
            print(f"[Error] '{filename}': {e}")
