import json
from language_codes import language_codes
from googletrans import Translator
from sys import exit
import time


def add_marked_words_to_array():
    for entry in highlights:
        try:
            marked_words.append(entry["text"].lower().lstrip("to").strip("’´,.;:_?!$%&/()[]{}+*#"))
        except:
            print("ERROR: Json file does not correspond to the json schema.")
            exit()


def create_translated_array():
    print("Translating words...")
    start_time = time.time()

    counter = 0

    index = 0
    while index < len(marked_words):
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

        index += 1 

    print("Translation done!")
    trans_perc = (counter / len(marked_words)) * 100
    print(f"No translation for {round(trans_perc, 0)}% of the words provided.")

    print()

    end_time = time.time()
    print(f"Finished translating words in {round(end_time - start_time, 0)} seconds")

    print()


def generate_json_object() -> list:
    try:
        with open(FILE_NAME, "r") as json_file:
            try:
                json_object = json.load(json_file)
                return json_object["highlights"]
            except:
                print("ERROR: Provided file is false or file extension is not json.")
                exit()
    except:
        print("ERROR: Could not open file/ file path. Check if the provided path is right and if the file exists.")
        exit()


def translate_words():
    add_marked_words_to_array()
    create_translated_array()


# initiate every variable
FILE_NAME = input("JSON file path with file name: ")
highlights = generate_json_object()

SOURCE_LANG = ""
DEST_LANG = ""

source_lang_input = input("Source language: ")

# check if the language is available
if source_lang_input.lower() in language_codes:
    SOURCE_LANG = source_lang_input
else:
    print("ERROR: Source language not available")
    exit()

dest_lang_input = input("Destinated language: ")

# check if the language is available
if dest_lang_input.lower() in language_codes:
    DEST_LANG = dest_lang_input
else:
    print("ERROR: Destinated language not available")
    exit()

DECK_NAME = input("Deck name: ")


translator = Translator()

marked_words = []

marked_words_translated = []

vocabs = []

vocabs_translated = []


translate_words()
