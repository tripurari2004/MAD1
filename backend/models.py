from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #instance of SQLAlchemy

# Admin Model
class Admin_Info(db.Model):
    __tablename__ = "admin_info"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=False, default=0)


#Service Model
class Service_Info(db.Model):
    __tablename__ = "service_info"
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    professionals = db.relationship('Professional_Info', backref='service_info', lazy=True, cascade="all, delete")


#Professional Model
class Professional_Info(db.Model):
    __tablename__ = "professional_info"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    service_name = db.Column(db.String, db.ForeignKey('service_info.service'), nullable=True)
    experience =db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    mobile_number = db.Column(db.Integer, unique=True, nullable=False)
    document = db.Column(db.String(300), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=1)
    is_approved = db.Column(db.Integer, nullable=False, default=0)
    
    service = db.relationship("Service_Info", backref="professional_info", lazy=True, cascade="all, delete")
    
    
#Customer Model
class Customer_Info(db.Model):
    __tablename__ = "customer_info"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    mobile_number = db.Column(db.Integer, unique=True, nullable=False)
    role = db.Column(db.Integer, nullable=False, default=2)
    is_approved = db.Column(db.Boolean, nullable=False, default=True)


#Request Model
class Request_Info(db.Model):
    __tablename__ = "request_info"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer_info.id"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional_info.id"), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey("service_info.id"), nullable=False)
    date_of_request = db.Column(db.Date, nullable=False)
    date_of_completion = db.Column(db.Date, nullable=True)
    status = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer, nullable=True)
    
    service = db.relationship("Service_Info", backref="request_info", lazy="joined")
    customer = db.relationship("Customer_Info", backref="request_info")
    professional = db.relationship("Professional_Info", backref="request_info", lazy="joined")

