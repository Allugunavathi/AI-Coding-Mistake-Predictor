import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

import pickle

# Load dataset
data = pd.read_csv("../dataset/coding_errors.csv")

# Input and Output
X = data["code"]
y = data["error_type"]

# Convert text into numbers
vectorizer = CountVectorizer()

X_vector = vectorizer.fit_transform(X)

# Train AI Model
model = MultinomialNB()

model.fit(X_vector, y)

# Save Model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("AI Model Trained Successfully!")