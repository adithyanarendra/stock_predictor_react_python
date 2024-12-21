import pg8000
from pg8000.dbapi import connect
from config import DB_CONFIG

def create_connection(database=None, autocommit=False):
    """
    Create a database connection.
    """
    conn = connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=database or "postgres",
    )
    conn.autocommit = autocommit
    return conn

def init_db():
    """
    Initialize the database and create required tables.
    """
    conn = create_connection(autocommit=True)
    cursor = conn.cursor()

    # Create the database if it doesn't exist
    try:
        cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' created successfully.")
    except pg8000.exceptions.DatabaseError as e:
        if e.args[0].get('C') == '42P04':
            print(f"Database '{DB_CONFIG['database']}' already exists.")
        else:
            raise e
    finally:
        conn.close()

    # Create the table for storing predictions
    conn = create_connection(database=DB_CONFIG["database"])
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            stock_symbol TEXT,
            timestamp TIMESTAMP,
            actual_price FLOAT,
            predicted_price FLOAT,
            mape FLOAT,
            rmse FLOAT
        )
    """)
    
    try:
        cursor.execute("""
            ALTER TABLE predictions
            ADD COLUMN IF NOT EXISTS mape FLOAT,
            ADD COLUMN IF NOT EXISTS rmse FLOAT
        """)
    except Exception as e:
        print(f"Error updating table: {e}")

    conn.commit()
    conn.close()
    print("Database initialized and table created successfully.")

def insert_prediction(stock_symbol, timestamp, actual_price, predicted_price, mape, rmse):
    """
    Insert prediction data into the database.
    """
    conn = create_connection(database=DB_CONFIG["database"])
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (stock_symbol, timestamp, actual_price, predicted_price, mape, rmse)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (stock_symbol, timestamp, actual_price, predicted_price, mape, rmse))
    conn.commit()
    conn.close()
    print(f"Inserted prediction for {stock_symbol} at {timestamp}.")

def fetch_accuracy():
    """
    Fetch the most recent prediction accuracy records.
    """
    conn = create_connection(database=DB_CONFIG["database"])
    cursor = conn.cursor()
    cursor.execute("""
        SELECT stock_symbol, timestamp, accuracy
        FROM predictions
        ORDER BY timestamp DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{"stock_symbol": row[0], "timestamp": row[1], "accuracy": row[2]} for row in rows]
