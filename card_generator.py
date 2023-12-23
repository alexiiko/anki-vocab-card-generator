import genanki
import requests
import time
from random import randint
from translator import *
from concurrent.futures import ThreadPoolExecutor

def generate_study_cards_worker(args):
    index, vocabs, translated_vocabs, card_model, deck, definition_counter, example_counter = args

    dict_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{vocabs[index]}"
    data = requests.get(dict_url).json()

    definition = ""
    example = ""

    try:
        definition = data[0]["meanings"][0]["definitions"][0]["definition"]
    except:
        definition = ""
        print(f"No definition provided for the word: {vocabs[index]}")
        print()
        definition_counter += 1

    try:
        example = data[0]["meanings"][0]["definitions"][0]["example"]
    except:
        example = ""
        print(f"No example provided for the word: {vocabs[index]}")
        print()
        example_counter += 1

    card_back = f"{vocabs[index]}"

    if not definition == "":
        card_back += f" <br> <br> Definition: {definition}"
    if not example == "":
        card_back += f" <br> <br> Example: {example}"

    card = genanki.Note(
        model=card_model,
        fields=[
            f"{translated_vocabs[index]}",  # front
            card_back  # back
        ]
    )
    deck.add_note(card)

    if index % 5 == 0:
        print(f"Progress: {index}/{len(vocabs)}")
        print()

    return definition_counter, example_counter


def generate_study_cards(card_model, deck):
    definition_counter = 0
    example_counter = 0

    start_time = time.time()

    thread_args = [(i, vocabs, translated_vocabs, card_model, deck, definition_counter, example_counter) for i in range(len(vocabs))]

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(generate_study_cards_worker, thread_args)

    for result in results:
        num1, num2 = result
        definition_counter += num1 
        example_counter += num2

    end_time = time.time()
    print()
    print(f"Finished generating the cards words in {round(end_time - start_time, 0)} seconds")

    print()
    examples_percent = (example_counter / len(vocabs)) * 100
    definitions_percent = (definition_counter / len(vocabs)) * 100

    print(f"No definition provided for {round(definitions_percent, 0)}% of the words.")
    print(f"No example provided for {round(examples_percent, 0)}% of the words.")
    print()


def main():
    print()

    print("Generating cards...")

    CARD_MODEL = genanki.Model(
      1485830179,
      'Basic (and reversed card) (genanki)',
      fields=[
        {
          'name': 'Front',
          'font': 'Arial',
        },
        {
          'name': 'Back',
          'font': 'Arial',
        },
      ],
      templates=[
        {
          'name': 'Card 1',
          'qfmt': '{{Front}}',
          'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}',
        },
        {
          'name': 'Card 2',
          'qfmt': '{{Back}}',
          'afmt': '{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}',
        },
      ],
      css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
    )

    deck = genanki.Deck(
        randint(0, 99999),
        DECK_NAME
    )

    generate_study_cards(CARD_MODEL, deck)

    print("Done! Check the current directory for any 'apkg' file with the chosen deck name.")

    genanki.Package(deck).write_to_file(f"{DECK_NAME}.apkg")

main()
