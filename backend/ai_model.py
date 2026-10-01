import pickle

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_error(code):

    code_vector = vectorizer.transform([code])

    prediction = model.predict(code_vector)

    return prediction[0]