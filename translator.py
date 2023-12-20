import json
from language_codes import language_codes
from googletrans import Translator
from sys import exit

FILE_NAME = input("JSON file path with file name: ")

SOURCE_LANG = ""
DEST_LANG = ""

source_lang_input = input("Source language: ")

if source_lang_input.lower() in language_codes:
    SOURCE_LANG = source_lang_input
else:
    print("ERROR: Source language not available")
    exit()

dest_lang_input = input("Destinated language: ")

if dest_lang_input.lower() in language_codes:
    DEST_LANG = dest_lang_input
else:
    print("ERROR: Destinated language not available")
    exit()


translator = Translator()

marked_words = []

marked_words_translated = []

global json_object
try:
    with open(FILE_NAME, "r") as json_file:
        try:
            json_object = json.load(json_file)
        except:
            print("ERROR: Provided file is false or file extension is not json.")
            exit()
except:
    print("ERROR: Could not open file/ file path. Check if the provided path is right and if the file exists.")
    exit()

highlights = json_object["highlights"]

for entry in highlights:
    try:
        marked_words.append(entry["text"].lower().lstrip("to").rstrip("’´,.;:_?!$%&/()[]{}+*#").strip("’´,.;:_?!$%&/()[]{}+*#"))
    except:
        print("ERROR: Json file does not correspond to the json schema.")
        exit()

print()

print("Translating words...")
print()

vocabs = []
vocabs_translated = []
counter = 0
for index in range(len(marked_words)):
    try:
        translated_word = translator.translate(marked_words[index], dest=DEST_LANG, src=SOURCE_LANG)
        marked_words_translated.append(translated_word.text)
        vocabs.append(marked_words[index])
        vocabs_translated.append(translated_word.text)

    except: 
        print()
        print(f"Could not translate the word: {marked_words[index]}")
        print()
        counter += 1
    if index % 5 == 0:
            print(f"Progress: {index}/{len(marked_words)}")

print("Translating done!")
trans_perc = (counter / len(marked_words)) * 100
print(f"No translation for {round(trans_perc, 0)}% of the words provided.")
print()
