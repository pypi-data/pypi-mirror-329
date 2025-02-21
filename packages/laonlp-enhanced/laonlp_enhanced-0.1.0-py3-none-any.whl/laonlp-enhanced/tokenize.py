import os
from transformers import PreTrainedTokenizerFast

class LaoTokenizer:
    def __init__(self, dictionary, stopwords=None):
        self.dictionary = dictionary
        self.stopwords = stopwords or set()
    
    def tokenize(self, text, remove_stopwords=False):
        if not text:
            return []
        
        tokens = []
        i = 0
        while i < len(text):
            if text[i].isdigit():
                num_start = i
                while i < len(text) and text[i].isdigit():
                    i += 1
                number = text[num_start:i]
                if not (remove_stopwords and number in self.stopwords):
                    tokens.append(number)
                continue
            
            longest_match = None
            for j in range(len(text), i, -1):
                candidate = text[i:j]
                if candidate in self.dictionary:
                    longest_match = candidate
                    break
            if longest_match:
                if not (remove_stopwords and longest_match in self.stopwords):
                    tokens.append(longest_match)
                i += len(longest_match)
            else:
                tokens.append(text[i])
                i += 1
        return tokens

class LaoEnhancedTokenizer:
    def __init__(self):
        base_path = os.path.dirname(__file__)
        self.hf_tokenizer = PreTrainedTokenizerFast(tokenizer_file=os.path.join(base_path, "lao_tokenizer.json"))
        with open(os.path.join(base_path, 'dictionary.txt'), 'r', encoding='utf-8') as f:
            dictionary = set(line.strip() for line in f if line.strip())
        with open(os.path.join(base_path, 'stopwords.txt'), 'r', encoding='utf-8') as f:
            stopwords = set(line.strip() for line in f if line.strip())
        self.lao_tokenizer = LaoTokenizer(dictionary, stopwords)
    
    def tokenize(self, text, remove_stopwords=False):
        return self.lao_tokenizer.tokenize(text, remove_stopwords)

def tokenize(text, remove_stopwords=False):
    tokenizer = LaoEnhancedTokenizer()
    return tokenizer.tokenize(text, remove_stopwords)