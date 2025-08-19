from transformers import pipeline
import google.generativeai as genai
import time

# Set up Gemini API
GOOGLE_API_KEY = "AIzaSyBISLngvU2XTW15hcFqS3dZnSap4Yh8X5w" #AIzaSyCajFF0yNywiqHnwdkeuDxZ5Y0FOAbEsvE
genai.configure(api_key=GOOGLE_API_KEY)

# Use Gemini 1.5 Pro
model = genai.GenerativeModel('gemini-1.5-pro')

file_path = './sample_data2.txt'

# Read the file
with open(file_path, 'r') as file:
    data = file.read()
transcript = data


#first layer that imp
print(transcript[:100])
task_specification = "question-answering"
model_name = "deepset/roberta-base-squad2"
qa_pipeline = pipeline(task_specification, model=model_name)

def answer_factoid_question(question):
    result = qa_pipeline(question=question, context=transcript)
    return result["answer"]

question = "when are we going to implement them into promotional material?"
print(answer_factoid_question(question))


def gemini_orchestrator(user_question):
    # Step 1: Generate factoid sub-questions using Gemini
    prompt = f"""
    You are a helpful assistant that breaks down complex questions into factoid sub-questions.
    User Question: {user_question}
    Generate a list of 3-5 factoid sub-questions that can be used to extract precise information from a meeting transcript.
    """

    response = model.generate_content(prompt)
    sub_questions = response.text.split("\n")[:20]
    print("Generated Sub-Questions:", sub_questions)

    # Step 2: Answer each sub-question using the first layer
    factoid_answers = {}
    for q in sub_questions:
        if q.strip():  # Skip empty lines
            answer = answer_factoid_question(q.strip())
            factoid_answers[q.strip()] = answer
    print("Factoid Answers:", factoid_answers)

    # Step 3: Refine and consolidate answers using Gemini
    refinement_prompt = f"""
    You are a helpful assistant that refines and consolidates answers into a final response.
    User Question: {user_question}
    Factoid Answers: {factoid_answers}
    Please refine the answers into a clear, concise, and user-friendly response.
    """
    time.sleep(120)
    refinement_response = model.generate_content(refinement_prompt)
    final_response = refinement_response.text
    return final_response

question = "What happened with the crash?"

print(gemini_orchestrator(question))