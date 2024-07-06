import json
import mysql.connector
import tkinter as tk
from tkinter import messagebox
from difflib import get_close_matches

# Load dictionary data from JSON file
data = json.load(open('/Users/sambhavjain/Desktop/Codes/py_miniProjects/mini_projects_in_py/1. An Interactive Dictionary/data.json'))

# Function to lookup word in dictionary data
def translate(word):
    word = word.lower()
    if word in data:
        return data[word]
    elif word.title() in data:
        return data[word.title()]
    elif word.upper() in data:
        return data[word.upper()]
    elif len(get_close_matches(word, data.keys())) > 0:
        yn = messagebox.askquestion("Word Not Found", f"Did you mean {get_close_matches(word, data.keys())[0]} instead?")
        if yn == 'yes':
            return data[get_close_matches(word, data.keys())[0]]
        else:
            return "The word doesn't exist. Please double check it."
    else:
        return 'Word not in Dictionary'

# Function to write dictionary data to MySQL database
def writeData():
    try:
        # Establish connection to MySQL database
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="new_password",
            database="diction"
        )
        cursor = db.cursor()

        with open('word-meanings.sql', 'w') as sql_file:
            for word, definitions in data.items():
                for definition in definitions:
                    try:
                        # Replace single quotes with double quotes to avoid SQL syntax issues
                        definition = definition.replace("'", "")
                        # Construct SQL INSERT statement
                        sql = f"INSERT INTO dictionary (word, definitions) VALUES ('{word}', '{definition}')"
                        # Execute SQL statement
                        cursor.execute(sql)
                        # Commit the transaction
                        db.commit()
                    except mysql.connector.Error as e:
                        print(f"Error writing {word}: {e}")
                        db.rollback()  # Rollback in case of error

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    finally:
        # Close database connection
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()
    
    print("SQL file created successfully.")

# Function to handle button click (search and display meaning)
def on_submit():
    word = entry_word.get()
    result = translate(word)
    if isinstance(result, list):
        meaning_text.config(text='\n'.join(result))
    else:
        meaning_text.config(text=result)

# Create Tkinter GUI window
root = tk.Tk()
root.title("Interactive Dictionary")

# Widgets
label_word = tk.Label(root, text="Enter a word:")
label_word.pack(pady=10)

entry_word = tk.Entry(root, width=30)
entry_word.pack()

btn_search = tk.Button(root, text="Search", command=on_submit)
btn_search.pack(pady=10)

meaning_text = tk.Label(root, text="", wraplength=400, justify='left')
meaning_text.pack(pady=20)

# Execute Tkinter main loop
root.mainloop()
