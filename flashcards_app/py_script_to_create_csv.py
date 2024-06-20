import csv

# Define the data you want to include in the CSV
cards_data = [
    {"question": "What is the capital of France?", "answer": "Paris", "deck_id": 1, "tags": "geography;capitals"},
    {"question": "What is the largest planet in our solar system?", "answer": "Jupiter", "deck_id": 2,
     "tags": "astronomy;planets"},
    # Add more cards here
    {"question": "What is the speed of light?", "answer": "299,792,458 meters per second", "deck_id": 3,
     "tags": "physics;constants"},
    {"question": "Who wrote 'To Kill a Mockingbird'?", "answer": "Harper Lee", "deck_id": 4,
     "tags": "literature;authors"},
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
