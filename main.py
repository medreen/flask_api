from flask import Flask, jsonify, request

app = Flask(__name__)

allowed_methods = ["GET", "POST", "PUT", "PATCH", "UPDATE", "DELETE"]
users_list = [

]

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
            return jsonify({"data": users_list}), 200
        elif method == "post":
            data = request.get_json()
            if data["name"] == "" or data["location"] == "":
                return jsonify({"message": "name and location fields required."}), 403
            else:
                users_list.append(data)
                return jsonify({"message": "Successfully added users"}), 201
        else:
            return jsonify({"message": "Methods not allowed."}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500    


app.run(debug=True)
