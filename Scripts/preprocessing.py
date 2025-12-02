import pandas as pd
from config import COLUMN_RENAME_MAP, FINAL_COLUMNS, DATA_SOURCE, CLEAN_DATA_FILE
from scraper import scrape_data # Import the scraping function

def preprocess_data(df):
    """
    Cleans, transforms, and formats the raw review DataFrame.
    """
    print("\n--- Starting Data Preprocessing ---")
    
    # 1. Select and rename required columns
    # ... (Preprocessing logic remains the same: renaming, dropping NaN, removing duplicates, date formatting, adding 'source' column)
    cols_to_keep = list(COLUMN_RENAME_MAP.keys()) + ['bank'] 
    
    try:
        df_clean = df[cols_to_keep]
    except KeyError as e:
        print(f"!!! ERROR: Missing column from raw data: {e}")
        return pd.DataFrame(columns=FINAL_COLUMNS) 

    df_clean = df_clean.rename(columns=COLUMN_RENAME_MAP)
    
    initial_count = len(df_clean)
    df_clean.dropna(subset=['review_text', 'rating', 'date'], inplace=True)
    dropped_count = initial_count - len(df_clean)
    print(f"-> Dropped {dropped_count} rows with missing data.")
    
    df_clean.drop_duplicates(subset=['review_text', 'bank', 'date'], inplace=True)
    print(f"-> Total unique reviews after dropping duplicates: {len(df_clean)}")

    df_clean['date'] = pd.to_datetime(df_clean['date']).dt.strftime('%Y-%m-%d')
    df_clean['source'] = DATA_SOURCE
    
    df_final = df_clean[FINAL_COLUMNS]

    print(f"\nFinal clean dataset size: {len(df_final)} reviews.")
    print(f"Reviews per bank:\n{df_final['bank'].value_counts()}")
    
    # Save the cleaned data
    df_final.to_csv(CLEAN_DATA_FILE, index=False)
    print(f"\nClean data saved to {CLEAN_DATA_FILE}")

    return df_final

# ------------------------------------
# ORCHESTRATION BLOCK (Replaces main.py)
# ------------------------------------
if __name__ == '__main__':
    print("--- Executing Task 1 Pipeline ---")
    
    # 1. Scrape the data
    raw_df = scrape_data()
    
    # Check if scraping returned data
    if raw_df.empty:
        print("\nPipeline failed: No raw data collected.")
    else:
        # 2. Preprocess the data
        clean_df = preprocess_data(raw_df)
        
        if not clean_df.empty:
            print("\n--- Pipeline Completed Successfully ---")
        else:
            print("\nPipeline failed: Preprocessing resulted in an empty dataset.")