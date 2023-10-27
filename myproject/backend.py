from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import joblib 
import os
import csv

dt = joblib.load("./static/dt.joblib")

app = Flask(__name__)
CORS(app)

@app.route("/hola", methods = ["GET"])
def inicio():
    return "Hola mundo"

@app.route("/predict_json", methods=["POST"])
def predict_json():
    data = request.predict_json
    X = [
        float (data["pH"]),
        float (data["sulphates"]),
        float (data["alcohol"])
    ]
    y_pred = dt.predict(X)
    print(y_pred)
    return jsonify({"result": y_pred[0]})

@app.route("/predict_form", methods=["POST"])
def predict_form():
    data = request.form
    X = [
        float (data["pH"]),
        float (data["sulphates"]),
        float (data["alcohol"])
    ]
    y_pred = dt.predict(X)
    print(y_pred)
    return jsonify({"result": y_pred[0]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = False, port = 8081)
    
@app.route("/predict_file", methods = ["POST"])
def predict_file():
    files = request.files["archivo"]
    filename = secure_filename(file.filename)
    #file.save(f"./static/{filename}")
    path = os.path.join(os.getcwd(),"static", filename)
    file.save(path)
    with open(path,"r") as f:
        reader = csv.DictReader(f)
        X = [[float(row[0]), float(row[1]),float(row[2])]]
        y_pred = dt.predict(X)
        return jsonify({
            "results": [{"key": f"{k}",
                         "results": f"{v}"} for k, v in enumerate(y_pred)]
        })
    
    
    