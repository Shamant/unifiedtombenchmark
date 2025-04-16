# UniToMBench: A Unified Benchmark for Theory of Mind in Large Language Models

## Overview

**UniToMBench** is a unified evaluation framework for assessing the **Theory of Mind (ToM)** capabilities of large language models (LLMs). ToM refers to the ability to attribute mental states—beliefs, intents, desires, emotions, and knowledge—to oneself and others, and to reason about perspectives that differ from one's own.

This repository provides code, datasets, and evaluation methodologies that integrate the strengths of prior benchmarks (SimToM, ToMBench) to test LLMs across diverse and cognitively demanding ToM scenarios.

## Features

- Evaluate LLMs on standard and custom ToM benchmarks
- Support for multiple evaluation methodologies:
  - Direct question answering
  - Multi-stage perspective-taking pipelines
- Flexible integration with various LLM APIs (OpenAI, Google, Meta, Anthropic, etc.)
- Easily customizable for new datasets and experimental formats

## Testing Methodologies

### Direct Question Answering

A baseline approach that queries the model with the full story and question, testing for the correct multiple-choice response.

```python
def ask(question, answer):
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

A structured pipeline that decomposes ToM reasoning into the following stages:

1. **Character Identification** – Identify the main actor in the scenario
2. **Perspective Filtering** – Infer what knowledge the character possesses
3. **Contextual Answering** – Select the correct response based on that perspective

This pipeline mirrors how humans approach ToM tasks and improves model accuracy on complex scenarios.

## Datasets

### 1. Standard ToM Benchmark

- **Source**: `ToMBench_release_v1_0618.xlsx`
- **Tasks**: False belief, emotion recognition, scalar implicature, and more
- **Format**: Narrative-based MCQ questions

### 2. Custom Evolving Stories Dataset

- **Source**: `evolving_stories_250.xlsx`
- **Format**: Progressively unfolding narratives with character-based MCQs

### 3. Multi-Interaction Dataset

- **Source**: `multi_interaction_100.xlsx`
- **Format**: Scenarios involving multi-turn dialogues and perspective shifts

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

Adjust the client configuration to use different LLMs:

```python
# OpenAI
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(model="gpt-4o", ...)

# Google Gemini
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(...)

# Meta Llama via Ollama
import ollama
response = ollama.chat(model='llama3', messages=[...])

# Anthropic Claude
from anthropic import Anthropic
client = Anthropic()
response = client.messages.create(model="claude-3-opus-20240229", ...)
```

## Results Analysis

The evaluation script computes:

- Total number of questions tested
- Number of correct responses
- Overall accuracy

Example output:

```
Total questions: 100
Correct answers: 78
Accuracy: 78.00%
```

## Customization

### Testing Different Tasks

To test different datasets or task types:

1. Change the dataset file path
2. Update column references (e.g., question, answer, options)
3. Modify prompts or reasoning steps as needed

### Extending Evaluation Strategies

You can add new testing pipelines or models by creating additional functions that define:

- Input formatting logic
- Model interaction pattern
- Evaluation and parsing criteria

## Requirements

- Python 3.8+
- `pandas`
- Model client libraries:
  - `openai`
  - `anthropic`
  - `google-generativeai`
  - `ollama` (or any wrapper for LLaMA models)
- API keys for respective LLMs

## Citation

If you use UniToMBench in your research, please cite:

```
@misc{unito2025,
  title={UniToMBench: A Unified Benchmark for Advancing Theory of Mind in Large Language Models},
    author={Shamant},
  year={2025},
  note={In Submission}
}
```

---

