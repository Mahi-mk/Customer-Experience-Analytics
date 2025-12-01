# Google Play App IDs
APP_IDS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

# Number of reviews per bank (assignment requirement: 400+)
REVIEWS_PER_BANK = 450   # safer than exactly 400

# Output CSV file
OUTPUT_CSV = "data/reviews_clean.csv"

# File paths
DATA_PATHS = {
    "raw_reviews": "data/raw/reviews_raw.csv",           # raw scraped reviews
    "processed_reviews": "data/processed/reviews_clean.csv"  # cleaned CSV
}

# Database Config (for Task 3)
DB_CONFIG = {
    "dbname": "bank_reviews",
    "user": "postgres",
    "password": "yourpassword",   # change this later
    "host": "localhost",
    "port": "5432"
}
