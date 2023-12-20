import genanki
import requests
from random import randint
from translator import vocabs, vocabs_translated


DECK_NAME = input("Deck name: ")

print()

print("Generating cards...")

CARD_MODEL = genanki.Model(
    randint(0,99999),
    "Simple Model",
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
    ],
      templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
    ]
)

deck = genanki.Deck(
    randint(0,99999),
    DECK_NAME
)

print()

def_counter = 0
ex_counter = 0
for index in range(len(vocabs)):
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
        def_counter += 1

    try:
        example = data[0]["meanings"][0]["definitions"][0]["example"]
    except:
        example = ""
        print(f"No example provided for the word: {vocabs[index]}")
        print()
        ex_counter += 1 

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

    card = genanki.Note(
        model=CARD_MODEL,
        fields= [
            card_back, # front
            f"{vocabs_translated[index]}" # back
        ]
    )

    deck.add_note(card)

    if index % 5 == 0:
        print(f"Progress: {index}/{len(vocabs)}")
        print()

print()
ex_perc = (ex_counter / len(vocabs)) * 100
def_perc = (def_counter / len(vocabs)) * 100

print(f"No translation provided for {round(def_perc, 0)}% of the words.")
print(f"No example provided for {round(ex_perc, 0)}% of the words.")

print()

print("Done! Check the current directory for any 'apkg' file with the chosen deck name.")

genanki.Package(deck).write_to_file(f"{DECK_NAME}.apkg")
