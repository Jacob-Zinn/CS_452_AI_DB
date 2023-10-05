import argparse
import openai
import json

from query import select_from_table
from schema import get_schema, get_schema_in_md
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
    Using the SQL schema provided below, write a SQL query to answer this question: {question}. Format your response as syntactically correct SQL.
    
    SQL Schema:
    {get_schema_in_md()}

    SQL Query:
    """

    messages=[
        {"role": "system", "content": "You are a helpful assistant that responds with only syntactically correct SQL."},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # "gpt-4", #
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
    parser.add_argument("--query", type=str, default="Which country purchased the most items?")
    args = parser.parse_args()
    conn = create_connection(DATABASE)

    main(conn, question=args.query)


# DEMO PRMPTS:
# SUCCESS

# FAILED
# Which country purchased the most items in the month of September and how much was the total spend?