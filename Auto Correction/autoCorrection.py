import difflib

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def get_words(self, node=None, current_prefix='', words=None):
        if node is None:
            node = self.root
        if words is None:
            words = []
        if node.is_end_of_word:
            words.append(current_prefix)
        for char, child_node in node.children.items():
            self.get_words(child_node, current_prefix + char, words)
        return words
    
def suggest_corrections(word, trie, threshold=0.15):
    suggestions = []
    trie_words = trie.get_words()
    close_matches = difflib.get_close_matches(word, trie_words, n=5, cutoff=threshold)

    for match in close_matches:
        suggestions.append(match)

    return set(suggestions)

def main():
    trie = Trie()

    with open("dictionary.txt", "r") as file:
        trie_words = [line.strip() for line in file]

    for word in trie_words:
        trie.insert(word)

    user_input = input("my_word = ")
    if user_input.isalpha():
        if trie.search(user_input):
            print(f"'{user_input}' is a valid word.")
        else:
            suggestions = suggest_corrections(user_input, trie)
            if suggestions:
                print(f"Did you mean: {suggestions} ?")
            else:
                print(f"No suggestions found for '{user_input}'.")
    else:
        print("Only alphabetic input is accepted.")

if __name__ == "__main__":
    main()
