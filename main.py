from flask import Flask, render_template, request, jsonify
from interview.interview import TechnicalInterview
from utils.vector_store import load_faiss_vector_store
from langchain_openai import ChatOpenAI
from config.config import LLM_PARAMS
import warnings

# OpenAI API Key
OPENAI_API_KEY = "your-openai-api-key"
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")

# Initialize Flask app
app = Flask(__name__)

# Global variable to hold interview instance
interview = None

@app.route('/')
def index():
    return render_template('index.html')  # Initial page to input topic

@app.route('/start_interview', methods=['POST'])
def start_interview():
    global interview
    topic = request.form.get('topic')

    try:
        # Load FAISS vector store for the topic
        vector_store, faiss_index = load_faiss_vector_store(topic, OPENAI_API_KEY)
    except ValueError as e:
        return f"Error: {str(e)}", 500

    # Initialize the interview system
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=LLM_PARAMS['temperature'], openai_api_key=OPENAI_API_KEY)
    interview = TechnicalInterview(llm, vector_store, faiss_index, OPENAI_API_KEY)

    # Start the interview process and get the first question
    question = interview.ask_question(topic, 0)
    return render_template('interview.html', question=question, topic=topic)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    answer = request.form.get('answer')
    topic = request.form.get('topic')

    # Evaluate the answer
    evaluation = interview.evaluate_answer_intelligently(answer)
    
    # Get the next question
    question_num = int(request.form.get('question_num')) + 1
    next_question = interview.ask_question(topic, question_num)
    
    return jsonify({
        'evaluation': evaluation,
        'next_question': next_question
    })

if __name__ == "__main__":
    app.run(debug=True)
