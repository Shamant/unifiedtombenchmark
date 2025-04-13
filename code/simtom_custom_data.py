# This code is made to run on the specified format files we have created for our custom datasets. Also, these are custom models made based on perspective taking.
from openai import OpenAI
import os
import pandas as pd

# Set up the OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_api_key"
# Replace with your actual API key or use environment variables for security

# Initialize the OpenAI client
client = OpenAI()
# Note: For other models like Gemini, Claude, or Llama, you'd use their respective client libraries here

total = 0    # Counter for total questions processed
correct = 0  # Counter for correctly answered questions

# Function to extract character names using Named Entity Recognition
def extract_main_character_name(story):
    prompt = f"Identify the main character in the following story:\n\n{story}. reply only with the name of the character. for ex: Xiao Ming"
    response = client.chat.completions.create(
        model="gpt-4o",  # Change this model name to test different models
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
    # For different APIs, modify this return statement accordingly

# Function to perform perspective-taking - determining what information the character knows
def perspective_taking(story, character_name):
    prompt = f"The following is a sequence of events:\n{story}\nWhich events does {character_name} know about?"
    response = client.chat.completions.create(
        model="gpt-4o",  # Change this model name to test different models
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
    # For different APIs, modify this return statement accordingly

# Function to perform question-answering based on the character's perspective
def question_answering(filtered_story, question):
    prompt = f"{filtered_story}\nAnswer the following question:\n{question}"
    response = client.chat.completions.create(
        model="gpt-4o",  # Change this model name to test different models
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt + ". reply only with the option. for ex: A nothing else. don't reply like A) investigate the cause. only A "}
        ]
    )
    return response.choices[0].message.content.strip()
    # For different APIs, modify this return statement accordingly

# Load Excel data from custom multi-interaction dataset
file_path = '/multi_interaction_100.xlsx'
# Change this path to point to your specific dataset file

excel_data = pd.ExcelFile(file_path)
df = pd.read_excel(excel_data, sheet_name='Sheet1')
# Change 'Sheet1' to match your dataset's sheet name

df.columns = df.columns.str.strip()
# Clean column names by removing whitespace

i = 0  # Counter for tracking progress
answer_column = 'Answer'
# Column name containing correct answers - adjust to match your dataset structure

questions = {}
# Dictionary to store questions and their answers

for _, row in df.iterrows():
    # Format each question with the scenario, question, and options from the custom dataset
    question_text = f'Story: {row["Scenario"]}. Question: {row["Question"]} Options: {row["Options"]}'
    answer = row[answer_column]
    questions[question_text] = answer

# Function to ask a question and evaluate the response using perspective-taking approach
def ask_question(question_text, correct_answer):
    global total, correct
    total += 1
    
    # Extract the story part from the question text
    story_part = question_text.split("Question:")[0].replace("Story: ", "")
    
    # Stage 0: Extract the main character name
    character_name = extract_main_character_name(story_part)
    
    # Stage 1: Perspective-Taking - understand what the character knows
    filtered_story = perspective_taking(story_part, character_name)
    
    # Stage 2: Question-Answering - answer based on character's perspective
    response = question_answering(filtered_story, question_text.split("Question:")[1].strip())
    
    # Check if the response is correct (case-insensitive comparison)
    if response.replace(".", "").upper() == correct_answer.upper():
       correct += 1

# Evaluate the model on all questions in the custom dataset
for question, correct_answer in questions.items():
    i += 1
    print(i)  # Print progress counter
    ask_question(question, correct_answer)

# Print the results
print(f"Total questions: {total}")
print(f"Correct answers: {correct}")
print(f"Accuracy: {correct / total * 100:.2f}%")
