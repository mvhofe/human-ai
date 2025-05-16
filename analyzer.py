import nltk
from nltk.probability import FreqDist
from nltk.util import ngrams
from collections import Counter

# Assuming preprocessor.py is in the same directory and NLTK resources are downloaded
# from preprocessor import TextPreprocessor # This will be used when integrating

class AICharacteristicAnalyzer:
    def __init__(self, preprocessed_sentences: list[list[tuple[str, str, str]]]):
        """
        Initializes the analyzer with preprocessed text data.
        preprocessed_sentences: A list of sentences, where each sentence is a list of (token, POS_tag, lemma) tuples.
        """
        self.processed_sentences = preprocessed_sentences
        self.all_tokens = [token_data[0].lower() for sentence in self.processed_sentences for token_data in sentence]
        self.all_lemmas = [token_data[2].lower() for sentence in self.processed_sentences for token_data in sentence]
        self.text_as_string = " ".join(self.all_tokens)

    def calculate_lexical_diversity(self) -> float:
        """Calculates lexical diversity using Type-Token Ratio (TTR)."""
        if not self.all_lemmas:
            return 0.0
        return len(set(self.all_lemmas)) / len(self.all_lemmas) if len(self.all_lemmas) > 0 else 0

    def get_word_frequency(self, top_n: int = 10) -> list[tuple[str, int]]:
        """Returns the most frequent words (lemmas)."""
        if not self.all_lemmas:
            return []
        freq_dist = FreqDist(self.all_lemmas)
        return freq_dist.most_common(top_n)

    def detect_repetitions(self, n: int = 3, min_freq: int = 2) -> dict[str, int]:
        """
        Detects repeated n-grams (phrases).
        n: The size of the n-gram (e.g., 2 for bigrams, 3 for trigrams).
        min_freq: Minimum frequency for an n-gram to be considered repetitive.
        Returns a dictionary of repeated n-grams and their counts.
        """
        if not self.all_tokens or len(self.all_tokens) < n:
            return {}
        
        n_grams_list = list(ngrams(self.all_tokens, n))
        if not n_grams_list:
            return {}
            
        n_gram_counts = Counter(n_grams_list)
        
        repeated_phrases = {}
        for phrase_tuple, count in n_gram_counts.items():
            if count >= min_freq:
                repeated_phrases[" ".join(phrase_tuple)] = count
        return repeated_phrases

    def analyze_sentence_length_variability(self) -> tuple[float, float, list[int]]:
        """
        Analyzes sentence length and its variability.
        Returns: (average_sentence_length, std_dev_sentence_length, list_of_sentence_lengths)
        """
        if not self.processed_sentences:
            return 0.0, 0.0, []

        sentence_lengths = [len(sentence) for sentence in self.processed_sentences]
        if not sentence_lengths:
             return 0.0, 0.0, []

        avg_len = sum(sentence_lengths) / len(sentence_lengths)
        
        if len(sentence_lengths) > 1:
            variance = sum([(length - avg_len) ** 2 for length in sentence_lengths]) / (len(sentence_lengths) -1) # sample variance
            std_dev = variance ** 0.5
        else:
            std_dev = 0.0 # Cannot calculate std dev for a single sentence
            
        return avg_len, std_dev, sentence_lengths

    def count_passive_voice_sentences(self) -> tuple[int, int]:
        """
        A heuristic to count potential passive voice constructions.
        Looks for patterns like "be + past participle (VBN)".
        Returns: (count_of_potential_passive_sentences, total_sentences)
        Note: This is a simplified heuristic and may not be perfectly accurate.
        """
        passive_count = 0
        total_sentences = len(self.processed_sentences)
        if total_sentences == 0:
            return 0, 0

        be_forms = ["is", "am", "are", "was", "were", "be", "being", "been"]

        for sentence_data in self.processed_sentences:
            tokens = [td[0].lower() for td in sentence_data]
            pos_tags = [td[1] for td in sentence_data]
            lemmas = [td[2].lower() for td in sentence_data]

            for i in range(len(lemmas) - 1):
                # Check for a form of "to be" followed by a past participle (VBN)
                # Or a modal + be + VBN
                if lemmas[i] in be_forms and pos_tags[i+1] == "VBN":
                    passive_count += 1
                    break # Count sentence once
                # Heuristic for modals: modal (MD) + "be" + VBN
                if i < len(lemmas) - 2 and pos_tags[i] == "MD" and lemmas[i+1] == "be" and pos_tags[i+2] == "VBN":
                    passive_count += 1
                    break # Count sentence once
        return passive_count, total_sentences

    def run_all_analyses(self) -> dict:
        """Runs all implemented analysis methods and returns a summary dictionary."""
        analyses = {
            "lexical_diversity_ttr": self.calculate_lexical_diversity(),
            "most_frequent_words_top10": self.get_word_frequency(top_n=10),
            "repeated_trigrams_min2_freq": self.detect_repetitions(n=3, min_freq=2),
            "repeated_bigrams_min2_freq": self.detect_repetitions(n=2, min_freq=2),
            "sentence_length_analysis": self.analyze_sentence_length_variability(),
            "passive_voice_heuristic_count": self.count_passive_voice_sentences()
        }
        return analyses

