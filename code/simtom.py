from openai import OpenAI
import os
import pandas as pd

# Set up the OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_api_key"
# Note: Replace with your actual API key or use a more secure method like environment variables

# Initialize the OpenAI client
client = OpenAI()
# Note: If using a different model provider (Gemini, Llama, etc.), you'll need to import and initialize
# their respective client libraries instead

total = 0    # Counter for total questions processed
correct = 0  # Counter for correctly answered questions

# Function to extract character names using NER (Named Entity Recognition)
def extract_main_character_name(story):
    # This function uses GPT-4o to identify the main character in a story
    # For other models, you'd need to modify the model parameter and possibly the prompt format
    prompt = f"Identify the main character in the following story:\n\n{story}. reply only with the name of the character. for ex: Xiao Ming"
    response = client.chat.completions.create(
        model="gpt-4o",  # Change this to your preferred model (e.g., "gemini-pro" or "llama-3-70b")
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
    # Note: Different APIs have different response structures
    # For Gemini: return gemini_response.text
    # For Llama (via ollama): return llama_response.choices[0].message.content

# Function to perform perspective-taking
def perspective_taking(story, character_name):
    # This function determines what events the character knows about
    # This step is crucial for ToM testing as it assesses the model's ability to track character knowledge
    prompt = f"The following is a sequence of events:\n{story}\nWhich events does {character_name} know about?"
    response = client.chat.completions.create(
        model="gpt-4o",  # Change to your preferred model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
    # Adapt return statement based on the API you're using

# Function to perform question-answering
def question_answering(filtered_story, question):
    # This function asks the model to answer questions based on a filtered story (from perspective-taking)
    prompt = f"{filtered_story}\nAnswer the following question:\n{question}"
    response = client.chat.completions.create(
        model="gpt-4o",  # Change to your preferred model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt + ". You must answer by choosing an option. Doesn't matter if you don't know; take a guess in this case. for ex: D"}
        ]
    )
    return response.choices[0].message.content.strip()
    # Adapt return statement based on the API you're using

# Load Excel data
file_path = '/ToMBench_release_v1_0618.xlsx'
# Path to your TOM benchmark questions file
excel_data = pd.ExcelFile(file_path)
df = pd.read_excel(excel_data, sheet_name='Unexpected Outcome Test')
# This specifically loads the 'Unexpected Outcome Test' sheet - change as needed for other test types

# Clean up column names
df.columns = df.columns.str.strip()

# Define relevant columns
ability_column = '能力\nABILITY'  # Bilingual column name (Chinese/English)
answer_column = '答案\nANSWER'    # Bilingual column name (Chinese/English)

# Dictionaries to store questions based on their ability type
belief_false_location_dict = {}
typical_emotion_dict = {}
atypical_emotion_dict = {}

# Populate dictionaries with questions and answers from Excel
for _, row in df.iterrows():
    ability = row[ability_column]
    question_text = f'Story: {row["STORY"]}.  Question: {row["QUESTION"]}. Option A: {row["OPTION-A"]}, Option B: {row["OPTION-B"]}, Option C: {row["OPTION-C"]}, Option D: {row["OPTION-D"]}. reply only with the option. for ex: D. dont say D. Curious instead say D'
    answer = row[answer_column]

    # Categorize questions based on their ability type
    if "Belief: Sequence false beliefs" in ability:
        belief_false_location_dict[question_text] = answer
    elif "Emotion: Typical emotional reactions" in ability:
        typical_emotion_dict[question_text] = answer
    elif "Emotion: Atypical emotional reactions" in ability:
        atypical_emotion_dict[question_text] = answer

# Function to ask a question and evaluate the response
def ask_question(question_text, correct_answer):
    global total, correct
    total += 1
    
    # Extract the story part from the question text
    story_part = question_text.split("Question:")[0].replace("Story: ", "")
    print(story_part)
    
    # Stage 0: Extract the main character name
    character_name = extract_main_character_name(story_part)
    print(character_name)

    # Stage 1: Perspective-Taking - understand what the character knows
    filtered_story = perspective_taking(story_part, character_name)
    print(filtered_story)

    # Stage 2: Question-Answering - answer based on character's perspective
    response = question_answering(filtered_story, question_text.split("Question:")[1].strip())
    print(response)
    print(correct_answer)

    # Check if the response is correct (ignoring periods)
    if response.replace(".", "") == correct_answer:
       correct += 1

# Execute testing on the atypical emotion questions
# You can change this to test other categories like belief_false_location_dict or typical_emotion_dict
for question, correct_answer in atypical_emotion_dict.items():
    ask_question(question, correct_answer)

# Print the results
print(f"Total questions: {total}")
print(f"Correct answers: {correct}")
print(f"Accuracy: {correct / total * 100:.2f}%")
