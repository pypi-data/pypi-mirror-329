from symspellpy import SymSpell, Verbosity
import os

class LaoSpellChecker:
    def __init__(self, dictionary_path=None):
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2)
        if dictionary_path is None:
            dictionary_path = os.path.join(os.path.dirname(__file__), "lao_words.txt")
        if os.path.exists(dictionary_path):
            self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
        else:
            raise FileNotFoundError("Dictionary file not found!")

    def correct_word(self, word):
        suggestions = self.sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        return suggestions[0].term if suggestions else word

# Example usage
if __name__ == "__main__":
    spell_checker = LaoSpellChecker("laonlp_spellchecker/lao_words.txt")
    print(spell_checker.correct_word("ປະເທດລາສ"))  # Example misspelled word
