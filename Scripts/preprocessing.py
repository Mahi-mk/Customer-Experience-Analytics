import os
import pandas as pd
import re
from config import DATA_PATHS

# -----------------------------
# Step 0: Load raw reviews CSV
# -----------------------------
df_raw = pd.read_csv(DATA_PATHS["raw_reviews"])

# -----------------------------
# Step 1: Clean Text Function
# -----------------------------
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()                     # lowercase
    text = re.sub(r'\s+', ' ', text)       # remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)    # remove punctuation
    return text

# -----------------------------
# Step 2: Apply text cleaning
# -----------------------------
df_raw['review'] = df_raw['review'].apply(clean_text)

# -----------------------------
# Step 3: Remove duplicates
# -----------------------------
df_raw.drop_duplicates(subset=["review", "bank"], inplace=True)

# -----------------------------
# Step 4: Handle missing data
# -----------------------------
df_raw.dropna(subset=["review", "rating", "date"], inplace=True)

# -----------------------------
# Step 5: Normalize date
# -----------------------------
df_raw["date"] = pd.to_datetime(df_raw["date"]).dt.strftime("%Y-%m-%d")

# -----------------------------
# Step 6: Reorder columns to project spec
# -----------------------------
df_clean = df_raw[["review", "rating", "date", "bank", "source"]]

# -----------------------------
# Step 7: Ensure output directory exists
# -----------------------------
os.makedirs(os.path.dirname(DATA_PATHS["processed_reviews"]), exist_ok=True)

# -----------------------------
# Step 8: Save cleaned CSV
# -----------------------------
df_clean.to_csv(DATA_PATHS["processed_reviews"], index=False)

# -----------------------------
# Step 9: Summary print
# -----------------------------
print("\n✔ Task 1 preprocessing complete!")
print(f"✔ Total reviews after cleaning: {len(df_clean)}")
print(f"✔ File saved to → {DATA_PATHS['processed_reviews']}\n")

