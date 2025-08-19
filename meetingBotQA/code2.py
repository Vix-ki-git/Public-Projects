from transformers import pipeline
import google.generativeai as genai
import time

# Configuration
GOOGLE_API_KEY = "AIzaSyBISLngvU2XTW15hcFqS3dZnSap4Yh8X5w"
FILE_PATH = './sample_data2.txt'

# Set up Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Read the file
with open(FILE_PATH, 'r') as file:
    transcript = file.read()

# Initialize QA pipeline
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Function to answer factoid questions
def answer_factoid_question(question, context):
    result = qa_pipeline(question=question, context=context)
    return result["answer"]

# Function to orchestrate Gemini for complex questions
def gemini_orchestrator(user_question, context):
    # Step 1: Generate factoid sub-questions using Gemini
    prompt = f"""
    You are a helpful assistant that breaks down complex questions into factoid sub-questions.
    User Question: {user_question}
    Generate a list of 3-5 factoid sub-questions that can be used to extract precise information from a meeting transcript.
    """
    response = model.generate_content(prompt)
    sub_questions = response.text.split("\n")[:20]
    print("Generated Sub-Questions:", sub_questions)

    # Step 2: Answer each sub-question using the QA pipeline
    factoid_answers = {}
    for q in sub_questions:
        if q.strip():  # Skip empty lines
            answer = answer_factoid_question(q.strip(), context)
            factoid_answers[q.strip()] = answer
    print("Factoid Answers:", factoid_answers)

    # Step 3: Refine and consolidate answers using Gemini
    refinement_prompt = f"""
    You are a helpful assistant that refines and consolidates answers into a final response.
    User Question: {user_question}
    Factoid Answers: {factoid_answers}
    Please refine the answers into a clear, concise, and user-friendly response.
    """
    time.sleep(120)  # Consider reducing or removing this delay
    refinement_response = model.generate_content(refinement_prompt)
    return refinement_response.text

# Example usage
question = "What happened with the crash?"
print(gemini_orchestrator(question, transcript))