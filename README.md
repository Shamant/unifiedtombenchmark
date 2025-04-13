# SimToM: Theory of Mind Benchmark Testing

## Overview

SimToM is a framework for testing Language Models (LLMs) on Theory of Mind (ToM) tasks. Theory of Mind refers to the ability to attribute mental states—beliefs, intents, desires, emotions, knowledge—to oneself and others, and to understand that others have beliefs, desires, intentions, and perspectives that are different from one's own.

This repository contains code for evaluating how well various LLMs can perform on ToM reasoning tasks through different testing methodologies.

## Features

- Evaluate LLMs on standard ToM benchmarks including:
- Support for different testing approaches:
  - Direct question answering
  - Multi-stage perspective-taking pipeline
- Flexibility to test multiple models (OpenAI, Google, Meta, Anthropic, etc.)
- Customizable for different datasets and test formats

## Testing Methodologies

### Direct Question Answering

The simplest approach directly queries the model with the full story and question, evaluating if it can correctly choose the right option.

```python
def ask(question, answer):
    # Query model directly with full question
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question + " reply only with the option. for ex: D"}
        ]
    )
    return response.choices[0].message.content.strip() == answer
```

### Perspective-Taking Pipeline

A more sophisticated approach that mimics human ToM reasoning by breaking it down into steps:

1. **Character Identification**: Identify the main character in the story
2. **Perspective Filtering**: Determine what information the character has access to
3. **Question Answering**: Answer based on the character's knowledge state

This multi-stage approach often results in better performance on complex ToM tasks.

## Datasets

### Standard ToM Benchmark
- **Source**: ToMBench_release_v1_0618.xlsx
- **Tests**: False belief, scalar implicature, emotion recognition, etc.
- **Format**: Stories with multiple-choice questions

### Custom Evolving Stories Dataset
- **Source**: evolving_stories_250.xlsx
- **Format**: Scenarios with questions and multiple-choice options

### Multi-Interaction Dataset
- **Source**: multi_interaction_100.xlsx
- **Format**: Scenarios involving multiple character interactions

## Usage

### Basic Testing

```python
# Load dataset
file_path = '/path/to/your/dataset.xlsx'
excel_data = pd.ExcelFile(file_path)
df = pd.read_excel(excel_data, sheet_name='Your Sheet Name')

# Set up model client
os.environ["YOUR_API_KEY"] = "your_api_key"
client = YourClientLibrary()

# Run tests
for question, answer in questions.items():
    test_result = ask(question, answer)
    # Process results
```

### Switching Models

To test different models, modify the client initialization and API calls accordingly:

```python
# For OpenAI models
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(model="gpt-4o", ...)

# For Google's Gemini
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(...)

# For Meta's Llama (via ollama)
import ollama
response = ollama.chat(model='llama3', messages=[...])

# For Anthropic's Claude
from anthropic import Anthropic
client = Anthropic()
response = client.messages.create(model="claude-3-opus-20240229", ...)
```

## Results Analysis

After running tests, the framework calculates and outputs:
- Total questions tested
- Number of correct answers
- Accuracy percentage

Example output:
```
Total questions: 100
Correct answers: 78
Accuracy: 78.00%
```

## Customization

### Testing Different Tasks

To test on different ToM tasks:
1. Switch the file path to your desired dataset
2. Adjust column references to match your data structure
3. Modify prompts if needed for specific task types

### Adding New Testing Methods

The framework is designed to be extensible. New testing methodologies can be added by implementing additional functions for different approaches to ToM reasoning.

## Requirements

- Python 3.8+
- pandas
- Relevant API client libraries (openai, anthropic, etc.)
- Access to LLM APIs