# Example Usage (requires preprocessor.py and its output format)
if __name__ == '__main__':
    # This example assumes you have a TextPreprocessor class available
    # and can generate the `processed_output` as shown in preprocessor.py
    
    # Mocking preprocessor output for standalone testing
    sample_text_for_preproc = "This is an example sentence. This is another example. AI models are running quickly. They are generating texts. The texts look good. The texts are good. It is said that this is good."
    # Simulate preprocessor output structure:
    # [ [(token, POS, lemma), ...], [(token, POS, lemma), ...] ]
    
    # Manual mock of preprocessed_sentences for demonstration
    # In a real scenario, this would come from preprocessor.preprocess_text(sample_text_for_preproc)
    mock_processed_sentences = [
        [("This", "DT", "this"), ("is", "VBZ", "be"), ("an", "DT", "an"), ("example", "NN", "example"), ("sentence", "NN", "sentence"), (".", ".", ".")],
        [("This", "DT", "this"), ("is", "VBZ", "be"), ("another", "DT", "another"), ("example", "NN", "example"), (".", ".", ".")],
        [("AI", "NNP", "ai"), ("models", "NNS", "model"), ("are", "VBP", "be"), ("running", "VBG", "run"), ("quickly", "RB", "quickly"), (".", ".", ".")],
        [("They", "PRP", "they"), ("are", "VBP", "be"), ("generating", "VBG", "generate"), ("texts", "NNS", "text"), (".", ".", ".")],
        [("The", "DT", "the"), ("texts", "NNS", "text"), ("look", "VBP", "look"), ("good", "JJ", "good"), (".", ".", ".")],
        [("The", "DT", "the"), ("texts", "NNS", "text"), ("are", "VBP", "be"), ("good", "JJ", "good"), (".", ".", ".")],
        [("It", "PRP", "it"), ("is", "VBZ", "be"), ("said", "VBN", "say"), ("that", "IN", "that"), ("this", "DT", "this"), ("is", "VBZ", "be"), ("good", "JJ", "good"), (".", ".", ".")]
    ]

    print(f"Analyzing mock preprocessed text (derived from: \n{sample_text_for_preproc}\n)")
    analyzer = AICharacteristicAnalyzer(mock_processed_sentences)
    analysis_results = analyzer.run_all_analyses()

    print("\nAnalysis Results:")
    for key, value in analysis_results.items():
        print(f"  {key}: {value}")

    # Example of how to use with the actual preprocessor (if in the same directory)
    # from preprocessor import TextPreprocessor
    # preprocessor_instance = TextPreprocessor()
    # actual_processed_data = preprocessor_instance.preprocess_text(sample_text_for_preproc)
    # if actual_processed_data:
    #     analyzer_with_actual_preproc = AICharacteristicAnalyzer(actual_processed_data)
    #     actual_results = analyzer_with_actual_preproc.run_all_analyses()
    #     print("\n--- Actual Preprocessor Results ---")
    #     for key, value in actual_results.items():
    #         print(f"  {key}: {value}")
    # else:
    #     print("\n--- Actual Preprocessor produced no output ---")

