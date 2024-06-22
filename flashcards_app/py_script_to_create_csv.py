import csv

# Define the data you want to include in the CSV
cards_data = ([
    {"question": "Arbitrary", "answer": "Based on random choice or personal whim, rather than any reason or system.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Comprehensive", "answer": "Complete and including everything that is necessary.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Facilitate", "answer": "To make an action or process easy or easier.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Intrinsic", "answer": "Belonging naturally; essential.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Redundant", "answer": "Not or no longer needed or useful; superfluous.", "deck_id": 1, "tags": "vocabulary;intermediate"}
])


# Define the CSV file name
csv_file_name = "flashcards.csv"

# Create and write to the CSV file
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["question", "answer", "deck_id", "tags"])

    # Write the card data
    for card in cards_data:
        writer.writerow([card["question"], card["answer"], card["deck_id"], card["tags"]])

print(f"CSV file '{csv_file_name}' created successfully.")
