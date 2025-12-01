import os
import pandas as pd
from google_play_scraper import reviews, Sort
from config import APP_IDS, SCRAPING_CONFIG, DATA_PATHS

# Ensure output directory exists
os.makedirs(os.path.dirname(DATA_PATHS["raw_reviews"]), exist_ok=True)

all_reviews = []  # start empty
REVIEWS_PER_BANK = SCRAPING_CONFIG["reviews_per_bank"]

print("\n=== Starting Real-Time Google Play Scraping ===\n")

for bank_code, app_id in APP_IDS.items():
    print(f"Scraping reviews for {bank_code} (App ID: {app_id})...")

    try:
        result, _ = reviews(
            app_id,
            lang=SCRAPING_CONFIG["lang"],
            country=SCRAPING_CONFIG["country"],
            count=REVIEWS_PER_BANK,
            sort=Sort.NEWEST
        )
    except Exception as e:
        print(f"Error scraping {bank_code}: {e}")
        continue

    for r in result:
        all_reviews.append({
            "review": r["content"],
            "rating": r["score"],
            "date": str(r["at"]).split(" ")[0],
            "bank": bank_code,
            "source": "Google Play"
        })

# Now save the raw scraped data
df = pd.DataFrame(all_reviews)
df.to_csv(DATA_PATHS["raw_reviews"], index=False)

print(f"\n✔ Scraping complete! Total reviews: {len(df)}")
print(f"✔ Raw file saved to → {DATA_PATHS['raw_reviews']}\n")

