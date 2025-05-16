from preprocessor import TextPreprocessor
from analyzer import AICharacteristicAnalyzer
from transformer import TransformationEngine

class TextHumanizer:
    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def humanize_text(self, raw_text: str, lexical_sub_rate: float = 0.15, apply_contractions: bool = True) -> tuple[str, dict]:
        """
        Processes raw text through the full humanization pipeline.
        Returns the humanized text and the analysis results of the original text.
        """
        if not isinstance(raw_text, str) or not raw_text.strip():
            print("Input text is empty or invalid.")
            return raw_text, {}

        print(f"Original Text for Humanization:\n{raw_text}\n")

        # 1. Preprocess the text
        print("Step 1: Preprocessing text...")
        preprocessed_sentences = self.preprocessor.preprocess_text(raw_text)
        if not preprocessed_sentences:
            print("Preprocessing resulted in no sentences. Returning original text.")
            return raw_text, {}
        # print(f"Preprocessed data: {preprocessed_sentences}") # For debugging

        # 2. Analyze the preprocessed text (original characteristics)
        print("\nStep 2: Analyzing original text characteristics...")
        analyzer = AICharacteristicAnalyzer(preprocessed_sentences)
        original_analysis_results = analyzer.run_all_analyses()
        print("Original Analysis Results:")
        for key, value in original_analysis_results.items():
            print(f"  {key}: {value}")

        # 3. Transform the text
        print("\nStep 3: Applying transformations...")
        # The transformer will use the same preprocessed_sentences that the analyzer used for its initial state.
        transformer = TransformationEngine(preprocessed_sentences, original_analysis_results) # Pass original analysis for context if needed by transformer
        
        # The humanize method in the transformer applies changes and prints intermediate steps
        humanized_text_output = transformer.humanize(
            lexical_sub_rate=lexical_sub_rate, 
            apply_contractions=apply_contractions
        )
        
        print(f"\nHumanization Complete.")
        return humanized_text_output, original_analysis_results

if __name__ == "__main__":
    humanizer_tool = TextHumanizer()

    sample_ai_text_1 = "The utilization of advanced computational paradigms facilitates the optimization of resource allocation. It is imperative that organizational stakeholders strategically leverage emergent technological solutions to enhance operational efficiencies. The aforementioned methodologies are anticipated to yield substantial performance improvements."
    
    sample_ai_text_2 = "This document provides an overview of the current situation. The situation is complex. We must consider all factors. The factors are numerous. The solution will require careful planning. Planning is essential for success."

    sample_ai_text_3 = "It is a fact that the Earth is round. The moon orbits the Earth. Many stars are visible in the night sky. These are simple truths."

    print("--- Test Case 1 ---")
    humanized_1, analysis_1 = humanizer_tool.humanize_text(sample_ai_text_1, lexical_sub_rate=0.2)
    print(f"\nFinal Humanized Text 1:\n{humanized_1}")
    # print(f"\nOriginal Analysis for Text 1:\n{analysis_1}")

    print("\n\n--- Test Case 2 ---")
    humanized_2, analysis_2 = humanizer_tool.humanize_text(sample_ai_text_2, lexical_sub_rate=0.25, apply_contractions=True)
    print(f"\nFinal Humanized Text 2:\n{humanized_2}")
    # print(f"\nOriginal Analysis for Text 2:\n{analysis_2}")

    print("\n\n--- Test Case 3 ---")
    humanized_3, analysis_3 = humanizer_tool.humanize_text(sample_ai_text_3, lexical_sub_rate=0.1, apply_contractions=True)
    print(f"\nFinal Humanized Text 3:\n{humanized_3}")
    # print(f"\nOriginal Analysis for Text 3:\n{analysis_3}")

    # Example of a very short text
    sample_short_text = "AI is good."
    print("\n\n--- Test Case 4 (Short Text) ---")
    humanized_4, analysis_4 = humanizer_tool.humanize_text(sample_short_text, lexical_sub_rate=0.3, apply_contractions=True)
    print(f"\nFinal Humanized Text 4:\n{humanized_4}")

