import os
import pandas as pd
import numpy as np

# Folder containing your CSV files
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\April\Rename\Consent\Extract\step4"

# Block config: {K value: (Label1, Label2)}
blocks = {
    3: ('MnA1', 'SDA1'),
    4: ('MnA2', 'SDA2'),
    6: ('MnB1', 'SDB1'),
    7: ('MnB2', 'SDB2'),
}

# Loop through each CSV file
for filename in os.listdir(folder_path):
    if filename.endswith(".csv") and not filename.startswith('~$'):
        file_path = os.path.join(folder_path, filename)

        print(f"🔄 Processing: {filename}")

        # Load CSV into DataFrame
        df = pd.read_csv(file_path)

        # Ensure relevant columns are numeric
        df.iloc[:, 4] = pd.to_numeric(df.iloc[:, 4], errors='coerce')  # Column E
        df.iloc[:, 9] = pd.to_numeric(df.iloc[:, 9], errors='coerce')  # Column J
        df.iloc[:, 10] = pd.to_numeric(df.iloc[:, 10], errors='coerce')  # Column K

        # Filter where column J == 0
        df_filtered = df[df.iloc[:, 9] == 0]

        # Create list to store new rows
        summary_rows = []

        for block_val, (mean_label, sd_label) in blocks.items():
            block_data = df_filtered[df_filtered.iloc[:, 10] == block_val].iloc[:, 4].dropna()

            if not block_data.empty:
                mean_val = block_data.mean()
                std_val = block_data.std()
            else:
                mean_val = std_val = np.nan

            # Add new summary row
            summary_rows.append([mean_label, mean_val, sd_label, std_val])

        # Convert to DataFrame and append to original
        summary_df = pd.DataFrame(summary_rows, columns=df.columns[:4])  # Use first 4 cols
        df_combined = pd.concat([df, summary_df], ignore_index=True)

        # Save over the original CSV
        df_combined.to_csv(file_path, index=False)
        print(f"✅ Stats appended to: {filename}")
