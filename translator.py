import json
import time
from language_codes import language_codes
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor
from sys import exit


def add_marked_words_to_array():
    FILE_NAME = input("JSON file path with file name: ")
    highlights = generate_json_object(FILE_NAME)
    marked_words = []
    for entry in highlights:
        try:
            marked_words.append(entry["text"].lower().lstrip("to").strip("’´,.;:_?!$%&/()[]{}+*#"))
        except:
            print("ERROR: Json file does not correspond to the json schema.")
            exit()

    return marked_words


def create_translated_array_worker(args):
    marked_word, dest_lang, source_lang, progress_callback = args
    translator = Translator()

    try:
        translated_word = translator.translate(marked_word, dest=dest_lang, src=source_lang)
        progress_callback(marked_word)
        return marked_word, translated_word.text
    except:
        print()
        print(f"Could not translate the word: {marked_word}")
        print()
        return None


def create_translated_array(dest_lang: str, source_lang: str, marked_words: list):
    vocabs = []
    vocabs_translated = []

    def progress_callback(word):
        nonlocal translation_counter
        nonlocal index

        translation_counter += 1
        index += 1

        if index % 5 == 0:
            print(f"Progress: {index}/{len(marked_words)}")

    print()
    print("Translating words...")
    start_time = time.time()

    translation_counter = 0
    index = 0
    thread_args = [(word, dest_lang, source_lang, progress_callback) for word in marked_words]

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(create_translated_array_worker, thread_args)

    for result in results:
        if result:
            marked_word, translated_word = result
            vocabs.append(marked_word)
            vocabs_translated.append(translated_word)
        else:
            translation_counter += 1

    print("Translation done!")
    trans_perc = (translation_counter / len(marked_words)) * 100
    print(f"No translation for {round(trans_perc, 0)}% of the words provided.")
    print()

    end_time = time.time()
    print(f"Finished translating words in {round(end_time - start_time, 0)} seconds")
    print()

    return vocabs, vocabs_translated


def generate_json_object(file_name) -> list:
    try:
        with open(file_name, "r") as json_file:
            try:
                json_object = json.load(json_file)
                return json_object["highlights"]
            except:
                print("ERROR: Provided file is false or file extension is not json.")
                exit()
    except:
        print("ERROR: Could not open file/ file path. Check if the provided path is right and if the file exists.")
        exit()


def create_langs():
    dest_lang_input = input("Destination language: ")
    source_lang_input = input("Source language: ")

    if source_lang_input.lower() in language_codes and dest_lang_input.lower() in language_codes:
        return dest_lang_input, source_lang_input
    else:
        print("ERROR: Source or destination language not available")
        exit()


marked_words_list = add_marked_words_to_array()
DEST_LANG, SOURCE_LANG = create_langs()
DECK_NAME = input("Deck name: ")

vocabs, translated_vocabs = create_translated_array(DEST_LANG, SOURCE_LANG, marked_words_list)

