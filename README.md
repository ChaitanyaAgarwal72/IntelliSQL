# 🧠 IntelliSQL

IntelliSQL is a smart and interactive web app that allows users to write natural language instructions which are seamlessly converted into executable SQL queries using **Google's Gemini Pro** model. It leverages **Streamlit** for a smooth UI experience and executes queries on a local **SQLite** database.

## 🚀 Features

- 🔍 **Natural Language to SQL**: Convert plain English queries into accurate SQL commands.
- ⚡ **Real-Time Execution**: Instantly run the generated SQL against a local SQLite database.
- 📊 **Visual Results**: Query results are beautifully rendered in tables.
- 🧠 **Powered by Google Gemini**: Utilizes Google's Gemini 2.0 Flash model for high-quality prompt handling.
- 🖥️ **Streamlit UI**: Clean, intuitive, and interactive frontend.

## 📸 Demo

[Click here to watch the Demo Video](https://drive.google.com/file/d/1OhpBbhSnxUMTJ0hOnCSyFyMKzuw-Wt3o/view?usp=sharing)

<br>

![Screenshot 2025-06-16 110439](https://github.com/user-attachments/assets/d268f35f-7fcb-4135-9c1a-9b85b35f38d3)


## 📦 Tech Stack

| Tool        | Role                          |
|-------------|-------------------------------|
| Python      | Core programming language     |
| Streamlit   | Web frontend framework        |
| SQLite      | Lightweight local database    |
| Gemini Pro  | Natural language to SQL AI    |
| dotenv      | Secure API key handling       |

## 🔧 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/ChaitanyaAgarwal72/IntelliSQL.git
   cd intellisql
2. **Set up a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   Configure your Gemini API key
4. **Configure your Gemini API key**
   **Create a `.env` file in the project root directory and add:**
   ```bash
   GOOGLE_API_KEY=your_google_gemini_api_key
5. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   
## 💡 Usage

- Go to the **Query Assistant** tab.
- Type natural language instructions like:
  - `Show all employees`
  - `Create a table called products with name, price, and category`
- The app will generate SQL using Gemini and execute it on the local SQLite DB.
- Results are displayed instantly in a readable table format.

## 🛡️ Note

All database operations happen **locally**. The only data sent to the Gemini model is the user’s English instruction for SQL generation. No actual database data is shared externally.

## 📄 License

This project is licensed under the **MIT License**.  
See the [`LICENSE`](LICENSE) file for more details.
