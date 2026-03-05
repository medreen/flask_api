import select

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, db

app = Flask(__name__)

alloweed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]

DATABASE_URL = "postgresql+psycopg2://postgres:Colesprouse2311!@localhost:5432/vue_myduka"

# Connect to the database using sqlalchemy
engine = create_engine(DATABASE_URL, echo=True)

# Create a session to call query methods
session = sessionmaker(bind=engine)
my_session = session()

# Create the tables in the database
db.metadata.create_all(engine)




@app.route("/", methods=alloweed_methods)
def home():
    if request.method == "GET":
        msg = { "Flask API Version" : "1.0" }
        return jsonify(msg), 200
    else:
        return jsonify({"error": "Method not allowed"}), 405


@app.route("/user")
def user():
    if request.method.upper() == "GET":
        # return a list of all users in the database
        query = select(User)
        users = my_session.scalars(query).all()
        data = []

        for user in users:
            data.append({
                "id": user.id,
                "name": user.name,
                "location": user.location
            })
        return jsonify({ "data": data })
    elif request.method.upper() == "POST":
        data = request.get_json()
        if data["Name"] == "" or data["Location"] == "":
            return jsonify({ "error": "Name and Location cannot be empty" }), 400
        else:
            new_user = User(name=data["Name"], location=data["Location"])
            my_session.add(new_user)
            my_session.commit()
            return jsonify({ "message": f"User created successfully{data['name']}" }), 201
    
app.run(debug=True)