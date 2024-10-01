import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Load the Groq API
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model_name="llama-3.1-70b-versatile")

# Initialize session state for conversation and intro
if 'conversation' not in st.session_state:
    st.session_state.conversation = []  # Store question-answer pairs

if 'intro' not in st.session_state:
    st.session_state.intro = ""  # Store the topic brief

# Initialize last selected algorithm
if 'last_selected_algorithm' not in st.session_state:
    st.session_state.last_selected_algorithm = None

# Function to select algorithm
def select_algorithm():
    sorting_algorithms = ["Enter Your Question", "Linked List", "Stack", "Queue", "Tree", "Graph"]
    return st.selectbox("Select the data structure topic you want to learn:", sorting_algorithms, index=0)

# Function to handle custom question input
def handle_custom_question(user_question):
    prompt = f"Provide a detailed explanation for the following question: '{user_question}'"
    response = llm.invoke(prompt)
    return response.content

# Generate a question based on the topic
def generate_question(algorithm, previous_answers=[]):
    prompt = f"You are a teaching assistant for data structure. The student is learning {algorithm}. Generate a Socratic question that is appropriate to their current understanding."
    # if previous_answers:
    #     prompt += " The student has answered the following so far: " + str(previous_answers)
    
    response = llm.invoke(prompt)
    return response.content

# Analyze user's answer and generate follow-up
def socratic_followup(question, user_answer):
    prompt = f"The question was: '{question}'. The student answered: '{user_answer}'. If the answer was wrong, generate a simpler, guiding question. If it was correct, generate the next more complex question."
    response = llm.invoke(prompt)
    return response.content

# Streamlit UI
st.title("Data Structures Tutor")

# Select the algorithm to learn
selected_algorithm = select_algorithm()

# Only proceed if the user has selected a valid topic (i.e., not the empty option)
if selected_algorithm and selected_algorithm != "Enter Your Question":
    if st.session_state.last_selected_algorithm != selected_algorithm:
        st.session_state.conversation = []
        st.session_state.intro = ""
        st.session_state.last_selected_algorithm = selected_algorithm 
    
    # Generate introduction to the selected topic, if not already generated
    if not st.session_state.intro:
        response = llm.invoke(f"Give a brief introduction of 5-6 lines about the {str(selected_algorithm)} data structure.")
        st.session_state.intro = response.content

    st.subheader("Topic Brief")
    st.write(st.session_state.intro)

    # Generate first question if conversation hasn't started
    if not st.session_state.conversation:
        first_question = generate_question(selected_algorithm)
        st.session_state.conversation.append({"question": first_question, "answer": ""})

    # Display chat history
    for qa in st.session_state.conversation:
        st.subheader("Question")
        st.write(qa['question'])
        if qa['answer']:
            st.subheader("Answer")
            st.write(qa['answer'])

    # Input for the user's answer to the latest question
    user_answer = st.text_area("Your Answer:", key=f"answer_{len(st.session_state.conversation)}")

    if user_answer:
        # Update the last question with user's answer
        st.session_state.conversation[-1]["answer"] = user_answer

        # Generate a follow-up question or feedback
        follow_up = socratic_followup(st.session_state.conversation[-1]["question"], user_answer)

        # Add the new follow-up question to the conversation
        st.session_state.conversation.append({"question": follow_up, "answer": ""})

        # Auto-scroll to the latest question
        st.rerun()
elif selected_algorithm == "Enter Your Question":
    custom_question = st.text_area("Enter Your Question:")
    
    # if st.button("Submit Question"):
    if custom_question:
        answer = handle_custom_question(custom_question)
        st.subheader("Answer")
        st.write(answer)
    else:
        st.warning("Please enter a question before submitting.")
else:
    st.write("Please select a topic to start learning.")













# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq

# load_dotenv()

# ## Load the Groq API
# os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
# # llm=ChatGroq(model_name = "llama-3.2-11b-text-preview")
# llm=ChatGroq(model_name = "llama-3.1-70b-versatile")


# def select_algorithm():
#     sorting_algorithms = ["Linked List", "Stack", "Queue", "Tree", "Graph"]
#     print("Select the data structure topic you want to learn:")
#     for i, algo in enumerate(sorting_algorithms, 1):
#         print(f"{i}. {algo}")
#     choice = int(input("Enter the number of your choice: "))
#     return sorting_algorithms[choice - 1]

# def generate_question(algorithm, previous_answers=[]):
#     # Dynamically generate a question based on the student's progress
#     prompt = f"You are a teaching assistant for data structure. The student is learning {algorithm}. Generate a Socratic question that is appropriate to their current understanding."
#     if previous_answers:
#         prompt += " The student has answered the following so far: " + str(previous_answers)
    
#     response = llm.invoke(prompt)
#     return response.content

# def analyze_answer(algorithm, question, user_answer):
#     # Ask the LLM to analyze the answer and decide next step
#     prompt = f"As a Socratic teacher, analyze the student's response to this question: '{question}' The student answered: '{user_answer}'. Based on this, generate a follow-up question or provide feedback."
    
#     response = llm.invoke(prompt)
#     return response.content

# def socratic_followup(question, user_answer):
#     prompt = f"The question was: '{question}'. The student answered: '{user_answer}'. If the answer was wrong, generate a simpler, guiding question. If it was correct, generate the next more complex question."
    
#     response = llm.invoke(prompt)
#     return response.content

# selected_algorithm = select_algorithm()
# # selected_algorithm = "Linked List"

# response = llm.invoke(f"Give a brief introduction of 5-6 lines about the {str(selected_algorithm)} data structure.")
# print("Topic Brief :\n  ",response.content)
# question = generate_question(selected_algorithm)
# print("\n\nQuestion: ", question)
# isRunning = True
# while isRunning:
#     user_answer = input("\n\nYour Answer: ")
#     if user_answer == "quit":
#         isRunning = False
#     else:
#         simplified_question_or_feedback = socratic_followup(question, user_answer)
#         print("\n\nFollow-up: ", simplified_question_or_feedback)