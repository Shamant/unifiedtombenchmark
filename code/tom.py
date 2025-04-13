
# This code outlines the testing process for certain baseline models such as gpt 4o, gpt 3.5 on the TOM(theory of mind) benchmark
import pandas as pd
file_path = '/ToMBench_release_v1_0618.xlsx.xlsx'
# Location of the TOM benchmark Excel file

excel_data = pd.ExcelFile(file_path)
df = pd.read_excel(excel_data, sheet_name='Scalar Implicature Test')
df.columns = df.columns.str.strip()

# Define the column names for ability type and correct answers
ability_column = '能力\nABILITY'
answer_column = '答案\nANSWER'

# Dictionary to store questions and their answers
knowledge = {}
for _, row in df.iterrows():
    ability = row[ability_column]
    # Format each question with story and multiple-choice options
    question_text = f'Story: {row["STORY"]}.  Question: {row["QUESTION"]}. Option A: {row["OPTION-A"]}, Option B: {row["OPTION-B"]}, Option C: {row["OPTION-C"]}, Option D: {row["OPTION-D"]}.'
    answer = row[answer_column]
    # Filter for questions only in the "Knowledge: Information-knowledge links" category
    if "Knowledge: Information-knowledge links" in ability:
        knowledge[question_text] = answer

# Set up OpenAI API
# You can modify this code based on different models you want to test. 
import os
os.environ["OPENAI_API_KEY"] = "your_api_key"
from openai import OpenAI
client = OpenAI()

# Track total questions and correct answers
total = 0
counter = 0

# Function to query the model and check if the answer is correct
def ask(q, ans):
    global total, counter
    total += 1
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": q+" reply only with the option. for ex: D"}
    ]
    )
    response = response.choices[0].message.content
    if response == ans:
        counter += 1

# Test the model on all questions in our filtered dataset
for q, ans in knowledge.items():
    ask(q, ans)

# Output results
print(total)
print(counter)
# Accuracy can be calculated as counter/total
