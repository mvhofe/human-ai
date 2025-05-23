# Text Humanizer Tool

## 1. Overview

This tool is designed to take English text that may have been generated by an AI and transform its phrasing to sound more natural and characteristic of human writing. It analyzes the input text for common AI-generated patterns (e.g., overly formal language, repetition, predictable vocabulary) and applies a series of transformations to mitigate these characteristics.

## 2. Project Structure

```
/humanizer_tool
|-- download_resources.py   # Script to download necessary NLTK resources
|-- preprocessor.py         # Module for text preprocessing (tokenization, POS tagging, lemmatization)
|-- analyzer.py             # Module to analyze text for AI-like characteristics
|-- transformer.py          # Module to apply transformations to the text
|-- humanizer.py            # Main script to run the full humanization pipeline
|-- README.md               # This file: setup and usage instructions
```

## 3. Setup

### a. Dependencies

The tool primarily uses Python and the NLTK (Natural Language Toolkit) library. Ensure you have Python 3.11+ installed.

To install NLTK:
```bash
pip install nltk
```

### b. NLTK Resources

The tool requires several NLTK data packages (e.g., for tokenization, POS tagging, WordNet). A script is provided to download these.

Navigate to the `humanizer_tool` directory and run:
```bash
python3.11 download_resources.py
```
This script will download and install all necessary NLTK resources into the default NLTK data path (usually `~/nltk_data/` on Linux).

## 4. Usage

The main script to use the tool is `humanizer.py`. You can run it directly to see example transformations on sample texts embedded within the script, or you can modify it to process your own text programmatically.

### a. Running the Example

To run the built-in examples:
```bash
cd /path/to/humanizer_tool
python3.11 humanizer.py
```
This will output the original text, analysis results, intermediate transformation steps (if print statements are enabled in `transformer.py`), and the final humanized text for several sample inputs.

### b. Integrating into Your Code

You can use the `TextHumanizer` class from `humanizer.py` in your own Python scripts:

```python
from humanizer import TextHumanizer

# Create an instance of the humanizer
humanizer_instance = TextHumanizer()

# Your AI-generated text
input_text = "The aforementioned paradigm shift necessitates a re-evaluation of existing frameworks. It is crucial for entities to adapt proactively."

# Humanize the text
# You can adjust the lexical_sub_rate (0.0 to 1.0, default 0.15) 
# and whether to apply_contractions (True/False, default True)
humanized_output, original_analysis = humanizer_instance.humanize_text(
    raw_text=input_text, 
    lexical_sub_rate=0.2, 
    apply_contractions=True
)

print("Original Text:")
print(input_text)
print("\nHumanized Text:")
print(humanized_output)
print("\nAnalysis of Original Text:")
for key, value in original_analysis.items():
    print(f"  {key}: {value}")

```

## 5. How it Works

1.  **Preprocessing (`preprocessor.py`):** The input text is tokenized into sentences and words. Each word is tagged with its part-of-speech (POS) and lemmatized (reduced to its base form).
2.  **Analysis (`analyzer.py`):** The preprocessed text is analyzed for characteristics often found in AI-generated content. This includes:
    *   Lexical diversity (variety of words used).
    *   Frequency of common words.
    *   Repetition of phrases (n-grams).
    *   Variability in sentence length.
    *   Heuristic-based detection of passive voice.
3.  **Transformation (`transformer.py`):** Based on the analysis (though current transformations are more general), the text undergoes several changes:
    *   **Lexical Substitution:** Some words are replaced with synonyms to increase vocabulary richness and reduce predictability. The rate of substitution can be controlled.
    *   **Contraction Introduction:** Common English contractions (e.g., "it is" to "it's") are introduced to make the text sound more natural and less formal.
    *   *(Future enhancements could include sentence restructuring, redundancy removal, and tone adjustments based more directly on the analyzer's output.)*
4.  **Reconstruction:** The transformed tokens are reassembled into sentences and then into a final text string.

## 6. Limitations

*   **Subjectivity:** What sounds "human" can be subjective. The tool aims for general improvements based on common linguistic patterns.
*   **Meaning Preservation:** While the tool tries to maintain the original meaning, complex transformations (especially synonym replacement) can sometimes lead to subtle shifts in meaning or nuance. Always review the output.
*   **Factuality:** The tool does *not* verify or alter the factual correctness of the input text. It only modifies the style and phrasing.
*   **Contextual Understanding:** The tool's understanding of deep context is limited. Transformations are primarily rule-based and statistical.
*   **Over-Correction:** It's possible for the tool to over-correct, making the text sound unnatural in a different way. Adjusting parameters like `lexical_sub_rate` can help.

## 7. Further Development Ideas

*   More sophisticated sentence restructuring algorithms.
*   Better integration of analysis results to guide transformations more precisely.
*   User-configurable style profiles (e.g., "formal human," "informal human").
*   Integration with larger language models for more nuanced rephrasing suggestions (used as a component, not as the primary generator).
*   A simple web interface for easier use.

