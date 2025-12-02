import pandas as pd
from google_play_scraper import reviews
from config import APP_IDS, REVIEW_COUNT_PER_BANK, LANG, COUNTRY, SORT_ORDER, RAW_DATA_FILE

def scrape_data():
    """
    Scrapes reviews for all banks defined in the config file.
    Returns the raw DataFrame.
    """
    all_reviews = []
    
    print("--- Starting Data Scraping ---")

    for bank_name, app_id in APP_IDS.items():
        # ... (Scraping logic remains the same)
        print(f"Scraping reviews for {bank_name} ({app_id})...")
        try:
            bank_reviews, _ = reviews(
                app_id, lang=LANG, country=COUNTRY, sort=SORT_ORDER,
                count=REVIEW_COUNT_PER_BANK, filter_score_with=None
            )
            for review in bank_reviews:
                review['bank'] = bank_name
            all_reviews.extend(bank_reviews)
            print(f"-> Scraped {len(bank_reviews)} reviews for {bank_name}.")
        except Exception as e:
            print(f"!!! ERROR scraping {bank_name}: {e}")

    df_raw = pd.DataFrame(all_reviews)
    print(f"\nTotal raw reviews collected: {len(df_raw)}")
    
    # Optional: Save raw data for debugging
    df_raw.to_csv(RAW_DATA_FILE, index=False)
    
    return df_raw