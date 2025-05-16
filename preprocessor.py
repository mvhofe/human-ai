import nltk
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are available (download_resources.py should have been run)
# nltk.download('punkt', quiet=True)
# nltk.download('averaged_perceptron_tagger', quiet=True)
# nltk.download('wordnet', quiet=True)
# nltk.download('omw-1.4', quiet=True) # For WordNet

class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def _get_wordnet_pos(self, treebank_tag):
        """Converts treebank POS tags to WordNet POS tags."""
        if treebank_tag.startswith('J'):
            return nltk.corpus.wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return nltk.corpus.wordnet.VERB
        elif treebank_tag.startswith('N'):
            return nltk.corpus.wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return nltk.corpus.wordnet.ADV
        else:
            return nltk.corpus.wordnet.NOUN # Default to noun

    def preprocess_text(self, text: str) -> list[list[tuple[str, str, str]]]:
        """
        Preprocesses the input text.
        Returns a list of sentences, where each sentence is a list of (token, POS_tag, lemma) tuples.
        """
        if not isinstance(text, str):
            raise ValueError("Input text must be a string.")
        if not text.strip():
            return [] # Return empty list for empty or whitespace-only input

        sentences = nltk.sent_tokenize(text)
        processed_sentences = []

        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            pos_tags = nltk.pos_tag(tokens)
            
            sentence_data = []
            for token, tag in pos_tags:
                wordnet_pos = self._get_wordnet_pos(tag)
                lemma = self.lemmatizer.lemmatize(token, pos=wordnet_pos)
                sentence_data.append((token, tag, lemma))
            processed_sentences.append(sentence_data)
            
        return processed_sentences

if __name__ == '__main__':
    # Example Usage
    preprocessor = TextPreprocessor()
    sample_text = "This is an example sentence. AI models are running quickly and generating texts. The texts look good."
    
    print(f"Original Text:\n{sample_text}\n")
    
    processed_output = preprocessor.preprocess_text(sample_text)
    
    print("Processed Output (List of sentences, each with (token, POS, lemma) tuples):\n")
    for i, sentence in enumerate(processed_output):
        print(f"Sentence {i+1}:")
        for token_data in sentence:
            print(f"  {token_data}")
        print("---")

    # Test with empty input
    try:
        print("\nTesting with empty input:")
        empty_processed = preprocessor.preprocess_text("  ")
        print(f"Processed empty input: {empty_processed}")
    except ValueError as e:
        print(f"Error with empty input: {e}")

    # Test with non-string input
    try:
        print("\nTesting with non-string input:")
        preprocessor.preprocess_text(123)
    except ValueError as e:
        print(f"Error with non-string input: {e}")

