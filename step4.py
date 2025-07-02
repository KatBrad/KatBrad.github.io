import os
import csv

# Set your target folder path
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\April\Rename\Consent\Extract"

# Loop through all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        input_file = os.path.join(folder_path, filename)
        base_name = os.path.splitext(filename)[0]
        output_file = os.path.join(folder_path, f"{base_name}_step4.csv")

        try:
            with open(input_file, newline='', encoding='utf-8') as infile, \
                 open(output_file, 'w', newline='', encoding='utf-8') as outfile:

                reader = csv.reader(infile)
                writer = csv.writer(outfile)

                # Write header
                header = next(reader)
                writer.writerow(header)

                # Filter rows where column E (index 4) < 10001
                for row in reader:
                    if len(row) > 4:
                        try:
                            if float(row[4]) < 10001:
                                writer.writerow(row)
                        except ValueError:
                            continue  # Skip rows where E is not a number

            print(f"[✓] Processed: {filename} → {base_name}_step4.csv")

        except Exception as e:
            print(f"[✗] Error processing '{filename}': {e}")
