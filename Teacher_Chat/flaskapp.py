# 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
import os
from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load the Groq API key
os.environ['GROQ_API_KEY'] = "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"
llm = ChatGroq(model_name="llama-3.1-70b-versatile")

# Define a simple prompt template for the conversation
prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="You are a helpful assistant. Respond to the user's question: {user_input}"
)

memory = ConversationBufferWindowMemory(k=10)
conversation_chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    memory=memory,
)


# Helper functions

def generate_question(algorithm):
    prompt = f"You are a teaching assistant for data structure. The student is learning {algorithm}. Generate a Socratic question that is appropriate to their current understanding."
    response = llm.invoke(prompt)
    return response.content

def socratic_followup(question, user_answer):
    prompt = f"The question was: '{question}'. The student answered: '{user_answer}'. If the answer was wrong, generate a simpler, guiding question. If it was correct, generate the next more complex question."
    response = llm.invoke(prompt)
    return response.content

def custom_question_response(user_question):
    que = f"Answer the following question: '{user_question}'"
    # response = llm.invoke(prompt)
    if memory.chat_memory.messages:
        print("IFFFFFFFFFFFFF")
        response = conversation_chain.invoke({"user_input": que, "history": memory.chat_memory.messages})
    else:
        print("ELSEEEEEEEEEEEEEEEEEEEEE")
        response = conversation_chain.invoke({"user_input": que})

    print("Current Memory State:")
    print(conversation_chain.memory.buffer)

    print("=============",response,"================")
    return response['text']

# API route for handling conversation
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # print("DATA++++++++++++++++++++++++++++",data,"++++++++++++++++++++++++++++")
    selected_algorithm = data.get('algorithm')
    user_answer = data.get('answer', "")
    user_question = data.get('user_question', "")

    # Check if it's a custom question request
    if selected_algorithm == "Ask a Question":
        if user_question:
            response = custom_question_response(user_question)
            return jsonify({"question": response})
        else:
            return jsonify({"error": "Please provide a question."}), 400

    # Handle predefined topics
    if selected_algorithm:
        if not user_answer:  # Initial question
            first_question = generate_question(selected_algorithm)
            return jsonify({"question": first_question})
        else:  # Generate follow-up
            last_question = data.get('last_question', "")
            follow_up = socratic_followup(last_question, user_answer)
            return jsonify({"question": follow_up})

    return jsonify({"error": "Invalid request"}), 400

# Simple frontend route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
