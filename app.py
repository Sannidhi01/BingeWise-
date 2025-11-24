from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from ml_model import recommend_similar

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend")
def recommend():
    try:
        movie = request.args.get("movie")
        return jsonify(recommend_similar(movie))
    except Exception as e:
        return jsonify({"error": str(e), "source": "error", "recs": []}), 500

if __name__ == "__main__":
    app.run(debug=True,use_reloader=True)





