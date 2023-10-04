import argparse
import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def select_from_table(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()

        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    database = "./pythonsqlite.db"
    conn = create_connection(database)

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default="SELECT * FROM Transactions", help="SQL query to execute")
    args = parser.parse_args()

    if args.query:
        print(f"Executing query: {args.query}")
        select_from_table(conn, args.query)
    else:
        print("No query provided. Please use the --query parameter.")

    print("testing")
