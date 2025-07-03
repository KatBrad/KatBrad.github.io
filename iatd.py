import os
import pandas as pd
import numpy as np

# === Folder containing the CSV files ===
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\April\Rename\Consent\Extract\step4\Recoded"

# === List to store summary IAT-D results ===
summary_data = []

# === Process each file ===
for file in os.listdir(folder_path):
    if file.endswith('.csv') and not file.endswith('_with_IAT_stats.csv'):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)

        # Ensure necessary columns are numeric
        df.iloc[:, 4] = pd.to_numeric(df.iloc[:, 4], errors='coerce')  # Column E
        df.iloc[:, 10] = pd.to_numeric(df.iloc[:, 10], errors='coerce')  # Column K

        results = {}

        # Define block keys (K values) and labels
        block_defs = {
            3: ('MnA1', 'SDA1', 'NA1'),
            4: ('MnA2', 'SDA2', 'NA2'),
            6: ('MnB1', 'SDB1', 'NB1'),
            7: ('MnB2', 'SDB2', 'NB2'),
        }

        # Calculate mean, SD, and count for each block (using only column K)
        for k_val, (mn, sd, n) in block_defs.items():
            block_data = df[df.iloc[:, 10] == k_val].iloc[:, 4].dropna()
            results[mn] = block_data.mean()
            results[sd] = block_data.std()
            results[n] = block_data.count()

        # Calculate differences
        results['B1 - A1'] = results['MnB1'] - results['MnA1']
        results['B2 - A2'] = results['MnB2'] - results['MnA2']

        # Inclusive SD1
        try:
            sd1 = np.sqrt(((results['NA1'] - 1)*results['SDA1']**2 + (results['NB1'] - 1)*results['SDB1']**2 +
                          ((results['NA1'] + results['NB1'])*(results['MnA1'] - results['MnB1'])**2)/4) /
                          (results['NA1'] + results['NB1'] - 1))
        except:
            sd1 = np.nan
        results['Inclusive SD1'] = sd1

        # Inclusive SD2
        try:
            sd2 = np.sqrt(((results['NA2'] - 1)*results['SDA2']**2 + (results['NB2'] - 1)*results['SDB2']**2 +
                          ((results['NA2'] + results['NB2'])*(results['MnA2'] - results['MnB2'])**2)/4) /
                          (results['NA2'] + results['NB2'] - 1))
        except:
            sd2 = np.nan
        results['Inclusive SD2'] = sd2

        # IAT Scores
        results['IAT1'] = results['B1 - A1'] / results['Inclusive SD1'] if results['Inclusive SD1'] else np.nan
        results['IAT2'] = results['B2 - A2'] / results['Inclusive SD2'] if results['Inclusive SD2'] else np.nan
        results['IAT-D'] = np.nanmean([results['IAT1'], results['IAT2']])

        # Store for summary
        summary_data.append({
            "File_ID": file[:12],
            "IAT-D": results['IAT-D']
        })

        # Append results to file
        append_rows = []
        for k_val, (mn, sd, n) in block_defs.items():
            append_rows.append([mn, results[mn]])
            append_rows.append([sd, results[sd]])
            append_rows.append([n, results[n]])

        append_rows += [
            ['B1 - A1', results['B1 - A1']],
            ['B2 - A2', results['B2 - A2']],
            ['Inclusive SD1', results['Inclusive SD1']],
            ['Inclusive SD2', results['Inclusive SD2']],
            ['IAT1', results['IAT1']],
            ['IAT2', results['IAT2']],
            ['IAT-D', results['IAT-D']]
        ]

        # Append to the original DataFrame
        append_df = pd.DataFrame(append_rows, columns=list(df.columns[:2]))
        df_updated = pd.concat([df, append_df], ignore_index=True)

        # Save updated file
        output_filename = file.replace('.csv', '_IAT.csv')
        df_updated.to_csv(os.path.join(folder_path, output_filename), index=False)
        print(f"✅ Processed: {output_filename}")

# === Create IAT-D summary file ===
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(os.path.join(folder_path, 'IAT_summary.csv'), index=False)
print("📊 Summary file saved as 'IAT_summary.csv'")

