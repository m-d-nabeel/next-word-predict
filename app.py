from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import joblib

app = Flask(__name__)

model = load_model("predict_next_words.keras")

tokenizer = joblib.load("tokenizer")

max_length = 71


def predict_next_words(input_text: str):

    words = input_text.split(" ")
    if len(words) > 4:
        input_text = " ".join(words[:-4])
        
    token_list = tokenizer.texts_to_sequences([input_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_length + 1, padding="pre")

    predicted_token = model.predict(token_list)
    predicted_token = np.argsort(predicted_token[0])[-3:]
    predicted_words = []
    for token in predicted_token:
        predicted_words.append(tokenizer.index_word[token])
    return predicted_words[::-1]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    input_text = data["input_text"]
    predictions = predict_next_words(input_text)
    return jsonify(predictions)


if __name__ == "__main__":
    app.run(debug=True)
