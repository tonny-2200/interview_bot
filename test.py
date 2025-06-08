# Importing necessary libraries
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import mysql.connector
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

# Initialize chat model
model = ChatOpenAI(
    openai_api_key=api_key,
    openai_api_base="https://api.mistral.ai/v1",
    model_name="mistral-small",
    temperature=0.7
)

# Mysql database insert function
def insert_user_details(user_data):
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255),
                email VARCHAR(255),
                phone BIGINT,
                years_experience INT,
                desired_position TEXT,
                current_location VARCHAR(255),
                tech_stack TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO user_details (
                full_name, email, phone, years_experience,
                desired_position, current_location, tech_stack
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            user_data["Full Name"],
            user_data["Email Address"],
            user_data["Phone Number"],
            user_data["Years of Experience"],
            user_data["Desired Position(s)"],
            user_data["Current Location"],
            user_data["Tech Stack"]
        ))
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Load/save chat history in a JSON file
def load_json_history():
    file = 'chat_history.json'
    if not os.path.exists(file) or os.stat(file).st_size == 0:
        return []
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_history(messages):
    file = 'chat_history.json'
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2)

# Streamlit UI
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.title("🤖 Tanmay's Interview AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_details" not in st.session_state:
    st.session_state.user_details = None
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

with st.sidebar:
    st.header("📋 Enter Candidate Details")
    with st.form(key="user_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        exp = st.number_input("Years of Experience", min_value=0, step=1)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")
        stack = st.text_area("Tech Stack")
        submit_btn = st.form_submit_button("Start Interview")

    if submit_btn:
        if name and email and phone.isdigit() and stack:
            st.session_state.user_details = {
                "Full Name": name,
                "Email Address": email,
                "Phone Number": int(phone),
                "Years of Experience": int(exp),
                "Desired Position(s)": position,
                "Current Location": location,
                "Tech Stack": stack
            }

            insert_user_details(st.session_state.user_details)

            # Interview initiation
            tech_stack = stack
            system_msg = SystemMessage(content=f"You are an interview assistant. Based on the candidate's tech stack: "
                                               f"{tech_stack}, ask relevant interview questions but keep the track using this system message. "
                                               "Do not ask more than 4 questions. "
                                               "Wait for the user's answer before asking the next question. "
                                               "Only one question after this system message. "
                                               "Questions should not exceed 30 words.")
            st.session_state.chat_history = [system_msg]
            first_response = model.invoke(st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=first_response.content))
            st.session_state.messages.append(("assistant", first_response.content))
            save_json_history([
                {"role": "system", "content": system_msg.content},
                {"role": "assistant", "content": first_response.content}
            ])
            st.session_state.interview_started = True
        else:
            st.warning("Please fill out all required fields properly.")

# Chat interface
if st.session_state.interview_started:
    for role, msg in st.session_state.messages:
        st.chat_message(role).write(msg)
    st.info("💡 Type `exit` to end the interview.")
    user_input = st.chat_input("Type your response...")
    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        st.session_state.messages.append(("user", user_input))

        response = model.invoke(st.session_state.chat_history)
        st.chat_message("assistant").write(response.content)
        st.session_state.chat_history.append(AIMessage(content=response.content))
        st.session_state.messages.append(("assistant", response.content))

        prev_history = load_json_history()
        prev_history.extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response.content}
        ])
        save_json_history(prev_history)   # Chats saved to JSON file
