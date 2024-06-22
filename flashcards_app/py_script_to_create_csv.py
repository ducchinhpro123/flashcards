import csv

# Define the data you want to include in the CSV
cards_data = [
    {"question": "Elicit", "answer": "To draw out a response or reaction from someone.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Ambiguous", "answer": "Open to more than one interpretation; having a double meaning.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Convey", "answer": "To communicate or make known.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Diminish", "answer": "To make or become less.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Coherent", "answer": "Logical and consistent.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Scrutinize", "answer": "To examine or inspect closely and thoroughly.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Plausible", "answer": "Seeming reasonable or probable.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Inherent", "answer": "Existing in something as a permanent, essential, or characteristic attribute.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Mitigate", "answer": "To make less severe, serious, or painful.", "deck_id": 1, "tags": "vocabulary;intermediate"},
    {"question": "Conundrum", "answer": "A confusing and difficult problem or question.", "deck_id": 1, "tags": "vocabulary;intermediate"}
]

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
