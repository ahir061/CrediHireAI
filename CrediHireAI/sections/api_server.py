def start_api_server(vectorizer, model):
    from flask import Flask, request, jsonify
    app = Flask(__name__)

    @app.route('/predict', methods=['POST'])
    def predict_api():
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "Missing 'text' field"}), 400
        text_vectorized = vectorizer.transform([text.lower()])
        prob = model.predict_proba(text_vectorized)[0, 1]
        prediction = int(prob > 0.5)
        return jsonify({
            "probability": round(float(prob), 4),
            "prediction": prediction,
            "label": "Fraud" if prediction else "Genuine"
        })

    app.run(debug=True)
