import argparse
import openai
import json

from query import select_from_table
from schema import get_schema
from db import create_connection

DATABASE = "./pythonsqlite.db"

def main(conn, question):
    with open("auth.json", "r") as f:
        auth = json.load(f)
    # Load your API key from an environment variable or secret management service
    #openai.api_key = os.getenv(auth['api_key'])
    openai.api_key = auth['api_key']
    print(f"Question: {question}")

    prompt = f"""
    
    Given the following SQL Schema:{get_schema()}
    Write a SQL query to answer this question: {question}
    
    """

    messages=[
        {"role": "system", "content": "You are a helpful assistant that returns only syntactically correct SQL."},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=600
    )



    q = response["choices"][0]["message"]["content"]

    print(f"AI-generated SQL query: \n{q}")
    print("Answer: \n")
    select_from_table(conn, q)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default="When was the last time that PARTY INVITES FOOTBALL product was purchased?")
    args = parser.parse_args()
    conn = create_connection(DATABASE)

    main(conn, question=args.query)

