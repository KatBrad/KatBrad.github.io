import os
import csv

# Set your folder path
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\April\Rename\Consent"

# Define the target values for column K (index 10)
keep_values = {'3', '4', '6', '7'}

# Process each CSV file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        input_file = os.path.join(folder_path, filename)
        base_name = os.path.splitext(filename)[0]
        output_file = os.path.join(folder_path, f"{base_name}_extract.csv")

        try:
            with open(input_file, newline='', encoding='utf-8') as infile, \
                 open(output_file, 'w', newline='', encoding='utf-8') as outfile:

                reader = csv.reader(infile)
                writer = csv.writer(outfile)

                # Optional: write header
                header = next(reader)
                writer.writerow(header)

                for row in reader:
                    if len(row) > 10 and row[10].strip() in keep_values:
                        writer.writerow(row)

            print(f"[✓] Saved: {output_file}")
        
        except Exception as e:
            print(f"[✗] Error processing '{filename}': {e}")
