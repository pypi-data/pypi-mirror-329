import re
from symspellpy import SymSpell, Verbosity
import os
import pkg_resources  # For loading files from the package

class LaoSpellChecker:
    def __init__(self, dictionary_path=None):
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2)

        # If dictionary path is not provided, use the bundled default file
        if dictionary_path is None:
            try:
                # Load dictionary from the package
                dictionary_path = pkg_resources.resource_filename(
                    __name__, 'lao_words_with_freq.txt'
                )
                # print(f"Dictionary file path: {dictionary_path}")
            except Exception as e:
                print(f"Error loading dictionary file: {e}")
                raise FileNotFoundError("Dictionary file not found!")

        # Check if the dictionary file exists
        if os.path.exists(dictionary_path):
            # print(f"Loading dictionary from: {dictionary_path}")
            self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
        else:
            raise FileNotFoundError(f"Dictionary file not found at {dictionary_path}!")

    def correct_word(self, word):
        # Get suggestions based on the word
        suggestions = self.sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        print(f"Suggestions for '{word}': {suggestions}")  # Debug print
        
        # If there are suggestions, return the closest one, else return the original word
        if suggestions:
            return suggestions[0].term
        else:
            return word

    def correct_sentence(self, sentence):
        # Split sentence into words, considering spaces and punctuation
        words = re.split(r'([^\u0E80-\u0EFF]+)', sentence)  # Split by non-Lao characters (space, punctuation)
        print(f"Words after split: {words}")  # Debug print
        
        corrected_words = []

        # Iterate through each word/punctuation
        for word in words:
            # Check if the word contains only Lao characters (ignore English alphabet and other characters)
            if re.match(r'^[\u0E80-\u0EFF]+$', word):  # This checks if the word contains only Lao characters
                corrected_words.append(self.correct_word(word))  # Correct the word
            else:
                # Skip any word containing English alphabets (or other non-Lao characters)
                print(f"Skipping word (contains non-Lao characters): {word}")
                continue  # Skip this word, do not append it
        
        # Reassemble the sentence from the corrected words
        corrected_sentence = ' '.join(corrected_words)
        return corrected_sentence