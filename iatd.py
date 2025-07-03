import os
import pandas as pd
import numpy as np

# === Folder path with input CSVs ===
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\April\Rename\Consent\Extract\step4\Recoded"

# === Output summary list ===
summary_data = []

# === Process each CSV ===
for file in os.listdir(folder_path):
    if file.endswith('.csv') and not file.endswith('_with_IAT_stats.csv'):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)

        # Ensure columns are numeric
        df.iloc[:, 4] = pd.to_numeric(df.iloc[:, 4], errors='coerce')  # Column E
        df.iloc[:, 9] = pd.to_numeric(df.iloc[:, 9], errors='coerce')  # Column J
        df.iloc[:, 10] = pd.to_numeric(df.iloc[:, 10], errors='coerce')  # Column K

        results = {}

        block_defs = {
            3: ('MnA1', 'SDA1', 'NA1'),
            4: ('MnA2', 'SDA2', 'NA2'),
            6: ('MnB1', 'SDB1', 'NB1'),
            7: ('MnB2', 'SDB2', 'NB2'),
        }

        for k, (mn, sd, n) in block_defs.items():
            block = df[(df.iloc[:, 9] == 0) & (df.iloc[:, 10] == k)].iloc[:, 4].dropna()
            results[mn] = block.mean()
            results[sd] = block.std()
            results[n] = block.count()

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

        # IAT scores
        results['IAT1'] = results['B1 - A1'] / results['Inclusive SD1'] if results['Inclusive SD1'] else np.nan
        results['IAT2'] = results['B2 - A2'] / results['Inclusive SD2'] if results['Inclusive SD2'] else np.nan
        results['IAT-D'] = np.nanmean([results['IAT1'], results['IAT2']])

        # Append to summary list
        summary_data.append({
            "File_ID": file[:12],
            "IAT-D": results['IAT-D']
        })

        # Prepare rows to append to individual file
        append_rows = []
        for k, (mn, sd, n) in block_defs.items():
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

        append_df = pd.DataFrame(append_rows, columns=list(df.columns[:2]))
        df_updated = pd.concat([df, append_df], ignore_index=True)

        # Save updated file
        new_file_name = file.replace('.csv', '_IAT.csv')
        df_updated.to_csv(os.path.join(folder_path, new_file_name), index=False)
        print(f"✅ Processed: {new_file_name}")

# === Save summary CSV ===
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(os.path.join(folder_path, 'IAT_summary.csv'), index=False)
print(f"\n📊 IAT summary saved as 'IAT_summary.csv'")
