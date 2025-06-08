
🤖 AI Interview Assistant
A Streamlit-based web application that simulates a technical interview using a language model from Mistral AI. The assistant dynamically generates questions based on a candidate's tech stack and stores user details in a MySQL database.
🔧 Features

📋 Candidate Data Collection: Collects essential information via a sidebar form.
🧠 AI-Driven Interview: Uses the Mistral language model via LangChain to generate context-aware technical questions.
💬 Interactive Chat Interface: Enables a structured, sequential interview with a maximum of 4 AI-generated questions.
🗃 Chat History: Saves the interview conversation in a `chat_history.json` file.
🛢 MySQL Integration: Securely stores candidate details in a local or remote MySQL database.


## 🔐 .env File Configuration

Create a `.env` file in the root directory of your project and add the following keys:

env
# Mistral API Configuration
MISTRAL_API_KEY=your_mistral_api_key
# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=interview_db

🧠 How It Works
1. User fills in candidate details in the sidebar form.
2. On submission:
   * Details are stored in the MySQL database.
   * Interview session starts with a system prompt based on the tech stack.
3. The AI model asks up to 4 interview questions, waiting for your response after each.
4. Chat is stored persistently in `chat_history.json`.

📁 Project Structure
.
├── interview_assistant.py      # Main Streamlit app
├── chat_history.json           # Local chat log storage
├── .env                        # Environment variables
└── README.md                   # This file

🧑‍💻 Author
Developed by **Tanmay Thombare**.
📜 License

This project is licensed under the MIT License.


