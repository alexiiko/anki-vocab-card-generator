import json
from googletrans import Translator

FILE_NAME = "highlights.json"
SOURCE_LANG = "en"
DEST_LANG = "de"

translator = Translator()

vocabs = []

translated_words_list = []

global object_
with open(FILE_NAME, "r") as json_file:
    object_ = json.load(json_file)

highlights = object_["highlights"]

for entry in highlights:
    vocabs.append(entry["text"].strip("!.,:;"))

for index in range(len(vocabs)):
    try:
        translated_word = translator.translate(vocabs[index], dest=DEST_LANG, src=SOURCE_LANG)
        translated_words_list.append(translated_word.text)
    except: 
        print(f"Failed the translation for the word: {vocabs[index]}")
