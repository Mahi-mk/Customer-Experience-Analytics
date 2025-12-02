from google_play_scraper import Sort

# -----------------
# APP CONFIGURATION
# -----------------
# NOTE: These App IDs were found by searching the Google Play Store.
APP_IDS = {
    'CBE': 'com.combanketh.mobilebanking',  
    'BOA': 'com.boa.boaMobileBanking',      
    'Dashen': 'com.dashen.dashensuperapp' 
}

# Scraping settings
REVIEW_COUNT_PER_BANK = 500  # Target slightly more than 400 to ensure min 400 are kept
LANG = 'en'
COUNTRY = 'us'
SORT_ORDER = Sort.NEWEST

# -----------------
# FILE & COLUMN CONFIGURATION
# -----------------
RAW_DATA_FILE = 'data/raw/raw_bank_reviews.csv'
CLEAN_DATA_FILE = 'data/processed/clean_bank_reviews.csv'

# Column renaming map for preprocessing
COLUMN_RENAME_MAP = {
    'content': 'review_text',
    'score': 'rating',
    'at': 'date'
}


# Final required columns for the clean dataset
FINAL_COLUMNS = [
    'review_text', 'rating', 'date', 'bank', 'source'
]

# Source constant
DATA_SOURCE = 'Google Play'
