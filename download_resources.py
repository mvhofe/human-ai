import nltk

def download_nltk_resources():
    resources_to_download = {
        "punkt": "tokenizers/punkt",
        "averaged_perceptron_tagger": "taggers/averaged_perceptron_tagger", # Main tagger package
        "wordnet": "corpora/wordnet",
        "omw-1.4": "corpora/omw-1.4"
    }

    print("Ensuring standard NLTK resources are downloaded...")
    for resource_name, resource_path in resources_to_download.items():
        try:
            nltk.data.find(resource_path)
            print(f"Resource 	'{resource_name}'	 already available.")
        except LookupError:
            print(f"Resource 	'{resource_name}'	 not found. Downloading...")
            try:
                nltk.download(resource_name, quiet=False)
                print(f"Resource 	'{resource_name}'	 downloaded successfully.")
            except Exception as e:
                print(f"Failed to download resource 	'{resource_name}'	. Error: {e}")

    # Address specific language model needs if errors arise
    # The 'punkt_tab' and 'averaged_perceptron_tagger_eng' errors suggest specific sub-components
    # or language models within the main packages might not be fully resolved by the generic download.

    print("\nAttempting to resolve specific NLTK component dependencies...")
    specific_components = ["punkt", "punkt_tab", "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"]
    
    for component_name in specific_components:
        print(f"Checking/Downloading specific component: 	'{component_name}'	...")
        try:
            # Forcing download for 'punkt' and 'averaged_perceptron_tagger' can help ensure completeness
            if component_name in ["punkt", "averaged_perceptron_tagger"]:
                 nltk.download(component_name, quiet=False, force=True)
            else:
                nltk.download(component_name, quiet=False)
            print(f"Component 	'{component_name}'	 check/download attempted successfully.")
        except ValueError as ve: # nltk.download raises ValueError for unknown package
            print(f"Component 	'{component_name}'	 is not a recognized NLTK package name for direct download: {ve}")
            print(f"This often means 	'{component_name}'	 refers to internal data within a main package (e.g., 'punkt' or 'averaged_perceptron_tagger').")
            print("Ensuring the main package is fully downloaded is the standard way to resolve this.")
        except Exception as e:
            print(f"Error downloading component 	'{component_name}'	: {e}")

if __name__ == "__main__":
    print("Starting NLTK resource download process (attempt 4)...")
    download_nltk_resources()
    print("NLTK resource download process complete (attempt 4).")

