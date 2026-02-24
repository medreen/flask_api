from flask import Flask, jsonify, request
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database import Base, User

app = Flask(__name__)

DATABASE_URL = "postgresql+psycopg2://postgres:Colesprouse2311!@localhost:5432/flask_api"
engine = create_engine(DATABASE_URL, echo=False)

session = sessionmaker(bind=engine)
my_session = session()

Base.metadata.create_all(engine)

allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]


@app.route("/", methods = allowed_methods)
def home():
    method = request.method.lower()
    if method == "get":
        return jsonify({"Flask API Version" : "1.0"}),200
    else:
        return jsonify({"message": "Method not allowed"}),405
    
@app.route("/users", methods = allowed_methods)
def users():
    try:
        method = request.method.lower()
        if method == "get":
            users_list = []
            query = select(User)
            my_users = list(my_session.scalars(query).all())

            for user in my_users:
                users_list.append({"id": user.id,
                                    "name": user.name,
                                    "location": user.location})

            return jsonify({"data": users_list}), 200
        elif method == "post":
            data = request.get_json()
            if data["name"] == "" or data["location"] == "":
                return jsonify({"message": "name and location fields required."}), 403
            else:
                #users_list.append(data)                                
                new_user = User(name = data["name"], location = data["location"])
                my_session.add(new_user)
                my_session.commit()
                return jsonify({"message": "Successfully added users"}), 201
        else:
            return jsonify({"message": "Methods not allowed."}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500    


app.run(debug=True)
