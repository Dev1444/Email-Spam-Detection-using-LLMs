import requests
import json
import pandas as pd
import sqlite3

# Path to the downloaded dataset
DATASET_PATH = 'path_to_your_downloaded_dataset/spam_or_not_spam.csv'

# LMStudio API endpoint
API_URL = 'http://localhost:1234/api/classify'

# Load the dataset
df = pd.read_csv(DATASET_PATH)

# Function to classify email using LMStudio API
def classify_email(email_text):
    payload = {'text': email_text}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(API_URL, data=json.dumps(payload), headers=headers)
    return response.json()

# Classify emails and store results
results = []
for _, row in df.iterrows():
    email_text = row['email']  # Update with the actual column name in your dataset
    result = classify_email(email_text)
    results.append({'email': email_text, 'classification': result['label']})

# Save results to a JSON file
with open('classification_results.json', 'w') as f:
    json.dump(results, f, indent=4)

# Save results to an SQLite database
def save_to_database(results):
    # Connect to SQLite database
    conn = sqlite3.connect('classification_results.db')
    c = conn.cursor()

    # Create table
    c.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY,
        email TEXT,
        classification TEXT
    )
    ''')

    # Insert data
    for result in results:
        c.execute('INSERT INTO results (email, classification) VALUES (?, ?)', 
                  (result['email'], result['classification']))

    # Commit and close
    conn.commit()
    conn.close()

# Save the results to the database
save_to_database(results)

print("Classification complete. Results saved to 'classification_results.json' and 'classification_results.db'.")
