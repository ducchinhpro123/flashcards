# Flashcard

## Introduction

This flashcard app helps memorize keywords, and its body is easy to use. It is beneficial for memorizing vocabulary. The
idea for this project came from [Anki](https://apps.ankiweb.net/).
It supports uploading CSV files to add flashcards quickly.

## Backend

- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
    - Models, Views, Templates
    - Django Admin
    - Form handling and validation
    - User authentication

### Frontend

- **HTML/CSS**: Standard technologies for creating and styling the user interface.
- **JavaScript/JQuery**: Used for enhancing interactivity and user experience.
- **Bootstrap**: A popular CSS framework for responsive, mobile-first front-end web development.
- **CKEditor 5**: A rich text editor used for the 'answer' field in the flashcards.

### Database

- **MySQL**: Used to handle data storage for user accounts, decks, cards, and tags.

## CSV File Handling

This application supports bulk uploading of flashcards using Comma-Separated Values (CSV) files.

### CSV File Structure

The CSV file should be structured as follows:

- Each row represents a flashcard.
- Each column represents a field of the flashcard.

Here's an example of how your CSV file should look:

![Flashcard csv](2024-06-20 16-00-28.png)

### Important Note

When uploading a CSV file, it is assumed that the user is aware of the `deck_id` associated with each flashcard.

## Setup and Installation

### Prerequisites

- Python 3.x
- Django

### Installation
> Note: the instructions below made for Linux-based systems.
1. Clone the repository:
   ```bash
   git clone https://github.com/ducchinhpro123/flashcards.git
   cd flashcards
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
    pip install -r requirements.txt
    ```
4. Run the server:

    ```bash
    python manage.py runserver
    ```
   