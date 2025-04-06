import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load the dataset
data = pd.read_csv('Youtube-Spam-Dataset.csv')

# Keep only the relevant columns: 'CONTENT' and 'CLASS'
data = data[['CONTENT', 'CLASS']]

# Optional: clean the text (lowercase, remove punctuation, etc.)
data['CONTENT'] = data['CONTENT'].str.lower().str.replace(r'[^a-z\s]', '', regex=True)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(data['CONTENT'], data['CLASS'], test_size=0.2, random_state=42)

# Vectorize the text data
vectorizer = TfidfVectorizer(stop_words='english')
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Train a classifier (e.g., Logistic Regression)
model = LogisticRegression()
model.fit(X_train_vect, y_train)

# Predict and evaluate
y_pred = model.predict(X_test_vect)
print(classification_report(y_test, y_pred))

# Test the model
test_sentence = 'Check out my items'
test_sentence_vect = vectorizer.transform([test_sentence])
prediction = model.predict(test_sentence_vect)[0]
result = "SPAM" if prediction == 1 else "NOT SPAM"
print(f"Test Sentence: {test_sentence}")
print(f"Prediction: {result} (class {prediction})")

import joblib
import os

# Create models directory if it doesn't exist
folder_name = 'is_spam_models'
os.makedirs(folder_name, exist_ok=True)

# Save the model in the models folder
joblib.dump(model, f'{folder_name}/spam_model.joblib')
joblib.dump(vectorizer, f'{folder_name}/spam_vectorizer.joblib')

print(f"Model and vectorizer saved in the {folder_name} folder")
