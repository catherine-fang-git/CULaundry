import json
from db import db
from flask import Flask, request
from db import Laundry, User

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# your routes here
@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/api/users/")
def get_users():
    """
    Enpoint for getting all users
    """
    return success_response({"users" : [t.serialize() for t in User.query.all()]})

@app.route("/api/users/", methods = ["POST"])
def create_user():
    """
    Enpoint for creating a new course
    """
    body = json.loads(request.data)
    name = body.get("name", None)
    netid = body.get("netid", None)
    if name is None:
        return failure_response("Invalid input: User's name not is provided", 400)
    if netid is None:
        return failure_response("Invalid input: User's netid not is provided", 400)
    new_user = User(
        name = name,
        netid = netid
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/laundry/", methods = ["POST"] )
def add_laundry_to_user(user_id):
    """
    Endpoint for creating a new assignment to a course
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    body = json.loads(request.data)
    dorm_room = body.get("dorm_room", None)
    laundry_number = body.get("laundry_number", None)
    time = body.get("time", None)

    if dorm_room is None:
        return failure_response("Invalid input: laundry dorm room not provided", 400)
    if laundry_number is None:
        return failure_response("Invalid input: laundry number not provided", 400)
    if time is None:
        return failure_response("Invalid input: laundry time not provided", 400)
    
    new_laundry = Laundry(
        dorm_room = dorm_room,
        laundry_number = laundry_number,
        time = time,
        user_id = user_id
    )
    db.session.add(new_laundry)
    db.session.commit()
    return success_response(new_laundry.serialize(), 201)


 





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
