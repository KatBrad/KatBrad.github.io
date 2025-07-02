import os
import pandas as pd
import numpy as np

# Folder containing your CSV files
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\April\Rename\Consent\Extract\step4"

# Process each CSV file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv') and not filename.startswith('~$'):
        file_path = os.path.join(folder_path, filename)
        print(f"🔄 Processing {filename}")

        # Load CSV
        df = pd.read_csv(file_path)

        # Ensure columns E, J, K are numeric (indices 4, 9, 10)
        df.iloc[:, 4] = pd.to_numeric(df.iloc[:, 4], errors='coerce')  # Column E
        df.iloc[:, 9] = pd.to_numeric(df.iloc[:, 9], errors='coerce')  # Column J
        df.iloc[:, 10] = pd.to_numeric(df.iloc[:, 10], errors='coerce')  # Column K

        # Calculate means for J == 0 and K in [3,4,6,7]
        means = {}
        for block, label in zip([3, 4, 6, 7], ['MnA1', 'MnA2', 'MnB1', 'MnB2']):
            block_data = df[(df.iloc[:, 9] == 0) & (df.iloc[:, 10] == block)].iloc[:, 4].dropna()
            means[block] = block_data.mean()
            print(f"Mean for block {block} ({label}): {means[block]}")

        # Replace values in E where J == 1 and K is 3, 4, 6, 7
        for block in [3, 4, 6, 7]:
            replacement_value = means[block] + 600 if not np.isnan(means[block]) else np.nan
            mask = (df.iloc[:, 9] == 1) & (df.iloc[:, 10] == block)
            df.loc[mask, df.columns[4]] = replacement_value

        # Save the modified DataFrame
        new_filename = filename.replace('.csv', '_recoded.csv')
        new_path = os.path.join(folder_path, new_filename)
        df.to_csv(new_path, index=False)
        print(f"✅ Saved: {new_filename}")
