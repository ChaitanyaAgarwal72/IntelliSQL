import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# SQLite DB file
DB_FILE = "data.db"

# Get Gemini response for SQL generation
def get_sql_from_prompt(user_input):
    prompt = f"""
    You are an expert in SQL. Convert the user's English instruction into a correct SQLite SQL statement.
    The response must contain only the SQL code without any extra comments, markdown, or explanation.

    Examples:
    Q: Show all students.
    A: SELECT * FROM STUDENTS;

    Q: Create a table named EMPLOYEE with name, age and salary.
    A: CREATE TABLE EMPLOYEE (Name TEXT, Age INTEGER, Salary REAL);

    Now convert this:
    Q: {user_input}
    A:
    """
    response = model.generate_content(prompt)
    return response.text.strip().strip("```sql").strip("```").strip()

# Execute SQL and return result
def execute_sql(query, db_file=DB_FILE):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        # If query is SELECT or SHOW-like
        if query.strip().lower().startswith("select"):
            col_names = [description[0] for description in cursor.description]
            return rows, col_names, None
        return None, None, "Executed successfully!"
    except Exception as e:
        return None, None, f"❌ Error: {e}"
    finally:
        conn.close()

