import sqlite3

DB_FILE = "./keylogs.db"  # Replace with your actual database file path


def check_table_existence(table_name):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # Query SQLite schema to check if table exists
        c.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        )

        # Fetch the result
        result = c.fetchone()

        conn.close()

        # Return True if table exists, False otherwise
        return result is not None

    except sqlite3.Error as e:
        print(f"Error checking table existence: {e}")
        return False


# Example usage
if __name__ == "__main__":
    tables_to_check = ["logs", "clipboard_logs"]

    for table in tables_to_check:
        if check_table_existence(table):
            print(f"Table '{table}' exists in the database.")
        else:
            print(f"Table '{table}' does not exist in the database.")
