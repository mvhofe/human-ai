import nltk
import random
from nltk.corpus import wordnet

# Assuming preprocessor.py and analyzer.py are in the same directory
# from preprocessor import TextPreprocessor
# from analyzer import AICharacteristicAnalyzer

class TransformationEngine:
    def __init__(self, preprocessed_sentences: list[list[tuple[str, str, str]]], analysis_results: dict):
        """
        Initializes the transformation engine with preprocessed text and analysis results.
        preprocessed_sentences: List of sentences, each a list of (token, POS_tag, lemma) tuples.
        analysis_results: Dictionary containing results from AICharacteristicAnalyzer.
        """
        self.processed_sentences = preprocessed_sentences
        self.analysis_results = analysis_results
        # NLTK resources (punkt, averaged_perceptron_tagger, wordnet, omw-1.4) should be downloaded.

    def _get_synonyms(self, word: str, pos_tag: str = None) -> list[str]:
        """Gets synonyms for a word, optionally filtered by POS tag."""
        synonyms = set()
        wordnet_pos = None
        if pos_tag:
            if pos_tag.startswith("N"): wordnet_pos = wordnet.NOUN
            elif pos_tag.startswith("V"): wordnet_pos = wordnet.VERB
            elif pos_tag.startswith("J"): wordnet_pos = wordnet.ADJ
            elif pos_tag.startswith("R"): wordnet_pos = wordnet.ADV
        
        for syn in wordnet.synsets(word, pos=wordnet_pos):
            for lemma in syn.lemmas():
                syn_word = lemma.name().replace("_", " ") # Replace underscores with spaces for multi-word synonyms
                if syn_word.lower() != word.lower(): # Exclude the original word
                    synonyms.add(syn_word)
        return list(synonyms)

    def lexical_substitution(self, substitution_rate: float = 0.1) -> list[list[tuple[str, str, str]]]:
        """
        Performs lexical substitution to increase vocabulary diversity.
        Replaces some words with their synonyms.
        substitution_rate: Approximate proportion of words to attempt to substitute.
        """
        transformed_sentences = []
        # Consider common words to target, or words identified as overused by the analyzer
        # For simplicity, we apply a general substitution rate here.
        
        # Words to generally avoid substituting (e.g., determiners, prepositions, very common verbs)
        # This list can be expanded.
        avoid_substituting_pos = ["DT", "IN", "CC", "TO", "PRP", "PRP$", ".", ",", ":"]
        # Also avoid substituting very common verbs like forms of "be", "have", "do" unless specifically targeted
        common_verbs_lemmas = ["be", "have", "do", "say", "get", "make", "go", "know", "take", "see", "come", "think", "look", "want", "give", "use", "find", "tell", "ask"]

        for sentence_data in self.processed_sentences:
            new_sentence = []
            for token, pos, lemma in sentence_data:
                if pos not in avoid_substituting_pos and lemma.lower() not in common_verbs_lemmas and random.random() < substitution_rate:
                    synonyms = self._get_synonyms(lemma, pos)
                    if synonyms:
                        chosen_synonym = random.choice(synonyms)
                        # Basic check to maintain case for proper nouns, otherwise lowercase for substituted word
                        # This is a simplification; more robust case handling might be needed.
                        if pos == "NNP" or pos == "NNPS":
                            # Attempt to capitalize first letter if it was a proper noun
                            # This is tricky for multi-word synonyms. For now, just use as is or capitalize first word.
                            new_token = chosen_synonym.split(" ")[0].capitalize() + (" " + " ".join(chosen_synonym.split(" ")[1:]) if len(chosen_synonym.split(" ")) > 1 else "")
                        else:
                            new_token = chosen_synonym.lower()
                        
                        # We are substituting the token, but the POS and lemma might change.
                        # For simplicity, we keep the original POS and use the new token as its own lemma here.
                        # A more advanced version would re-tag and re-lemmatize the new token.
                        new_sentence.append((new_token, pos, new_token.lower()))
                        continue
                new_sentence.append((token, pos, lemma))
            transformed_sentences.append(new_sentence)
        self.processed_sentences = transformed_sentences # Update internal state
        return transformed_sentences

    def introduce_contractions(self) -> list[list[tuple[str, str, str]]]:
        """Introduces common English contractions."""
        contraction_map = {
            ("is", "not"): "isn't", ("are", "not"): "aren't", ("was", "not"): "wasn't", ("were", "not"): "weren't",
            ("do", "not"): "don't", ("does", "not"): "doesn't", ("did", "not"): "didn't",
            ("have", "not"): "haven't", ("has", "not"): "hasn't", ("had", "not"): "hadn't",
            ("will", "not"): "won't", ("would", "not"): "wouldn't",
            ("can", "not"): "cannot", # or can't - choosing cannot for now as it's one word
            ("could", "not"): "couldn't", ("should", "not"): "shouldn't",
            ("i", "am"): "I'm", ("you", "are"): "you're", ("he", "is"): "he's", ("she", "is"): "she's",
            ("it", "is"): "it's", ("we", "are"): "we're", ("they", "are"): "they're",
            ("i", "have"): "I've", ("you", "have"): "you've", ("we", "have"): "we've", ("they", "have"): "they've",
            ("i", "will"): "I'll", ("you", "will"): "you'll", ("he", "will"): "he'll", ("she", "will"): "she'll",
            ("it", "will"): "it'll", ("we", "will"): "we'll", ("they", "will"): "they'll",
            ("i", "would"): "I'd", ("you", "would"): "you'd", ("he", "would"): "he'd", ("she", "would"): "she'd",
            ("we", "would"): "we'd", ("they", "would"): "they'd",
            ("let", "us"): "let's"
        }
        # More specific POS tags might be needed for accuracy (e.g. PRP for pronouns)

        transformed_sentences = []
        for sentence_data in self.processed_sentences:
            new_sentence_tokens = []
            i = 0
            while i < len(sentence_data):
                token1_data = sentence_data[i]
                token1_lower = token1_data[0].lower()
                
                if i + 1 < len(sentence_data):
                    token2_data = sentence_data[i+1]
                    token2_lower = token2_data[0].lower()
                    
                    if (token1_lower, token2_lower) in contraction_map:
                        contracted_form = contraction_map[(token1_lower, token2_lower)]
                        # Preserve case of the first token if it was capitalized (e.g., "I am" -> "I'm")
                        if token1_data[0][0].isupper() and contracted_form[0].islower() and contracted_form != "let's": # special case for let's
                            contracted_form = contracted_form[0].upper() + contracted_form[1:]
                        
                        # Simplified POS and lemma for the new contracted token
                        # A more robust approach would re-tag.
                        new_pos = token1_data[1] # Use POS of the first part as a heuristic
                        new_lemma = contracted_form.lower()
                        new_sentence_tokens.append((contracted_form, new_pos, new_lemma))
                        i += 2 # Skip the next token as it has been merged
                        continue
                new_sentence_tokens.append(token1_data)
                i += 1
            transformed_sentences.append(new_sentence_tokens)
        self.processed_sentences = transformed_sentences
        return transformed_sentences

    def reconstruct_text(self) -> str:
        """Reconstructs the text from the (potentially transformed) processed sentences."""
        output_sentences = []
        for sentence_data in self.processed_sentences:
            sentence_str = ""
            for i, (token, pos, lemma) in enumerate(sentence_data):
                if i > 0 and token not in [".", ",", "?", "!", ";", ":", "'s", "n't", "'m", "'re", "'ll", "'d", "'ve"] and sentence_str[-1] not in "(":
                    sentence_str += " " # Add space unless punctuation or specific contractions
                sentence_str += token
            output_sentences.append(sentence_str)
        return " ".join(output_sentences)

    def humanize(self, lexical_sub_rate=0.15, apply_contractions=True) -> str:
        """Applies a sequence of transformations to humanize the text."""
        print("Original (for transformation engine input):")
        print(self.reconstruct_text())

        if lexical_sub_rate > 0:
            print(f"\nApplying lexical substitution (rate: {lexical_sub_rate})...")
            self.lexical_substitution(substitution_rate=lexical_sub_rate)
            print("After lexical substitution:")
            print(self.reconstruct_text())

        if apply_contractions:
            print("\nApplying contraction introduction...")
            self.introduce_contractions()
            print("After introducing contractions:")
            print(self.reconstruct_text())
        
        # Future transformations (sentence restructuring, redundancy reduction) would go here.
        
        print("\nFinal humanized text:")
        final_text = self.reconstruct_text()
        print(final_text)
        return final_text

