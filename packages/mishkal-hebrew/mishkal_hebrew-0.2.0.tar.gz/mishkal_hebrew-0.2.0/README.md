# Mishkal

Grapheme to phoneme in Hebrew

Convert Hebrew text into IPA for TTS systems and learning.

## Features

- (WIP) Accurate lightweight niqqud model
- Expand dates into text with niqqud
- Expand numbers into text with niqqud
- (WIP) Mixed English in Hebrew
- Dictionaries with words, symbols, emojies
- Convert text with niqqud to modern spoken phonemes

## Limitiation

The following hard to predict even from text with niqqud.

- Shva nah and nah
- Stress (Atmaha / Milre / Milra. same thing.)
- Kamatz Katan

## Install
```console
pip install mishkal-hebrew
```

## Play

See [Phonemize with Hebrew Space](https://huggingface.co/spaces/thewh1teagle/phonemize-in-hebrew)

## Examples
```python
from mishkal import phonemize
phonemes = phonemize('שָׁלוֹם עוֹלָם') 
print(phonemes) # ʃalom ?olam
```

See [examples](examples)
