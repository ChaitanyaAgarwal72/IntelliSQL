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
    return response.text.strip().strip("``````").strip()


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


# Streamlit UI
def main():
    st.set_page_config(page_title="IntelliSQL", layout="wide")
    st.sidebar.title("Navigation")
    pages = ["Home", "About", "Query Assistant"]
    selection = st.sidebar.radio("Go to", pages)

    if selection == "Home":
        st.markdown("<h1 style='color:#4CAF50;'>Welcome to IntelliSQL!</h1>", unsafe_allow_html=True)
        st.markdown("""
        <div style='padding:20px;'>
            <h3 style='color:#4CAF50;'>Query your database using natural language</h3>
            <p style='color:#ffffff;'>Powered by Google's Gemini AI and Streamlit, IntelliSQL makes database interaction as easy as having a conversation.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='padding:15px; border-left:4px solid #4CAF50;'>
                <h4 style='color:#4CAF50;'>✨ Key Features</h4>
                <ul style='color:#ffffff;'>
                    <li>Natural language to SQL conversion</li>
                    <li>Real-time query execution</li>
                    <li>Visual results display</li>
                    <li>Local SQLite database support</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='padding:15px; border-left:4px solid #4CAF50;'>
                <h4 style='color:#4CAF50;'>🚀 Getting Started</h4>
                <ol style='color:#ffffff;'>
                    <li>Navigate to Query Assistant</li>
                    <li>Type your request in plain English</li>
                    <li>View and execute the generated SQL</li>
                    <li>See results instantly</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align:center; padding:10px;'>
            <p style='color:#ffffff;'>Try asking things like:</p>
            <p style='color:#ffffff;'><i>"Show all customers from New York"</i> or <i>"Create a products table with name, price and category"</i></p>
        </div>
        """, unsafe_allow_html=True)

    elif selection == "Query Assistant":
        st.markdown("<h1 style='color:#4CAF50;'>Query Assistant</h1>", unsafe_allow_html=True)
        
        user_input = st.text_area("Enter your natural language query:", height=100)
        
        if st.button("Generate SQL"):
            if user_input.strip():
                with st.spinner("Generating SQL..."):
                    try:
                        generated_sql = get_sql_from_prompt(user_input)
                        st.session_state.generated_sql = generated_sql
                    except Exception as e:
                        st.error(f"Failed to generate SQL: {str(e)}")
        
        if 'generated_sql' in st.session_state:
            st.markdown("### Generated SQL")
            st.code(st.session_state.generated_sql, language="sql")
            
            if st.button("Execute SQL"):
                with st.spinner("Executing..."):
                    rows, columns, error = execute_sql(st.session_state.generated_sql)
                    
                if error:
                    st.error(error)
                else:
                    st.success("Query executed successfully!")
                    if rows and columns:
                        st.markdown("### Results")
                        st.dataframe(rows, columns=columns)


if __name__ == "__main__":
    main()
# Run the Streamlit app
# To run the app, use the command: streamlit run app.py
