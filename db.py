from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here
class User(db.Model):
    """
    User Model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    laundry = db.relationship("Laundry", cascade = "delete",)

    def __init__(self, **kwargs):
        """
        Initialize Course object/entry
        """
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")

    
    def serialize(self):
        """
        Serialize a course object 
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "laundry":[s.serialize() for s in self.laundry]

        }
    
    def sim_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }
 

    
class Laundry(db.Model):
    """
    Laundry Model
    """
    __tablename__ = "laundries"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    dorm_room = db.Column(db.String, nullable = False)
    laundry_number = db.Column(db.Integer, nullable = False)
    time = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, **kwargs):
        """
        Initialize Laundry object/entry
        """
        self.dorm_room = kwargs.get("dorm_room", "")
        self.laundry_number = kwargs.get("laundry_number", "")
        self.time = kwargs.get("time", "")
        self.user_id = kwargs.get("user_id")

    def serialize(self):
        """
        Serialize a assignment object 
        """
        return {
            "id": self.id,
            "dorm_room": self.dorm_room,
            "laundry_number": self.laundry_number,
            "time": self.time,
            "user": User.query.filter_by(id=self.user_id).first().sim_serialize()
        }
    