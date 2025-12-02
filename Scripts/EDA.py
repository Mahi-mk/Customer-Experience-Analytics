import pandas as pd
import numpy as np

# Define the file path (based on your project structure)
CLEAN_DATA_FILE = 'data/processed/clean_bank_reviews.csv'

def run_task1_eda():
    """Performs Exploratory Data Analysis on the cleaned review data."""
    
    print("\n=============================================")
    print("      TASK 1: Exploratory Data Analysis      ")
    print("=============================================")

    try:
        # Load the cleaned data
        df = pd.read_csv(CLEAN_DATA_FILE)
    except FileNotFoundError:
        print(f"!!! ERROR: Clean data file not found at {CLEAN_DATA_FILE}.")
        print("Please ensure your Task 1 preprocessing script ran successfully.")
        return

    # --- 1. Data Quantity Check (KPI Check: 1,200+ reviews) ---
    total_reviews = len(df)
    print(f"\n[1] Data Quantity Check")
    print(f"-> Total Clean Reviews Collected: {total_reviews}")
    if total_reviews >= 1200:
        print("-> KPI Status: PASS (1,200+ reviews collected) 🎉")
    else:
        print("-> KPI Status: FAIL (Did not reach 1,200 minimum)")

    # --- 2. Data Structure and Schema Check ---
    print(f"\n[2] Data Structure Check")
    print("-> Columns and Data Types:")
    print(df.info(verbose=False))
    
    # Check for required columns
    required_cols = ['review_text', 'rating', 'date', 'bank', 'source']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if not missing_cols:
        print("-> Schema Status: PASS (All required columns are present)")
    else:
        print(f"-> Schema Status: FAIL (Missing columns: {missing_cols})")

    # --- 3. Data Quality Check (Missing Values) ---
    print(f"\n[3] Data Quality Check (Missing Values)")
    null_counts = df.isnull().sum()
    if null_counts.sum() == 0:
        print("-> Missing Value Status: PASS (No missing/null values found) ✅")
    else:
        print("-> Missing Value Status: FAIL (Missing values found):")
        print(null_counts[null_counts > 0])
        # Calculate percentage missing data
        percent_missing = (null_counts.sum() / (len(df) * len(df.columns))) * 100
        print(f"-> Total Missing Data Percentage: {percent_missing:.2f}%")
        if percent_missing < 5:
            print("-> KPI Status: PASS (<5% missing data)")
        else:
            print("-> KPI Status: FAIL (>=5% missing data)")


    # --- 4. Data Distribution (Reviews per Bank) ---
    print(f"\n[4] Review Distribution per Bank (KPI Check: 400+ per bank)")
    bank_counts = df['bank'].value_counts()
    print(bank_counts)
    if all(count >= 400 for count in bank_counts):
        print("-> KPI Status: PASS (400+ reviews per bank) 🏦")
    else:
        print("-> KPI Status: FAIL (At least one bank below 400 reviews)")


    # --- 5. Initial Conceptual Analysis (Rating Distribution) ---
    print(f"\n[5] Initial Conceptual Analysis (Rating Distribution)")
    rating_counts = df['rating'].value_counts().sort_index()
    rating_percent = df['rating'].value_counts(normalize=True).mul(100).sort_index()
    rating_summary = pd.DataFrame({'Count': rating_counts, 'Percentage': rating_percent.round(2).astype(str) + '%'})
    print(rating_summary)
    
    print("\n-> Observation:")
    print("The distribution often highlights a 'U-shape' (high 1-star and 5-star counts),")
    print("which is typical for user-submitted reviews where high satisfaction and high pain points drive feedback.")
    print("=============================================")


if __name__ == '__main__':
    run_task1_eda()