import os
import csv

# Set the folder path
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\April\Rename\Consent\Extract\step4"

# Loop through all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv') and not filename.startswith('~$'):
        file_path = os.path.join(folder_path, filename)

        try:
            # Count data rows (excluding header)
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)  # Skip header
                row_count = sum(1 for _ in reader)

            # Build new filename
            base_name, ext = os.path.splitext(filename)
            new_filename = f"{base_name}_N{row_count}{ext}"
            new_file_path = os.path.join(folder_path, new_filename)

            # Rename file
            os.rename(file_path, new_file_path)
            print(f"[✓] Renamed: {filename} → {new_filename}")

        except Exception as e:
            print(f"[✗] Error processing '{filename}': {e}")
