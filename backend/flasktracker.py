from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS # type: ignore

from dotenv import load_dotenv # type: ignore
import os
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

CORS(app)

db: SQLAlchemy = SQLAlchemy(app)

@app.route("/api/test")
def test():
  data = {'name': 'John', 'age': 30, 'city': 'New York'}
  return jsonify(data), 200

if __name__ == "__main__":
  app.run(debug=True)