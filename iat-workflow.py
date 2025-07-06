import os
import re
import csv
import pandas as pd
import numpy as np
from openpyxl import Workbook

# === CONFIG ===
folder_path = r"C:\Users\60107393\OneDrive - University of Doha for Science and Technology\Research\UREP\30th Cycle\IAT\Phase 2b"
raw_folder = os.path.join(folder_path, "3002")
consent_folder = os.path.join(folder_path, "Consent")
extract_folder = os.path.join(consent_folder, "extract")
step4_folder = os.path.join(extract_folder, "step4")

summary_records = []

# === STEP 1: Rename files using M2 (Row 2, Column M) ===
for filename in os.listdir(raw_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(raw_folder, filename)
        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                second_row = next(reader, [])
                if len(second_row) >= 13:
                    new_name_raw = second_row[12]
                else:
                    continue
            if not new_name_raw:
                continue
            safe_name = re.sub(r'[\\/:"*?<>|]+", "", new_name_raw.strip())
            new_path = os.path.join(consent_folder, f"{safe_name}.csv")
            if not os.path.exists(new_path):
                os.rename(file_path, new_path)
        except Exception as e:
            print(f"[Rename Error] {filename}: {e}")

# === STEP 2: Filter by K in (3,4,6,7) ===
os.makedirs(extract_folder, exist_ok=True)
keep_values = {'3', '4', '6', '7'}
for filename in os.listdir(consent_folder):
    if filename.endswith('.csv'):
        in_file = os.path.join(consent_folder, filename)
        out_file = os.path.join(extract_folder, filename.replace('.csv', '_extract.csv'))
        with open(in_file, newline='', encoding='utf-8') as infile, open(out_file, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            header = next(reader)
            writer.writerow(header)
            for row in reader:
                if len(row) > 10 and row[10].strip() in keep_values:
                    writer.writerow(row)

# === STEP 3: Filter E < 10001 ===
os.makedirs(step4_folder, exist_ok=True)
for filename in os.listdir(extract_folder):
    if filename.endswith('.csv'):
        in_file = os.path.join(extract_folder, filename)
        out_file = os.path.join(step4_folder, filename.replace('.csv', '_step4.csv'))
        with open(in_file, newline='', encoding='utf-8') as infile, open(out_file, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            header = next(reader)
            writer.writerow(header)
            for row in reader:
                try:
                    if len(row) > 4 and float(row[4]) < 10001:
                        writer.writerow(row)
                except:
                    continue

# === STEP 4 & 5: Count Rows and Latencies < 300 and Rename Files ===
for filename in os.listdir(step4_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(step4_folder, filename)
        row_count = 0
        lt_300_count = 0
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                row_count += 1
                try:
                    if float(row[4]) < 300:
                        lt_300_count += 1
                except:
                    continue
        base, ext = os.path.splitext(filename)
        new_filename = f"{base}_N{row_count}_LT300N{lt_300_count}{ext}"
        os.rename(file_path, os.path.join(step4_folder, new_filename))

# === STEP 6-7-8: Append stats, recode errors, calculate IAT-D and generate summary ===
summary = []
for filename in os.listdir(step4_folder):
    if filename.endswith('.csv'):
        path = os.path.join(step4_folder, filename)
        df = pd.read_csv(path)
        df.iloc[:, 4] = pd.to_numeric(df.iloc[:, 4], errors='coerce')  # E
        df.iloc[:, 9] = pd.to_numeric(df.iloc[:, 9], errors='coerce')  # J
        df.iloc[:, 10] = pd.to_numeric(df.iloc[:, 10], errors='coerce')  # K

        means, stds, counts = {}, {}, {}
        for blk in [3, 4, 6, 7]:
            values = df[df.iloc[:, 10] == blk].iloc[:, 4].dropna()
            means[blk] = values.mean()
            stds[blk] = values.std()
            counts[blk] = values.count()

        # Replace errors (J==1)
        for blk in [3,4,6,7]:
            mask = (df.iloc[:, 9] == 1) & (df.iloc[:, 10] == blk)
            df.loc[mask, df.columns[4]] = means[blk] + 600

        # IAT Calculations
        try:
            SD1 = np.sqrt((((counts[3]-1)*stds[3]**2 + (counts[6]-1)*stds[6]**2) +
                          ((counts[3]+counts[6]) * ((means[3]-means[6])**2) / 4)) / (counts[3]+counts[6]-1))
            SD2 = np.sqrt((((counts[4]-1)*stds[4]**2 + (counts[7]-1)*stds[7]**2) +
                          ((counts[4]+counts[7]) * ((means[4]-means[7])**2) / 4)) / (counts[4]+counts[7]-1))
        except:
            SD1 = SD2 = np.nan

        IAT1 = (means[6] - means[3]) / SD1 if SD1 else np.nan
        IAT2 = (means[7] - means[4]) / SD2 if SD2 else np.nan
        IAT_D = np.nanmean([IAT1, IAT2])

        # Flip sign if Liberal Arts/Male,Science/Female AND K=3 in data
        if 'Liberal Arts/Male,Science/Female' in df.iloc[:, 8].astype(str).tolist() and 3 in df.iloc[:, 10].values:
            IAT_D *= -1

        PID = df.iloc[1, 12] if len(df.columns) > 12 else filename[:12]
        block_cond = df.iloc[2, 8] if len(df) > 2 and len(df.columns) > 8 else ""
        summary.append([PID, IAT_D, block_cond, row_count, lt_300_count])

        # Save updated file
        df.to_csv(path.replace('.csv', '_with_stats.csv'), index=False)

# === Export Summary ===
sum_df = pd.DataFrame(summary, columns=["PID", "IAT-D", "BlockCondition", "Rows_After_Step4", "Latencies<300"])
sum_df.to_excel(os.path.join(step4_folder, 'IAT_Final_Summary.xlsx'), index=False)
print("📊 IAT_Final_Summary.xlsx saved")
