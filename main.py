from flask import Flask, request, jsonify
from database import Base, Budget, User 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['JWT_SECRET_KEY'] = 'medreen3435!'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

DATABASE_URL = "postgresql://postgres:Colesprouse2311!@localhost:5432/budgets"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()

allowed_methods = ['POST', 'GET', 'PUT', 'DELETE','PATCH']

@app.route('/register', methods=allowed_methods)
def register():
    try:
        if request.method == "POST":            
            data = request.get_json()

            if data:
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')           
            else:
                return jsonify({"message": "Request body is empty"}), 400
            
            if username == '' or password == '' or email=='':
                return jsonify({"error": "All fields required!"}), 400
            else:
                email = email.lower()
                # validate the user
                existing_user = db_session.query(User).filter_by(email=email).first()
                if existing_user:
                    return jsonify({"error": "User already exists"}), 409

                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                new_user = User(
                    username=username,
                    email=email,
                    password=hashed_password,
                    created_at=datetime.utcnow()
                )

                db_session.add(new_user)
                db_session.commit()

                token = create_access_token(identity=new_user.email)

                return jsonify({
                    "message": "User registered successfully!",
                    "token": token
                }), 201
        else: 
            return jsonify({"message": "Method not allowed"})

    except Exception as e:        
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=allowed_methods)
def login():
    try:
        if request.method == "POST":            
            data = request.get_json()

            if data:               
                email = data.get('email')
                password = data.get('password')           
            else:
                return jsonify({"message": "Request body is empty"}), 400
            
            if password == '' or email == '':
                return jsonify({"error": "All fields required!"}), 400
            else:
                 email = email.lower()
                 user = db_session.query(User).filter_by(email=email).first()

                 if user and bcrypt.check_password_hash(user.password, password):        
                    token = create_access_token(identity=new_user.email)

                    return jsonify({
                        "message": "Login successful!",
                        "token": token
                    }), 201
        else: 
            return jsonify({"message": "Method not allowed"})

    except Exception as e:        
        return jsonify({"error": str(e)}), 500

@app.route('/budget', methods=allowed_methods)
@jwt_required()
def budget():
    try:
        if request.method == "POST":            
            print("JWT identity:", get_jwt_identity())

            current_email = get_jwt_identity()
        
            if current_email:                  
                data = request.get_json()
            else: 
                return jsonify({"error": "Unauthorized User"}), 401
                
            if data: 
                title = data.get("title")              
                amount = data.get('amount')
                date = data.get('date')   
                
            else:
                return jsonify({"message": "Request body is empty"}), 400

            if title == '' or amount == '' or date == '':
                return jsonify({"error": "All fields required!"}), 400    
            else:    
                try:
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                except:
                    return jsonify({"error": "Invalid date format"}), 400

                user = db_session.query(User).filter_by(username=current_username).first()

                new_budget = Budget(
                    title=title,
                    amount=float(amount),
                    date=date_obj,
                    user_id=user.id
                )

                db_session.add(new_budget)
                db_session.commit()
                db_session.close()

                return jsonify({"message": "Budget added"}), 201
           

        elif request.method == "GET":            
            current_email = get_jwt_identity()

            user = db_session.query(User).filter_by(email=current_email).first()

            budgets = db_session.query(Budget).filter_by(user_id=user.id).all()

            for b in budgets:
                return jsonify([                    
                    {
                        "id": b.id,
                        "title": b.title,
                        "amount": b.amount,
                        "date": b.date.strftime("%Y-%m-%d")
                    } 
                ])
        else:
            return jsonify({"message": "Method not allowed"}), 405

    except Exception as e:        
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)