
# laonlp-enhanced

An enhanced tokenizer for the Lao language, built with a dictionary-based maximal matching approach and number handling. Integrates with `laonlp` for POS tagging.

## Reference
- [laonlp](Wannaphong Phatthiyaphaibun. (2022). LaoNLP: Lao language Natural Language Processing. Zenodo. https://doi.org/10.5281/zenodo.6833407)


## Installation
```bash
pip install laonlp-enhanced
```

## Usage
```python
from laonlp_enhanced import tokenize

text = "ສະບາຍດີ 245,394"
tokens = tokenize(text)
print(tokens)  # Output: ['ສະບາຍດີ', '245,394']
```

## POS Tagging with laonlp
Combine tokenization with POS tagging using the laonlp library:
```python
from laonlp_enhanced import tokenize, pos_tag

text = "ສະບາຍດີ 245,394"
tokens = tokenize(text)
tagged = pos_tag(tokens)
print(tagged)  # Output: [('ສະບາຍດີ', 'NOUN'), ('245,394', 'NUM')]
```

## License
Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.