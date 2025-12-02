import psycopg2
from psycopg2 import sql
import sys

# --- Configuration ---
SETUP_CONFIG = {
    "host": "localhost",
    "database": "postgres",  # <--- Connect to the default DB to create bank_reviews
    "user": "postgres", 
    "password": "password"
}

TARGET_DB_NAME = "bank_reviews"

def create_database_and_schema():
    """Handles the creation of the database and its tables."""
    
    # ----------------------------------------------------
    # PHASE 1: Connect to 'postgres' DB to CREATE the TARGET DATABASE
    # ----------------------------------------------------
    conn_sys = None
    try:
        conn_sys = psycopg2.connect(**SETUP_CONFIG)
        # Set isolation level for safety (required for CREATE DATABASE)
        conn_sys.autocommit = True
        cur_sys = conn_sys.cursor()

        # Check if the database already exists
        cur_sys.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TARGET_DB_NAME}'")
        if cur_sys.fetchone():
            print(f"Database '{TARGET_DB_NAME}' already exists.")
        else:
            print(f"Creating database '{TARGET_DB_NAME}'...")
            cur_sys.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(TARGET_DB_NAME)))
            print(f"Database '{TARGET_DB_NAME}' created successfully.")

        cur_sys.close()
        conn_sys.close()

    except Exception as e:
        print(f"Error during database creation: {e}", file=sys.stderr)
        if conn_sys:
            conn_sys.close()
        return False
        
    # ----------------------------------------------------
    # PHASE 2: Connect to the TARGET DATABASE to CREATE TABLES
    # ----------------------------------------------------
    conn_target = None
    try:
        # Update config to connect to the newly created database
        SETUP_CONFIG['database'] = TARGET_DB_NAME
        conn_target = psycopg2.connect(**SETUP_CONFIG)
        cur_target = conn_target.cursor()
        
        print(f"\nConnected to {TARGET_DB_NAME}. Creating tables...")

        # SQL to create the two required tables
        create_schema_sql = """
            -- 1. Banks Table
            CREATE TABLE IF NOT EXISTS Banks (
                bank_id SERIAL PRIMARY KEY,
                bank_name VARCHAR(100) NOT NULL UNIQUE,
                app_name VARCHAR(255)
            );

            -- 2. Reviews Table
            CREATE TABLE IF NOT EXISTS Reviews (
                review_id SERIAL PRIMARY KEY,
                bank_id INT NOT NULL,
                review_text TEXT,
                rating INT,
                review_date DATE,
                sentiment_label VARCHAR(10),
                sentiment_score NUMERIC(5, 4),
                identified_theme VARCHAR(50),
                source VARCHAR(50),
                
                -- Define the Foreign Key relationship
                FOREIGN KEY (bank_id) REFERENCES Banks (bank_id)
            );
        """
        
        cur_target.execute(create_schema_sql)
        conn_target.commit()
        print("Schema (Banks and Reviews tables) created/verified successfully.")
        
        cur_target.close()
        conn_target.close()
        return True

    except Exception as e:
        print(f"Error during table creation: {e}", file=sys.stderr)
        if conn_target:
            conn_target.rollback()
            conn_target.close()
        return False

if __name__ == "__main__":
    if create_database_and_schema():
        print("\nDatabase setup is complete. You can now run db_loader.py.")