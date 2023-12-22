import genanki
import requests
from random import randint
from translator import vocabs, vocabs_translated, DECK_NAME
import time


def generate_study_cards():
    definition_counter = 0
    example_counter = 0

    print("Started timer")
    start_time = time.time()

    index = 0
    while index < len(vocabs):
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

        card_back = ""
        if example == "":
            card_back = f"{vocabs[index]} <br> <br> Definition: {definition}" 
        elif definition == "":
            card_back = f"{vocabs[index]} <br> <br> Example: {example}"
        elif definition == "" and example == "":
            card_back = f"{vocabs[index]}"
        else:
            card_back = f"{vocabs[index]} <br> <br> Definition: {definition} <br> <br> Example: {example}"

        card = genanki.Note(
            model=CARD_MODEL,
            fields= [
                f"{vocabs_translated[index]}",# front
                card_back # back
            ]
        )
        deck.add_note(card)

        if index % 5 == 0:
            print(f"Progress: {index}/{len(vocabs)}")
            print()

        index += 1

    end_time = time.time()
    print()
    print(f"Finished translating words in {end_time - start_time} seconds")
    
    print()
    examples_percent = (example_counter / len(vocabs)) * 100
    definitions_percent = (definition_counter / len(vocabs)) * 100

    print(f"No definition provided for {round(definitions_percent, 0)}% of the words.")
    print(f"No example provided for {round(examples_percent, 0)}% of the words.")

    print()


print()

print("Generating cards...")

# initiate model and deck
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
    randint(0,99999),
    DECK_NAME
)

generate_study_cards()

# program done
print("Done! Check the current directory for any 'apkg' file with the chosen deck name.")

genanki.Package(deck).write_to_file(f"{DECK_NAME}.apkg")
