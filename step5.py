import os
import csv

# Target folder path
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\April\Rename\Consent\Extract\step4"

# Loop through all .csv files
for filename in os.listdir(folder_path):
    if filename.endswith('.csv') and not filename.startswith('~$'):
        file_path = os.path.join(folder_path, filename)

        try:
            # Count rows where column E (index 4) < 300
            count_lt_300 = 0
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)  # Skip header
                for row in reader:
                    if len(row) > 4:
                        try:
                            if float(row[4]) < 300:
                                count_lt_300 += 1
                        except ValueError:
                            continue  # skip if not numeric

            # Construct new filename
            base_name, ext = os.path.splitext(filename)
            new_filename = f"{base_name}_LT300N{count_lt_300}{ext}"
            new_file_path = os.path.join(folder_path, new_filename)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"[✓] Renamed: {filename} → {new_filename}")

        except Exception as e:
            print(f"[✗] Error processing {filename}: {e}")
