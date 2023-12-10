import genanki
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

for index in range(len(vocabs)):
    card = genanki.Note(
        model=CARD_MODEL,
        fields= [
            vocabs[index], # front
            f"{vocabs_translated[index]}" # back
        ]
    )

    deck.add_note(card)

for index in range(len(vocabs)):
    card = genanki.Note(
        model=CARD_MODEL,
        fields= [
            f"{vocabs_translated[index]}", # back
            vocabs[index] # back 
        ]
    )

    deck.add_note(card)

print()

print("Done! Check the current directory for any 'apkg' file with the chosen deck name.")

genanki.Package(deck).write_to_file(f"{DECK_NAME}.apkg")