# Example Usage (requires preprocessor.py and analyzer.py for full pipeline)
if __name__ == '__main__':
    # Mocking preprocessor and analyzer outputs for standalone testing of Transformer
    mock_processed_sentences_for_transformer = [
        [("It", "PRP", "it"), ("is", "VBZ", "be"), ("a", "DT", "a"), ("truth", "NN", "truth"), ("universally", "RB", "universally"), ("acknowledged", "VBN", "acknowledge"), (".", ".", ".")],
        [("A", "DT", "a"), ("single", "JJ", "single"), ("man", "NN", "man"), ("in", "IN", "in"), ("possession", "NN", "possession"), ("of", "IN", "of"), ("a", "DT", "a"), ("good", "JJ", "good"), ("fortune", "NN", "fortune"), ("must", "MD", "must"), ("be", "VB", "be"), ("in", "IN", "in"), ("want", "NN", "want"), ("of", "IN", "of"), ("a", "DT", "a"), ("wife", "NN", "wife"), (".", ".", ".")],
        [("I", "PRP", "i"), ("will", "MD", "will"), ("not", "RB", "not"), ("do", "VB", "do"), ("that", "DT", "that"), (".", ".", ".")],
        [("They", "PRP", "they"), ("are", "VBP", "be"), ("very", "RB", "very"), ("happy", "JJ", "happy"), (".", ".", ".")]
    ]
    mock_analysis_results_for_transformer = {
        "lexical_diversity_ttr": 0.6,
        "most_frequent_words_top10": [("a", 3), (".", 3)],
        # ... other analysis data ...
    }

    print("Initializing Transformer Engine with mock data...\n")
    transformer = TransformationEngine(mock_processed_sentences_for_transformer, mock_analysis_results_for_transformer)
    
    humanized_text = transformer.humanize(lexical_sub_rate=0.2, apply_contractions=True)
    
    print(f"\n--- End of Transformer Example ---")

    # A more complex example to test contractions and substitutions
    mock_complex_sentences = [
        [("This", "DT", "this"), ("is", "VBZ", "be"), ("a", "DT", "a"), ("test", "NN", "test"), (".", ".", ".")],
        [("AI", "NNP", "ai"), ("is", "VBZ", "be"), ("not", "RB", "not"), ("always", "RB", "always"), ("perfect", "JJ", "perfect"), (".", ".", ".")],
        [("You", "PRP", "you"), ("are", "VBP", "be"), ("going", "VBG", "go"), ("to", "TO", "to"), ("see", "VB", "see"), ("it", "PRP", "it"), (".", ".", ".")],
        [("She", "PRP", "she"), ("will", "MD", "will"), ("have", "VB", "have"), ("to", "TO", "to"), ("make", "VB", "make"), ("a", "DT", "a"), ("decision", "NN", "decision"), (".", ".", ".")]
    ]
    print("\nInitializing Transformer Engine with complex mock data...\n")
    transformer_complex = TransformationEngine(mock_complex_sentences, mock_analysis_results_for_transformer)
    humanized_complex_text = transformer_complex.humanize(lexical_sub_rate=0.25, apply_contractions=True)
    print(f"\n--- End of Complex Transformer Example ---")

