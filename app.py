from flask import Flask, request, jsonify
from pymongo import MongoClient, ReadPreference, WriteConcern

app = Flask(__name__)
client = MongoClient("mongodb+srv://sanikasandeep03_db_user:YMHmBesa2OoeuPbD@cluster0.hdbbfru.mongodb.net/?appName=Cluster0")
db = client["ev_db"]
col = db["vehicles"]

@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    doc = request.json
    result = col.with_options(write_concern=WriteConcern(w=1)).insert_one(doc)
    return jsonify({"inserted_id": str(result.inserted_id)})

@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    doc = request.json
    result = col.with_options(write_concern=WriteConcern(w="majority")).insert_one(doc)
    return jsonify({"inserted_id": str(result.inserted_id)})

@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    count = col.with_options(read_preference=ReadPreference.PRIMARY).count_documents({"Make": "TESLA"})
    return jsonify({"count": count})

@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    count = col.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED).count_documents({"Make": "BMW"})
    return jsonify({"count": count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
