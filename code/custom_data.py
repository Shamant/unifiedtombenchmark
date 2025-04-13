# This code is made to run on the specified format files we have created for our custom datasets. Also, these are baseline models without any perspective taking.
import pandas as pd
file_path = '/evolving_stories_250.xlsx'
# Path to the custom dataset file - modify this path to point to your specific file location

excel_data = pd.ExcelFile(file_path)
df = pd.read_excel(excel_data, sheet_name='Sheet1')

df.columns = df.columns.str.strip()
# Clean column names by removing any whitespace

answer_column = 'Answers'
# The column name that contains the correct answers - modify this to match your dataset's column name

questions = {}
# Dictionary to store questions and their answers

for _, row in df.iterrows():
    # Format each question with the scenario, question, and options from the custom dataset
    question_text = f'Story: {row["Scenario"]}.  Question: {row["Question"]}. Options: {row["Options"]}'
    answer = row[answer_column]
    questions[question_text] = answer
    # Store the formatted question and its correct answer in the dictionary

import os
os.environ["OPENAI_API_KEY"] = "your_api_key"
# Set up the OpenAI API key - replace with your actual key or use a more secure method

from openai import OpenAI
client = OpenAI()
# Initialize the OpenAI client - this would need to be changed for different model providers

total = 0    # Counter for total questions asked
counter = 0  # Counter for correctly answered questions

def ask(q, ans):
    global total, counter
    total += 1
    
    # Query the model with the question
    response = client.chat.completions.create(
    model="gpt-4o",  # The model being tested - change this to test different models
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": q+" reply only with the option. for ex: D"}
    ]
    )
    
    response = response.choices[0].message.content
    # Check if the model's answer matches the correct answer
    if response.strip() == ans:
        counter += 1

# Test the model on all questions in the custom dataset
for q, ans in questions.items():
    ask(q, ans)

# Output results
print(total)
print(counter)
# The accuracy can be calculated as counter/total
