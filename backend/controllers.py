#import important modules and libraries
from flask import render_template, request, jsonify, session, redirect, url_for, flash, json
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from flask import current_app as app
from  backend.models import *

#allowed extension
ALLOWED_EXTENSIONS = {'pdf', 'doc'}

#file extension checker function
def allowed_file(filename):
    return( "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS)


#home route
@app.route("/")
def home():
    return render_template("index.html")


#login route
@app.route("/login",methods = ["GET","POST"])
def login():
    """login functionality for admin, professional, customer"""
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
        role=request.form.get("login_type")
        
        user=None
        if role == "0":
            user=Admin_Info.query.filter_by(email=email, password=password).first()
        elif role == "1":
            user=Professional_Info.query.filter_by(email=email, password=password).first()
        elif role == "2":
            user=Customer_Info.query.filter_by(email=email, password=password).first()
            
        if user:
            session["user_id"] = user.id
            session["role"] = role
            if role=="0":
                flash("Login Successfully","success")
                return redirect(url_for("admin_dashboard"))
            elif role=="1":
                if user.is_approved==0:
                    return render_template("login.html",msg="Your account is not approved yet. Please wait for admin approval")
                elif user.is_approved==1:
                    flash("Login Successfully","success")
                    return redirect(url_for("professional_dashboard"))
                return render_template("login.html", msg="Your account has been blocked by the admin due to a violation of our policies")
            elif role=="2":
                if user.is_approved:
                    flash("Login Successfully","success")
                    return redirect(url_for("customer_dashboard"))
                return render_template("login.html", msg="Your account has been blocked by the admin due to a violation of our policies")
        else:
            return render_template("login.html",msg="* Incorrect Credentials. Verify your email and password.")
    return render_template("login.html",msg="")


#logout route
@app.route("/logout")
def logout():
    session.clear()
    flash("logout successfully", "success")
    return redirect(url_for("home"))


#seesion info function
def current_user():
    user_id = session.get("user_id")
    role = session.get("role")
    if not user_id or not role:
        return None
    if role == "0":
        return Admin_Info.query.get(user_id)
    elif role == "1":
        return Professional_Info.query.get(user_id)
    elif role == "2":
        return Customer_Info.query.get(user_id)


#admin dashboard route
@app.route("/admin_dashboard")
def admin_dashboard():
    user = current_user()
    if not user or session.get("role") != "0":
        return redirect(url_for("login"))
    service_summary = fetch_services()
    professional_summary = fetch_professional()
    customer_summary = fetch_customer()
    return render_template("adminDashboard.html",services=service_summary, professionals=professional_summary, customers=customer_summary)


#professional dashboard route
@app.route("/professional_dashboard")
def professional_dashboard():
    user = current_user()
    professional_id = session.get("user_id")
    if not user or session.get("role") != "1":
        return redirect(url_for("login"))
    professional_request = fetch_professional_request(professional_id)
    return render_template("professionalDashboard.html", requests=professional_request)


#customer dashboard route
@app.route("/customer_dashboard")
def customer_dashboard():
    user = current_user()
    customer_id = session.get("user_id")
    if not user or session.get("role") != "2":
        return redirect(url_for("login"))
    service_summary = fetch_services()
    customer_requests = fetch_customer_request(customer_id)
    return render_template("customerDashboard.html", services=service_summary, requests=customer_requests)


#professional register route
@app.route("/professional_Register",methods = ["GET","POST"])
def pro_register():
    services = db.session.query(Service_Info.service).distinct().all()
    if request.method == "POST":
        email=request.form.get("email")
        full_name=request.form.get("full_name")
        password=request.form.get("password")
        service_name=request.form.get("service")
        experience=request.form.get("experience")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        mobile_number=request.form.get("mobile_number")
        document=request.files.get("document")
        
        if not document:
            return render_template("professionalRegister.html", msg="Please upload a documnet.")
        if not allowed_file(document.filename):
            return render_template("professionalRegister.html", msg="Invalid document format.")
            
        
        # save file
        filename=secure_filename(document.filename)
        file_path=os.path.join(app.config["UPLOAD_FOLDER"], filename)
        document.save(file_path)
        relative_file_path = os.path.relpath(file_path, start=os.path.join(os.getcwd(), "static")).replace("\\","/")
        
        service = Service_Info.query.filter_by(service=service_name).first()
        if not service:
            return render_template("professionalRegister.html", msg="Selected service does not exist.")
        
        professional=Professional_Info.query.filter_by(email=email).first()
        if not professional:
            new_professional=Professional_Info(email=email, full_name=full_name, password=password, service_name=service.service, experience=experience, address=address, pincode=pincode, mobile_number=mobile_number, document=relative_file_path)
            db.session.add(new_professional)
            db.session.commit()
            flash("Account created successfully", "success")
            return redirect(url_for("login"))
        else:
            return render_template("professionalRegister.html",msg="* A professional account already exist with the email provided.")
    return render_template("professionalRegister.html", services=services, msg="")


#customer register route
@app.route("/customer_Register",methods = ["GET","POST"])
def cus_register():
    if request.method == "POST":
        email=request.form.get("email")
        full_name=request.form.get("full_name")
        password=request.form.get("password")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        mobile_number=request.form.get("mobile_number")
        user=Customer_Info.query.filter_by(email=email).first()
        if not user:
            new_user=Customer_Info(email=email, full_name=full_name, password=password, address=address, pincode=pincode, mobile_number=mobile_number)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully", "success")
            return redirect(url_for("login"))
        else:
            return render_template("customerRegister.html",msg="* A customer account already exist with the email provided.")
    return render_template("customerRegister.html",msg="")


#profile route
@app.route('/profile', methods=["GET","POST"])
def profile():
    user_role = session.get("role")
    user_id = session.get("user_id")
    
    if request.method == "GET":
        if user_role == "1":
            user = Professional_Info.query.get(user_id)
        elif user_role == "2":
            user = Customer_Info.query.get(user_id)
        else:
            return "Invalid role"
        
        if user:
           return render_template("profile.html", user=user, user_role = user_role)
        return "User not found"
    
    elif request.method == "POST":
        data = request.form
        if user_role == "1":
            user = Professional_Info.query.get(user_id)
        elif user_role == "2":
            user = Customer_Info.query.get(user_id)
            
        if user:
            user.full_name = data.get("full_name")
            user.email = data.get("email")
            user.password = data.get("password")
            user.address = data.get("address")
            user.pincode = data.get("pincode")
            user.mobile_number = data.get("mobile_number")
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect("/profile")
        return "User not found"
    
    
# fetch professional information function
def fetch_professional():
    professionals=Professional_Info.query.all()
    professional_list=[]
    for professional in professionals:
        professional_data = {
            "id":professional.id,
            "name":professional.full_name,
            "experience":professional.experience,
            "service":professional.service_name,
            "document":professional.document,
            "status":professional.is_approved
        }
        professional_list.append(professional_data)
    return professional_list


# fetch customer information function
def fetch_customer():
    customers=Customer_Info.query.all()
    customer_list={}
    for customer in customers:
        if customer.id not in customer_list.keys():
            customer_list[customer.id]=[customer.full_name, customer.address, customer.pincode, customer.is_approved]
    return customer_list


# fetch service information function
def fetch_services():
    services=Service_Info.query.all()
    service_list={}
    for service in services:
        professionals = Professional_Info.query.filter_by(service_name=service.service).all()
        professional_details = []
        for professional in professionals:
            professional_details.append({"id":professional.id, "name":professional.full_name, "experience":professional.experience, "document":professional.document})
        service_list[service.id]={"service_name":service.service, "price":service.price, "time":service.time, "description":service.description, "professionals":professional_details}
    return service_list


# fetch information about customer request 
def fetch_customer_request(customer_id):
    requests = Request_Info.query.filter(Request_Info.customer_id == customer_id).all()
    request_list = []
    for request in requests:
        request_list.append({
            "id":request.id,
            "service_name":request.service_id,
            "professional_name":request.professional.full_name if request.professional else None,
           "mobile_number":request.professional.mobile_number if request.professional else None,
            "date_of_completition":request.date_of_completion,
           "status":request.status,
           "rating":request.rating
        })
    print(request_list)
    return request_list


#fetch information about request come to professional
def fetch_professional_request(professional_id):
    requests = Request_Info.query.filter(Request_Info.professional_id == professional_id).all()
    request_list = []
    for request in requests:
        request_list.append({
            "id":request.id,
            "customer_name":request.customer.full_name,
            "mobile_number":request.customer.mobile_number,
            "date_of_request":request.date_of_request,
            "date_of_completition":request.date_of_completion,
            "status":request.status,
            "rating":request.rating
        })
    return request_list


#service rating route
@app.route("/service_rating", methods=["POST"])
def service_rating():
    request_id = request.form.get("request_id")
    rating = request.form.get('rating')
    
    if not request_id or not rating:
        return redirect(url_for("customer_dashboard"))
    
    service_request = Request_Info.query.get(request_id)
    if service_request:
        service_request.rating = int(rating)
        db.session.commit()
        flash("Rating updated successfully", "success")
    return redirect(url_for("customer_dashboard"))



# service add route
@app.route("/service/add", methods=["GET", "POST"])
def new_service():
        service=request.form.get("service")
        price=request.form.get("price")
        time=request.form.get("time")
        description=request.form.get("description")
        
        new_service=Service_Info(service=service, price=price, time=time, description=description)
        db.session.add(new_service)
        db.session.commit()
        flash("Service added successfully","success")
        return redirect(url_for('admin_dashboard'))


#service edit route
@app.route("/service/edit/<int:key>", methods=["GET", "POST"])
def edit_service(key):
     if request.method == "POST":
        service_obj=Service_Info.query.get(key)
        service_obj.price=request.form.get("price")
        service_obj.time=request.form.get("time")
        service_obj.description=request.form.get("description")
        
        db.session.commit()
        flash("Service updated successfully","success")
        return redirect(url_for('admin_dashboard'))


#service delete route
@app.route("/service/delete/<int:key>", methods=["GET", "POST"])
def delete_service(key):
    if request.method == "POST":
        service_obj=Service_Info.query.get(key)
        db.session.delete(service_obj)
        db.session.commit()
        flash("Service deleted successfully", "success")
        return redirect(url_for('admin_dashboard'))
    

#approve professional route
@app.route("/approve_professional/<int:id>", methods=["POST"])
def approve_professional(id):
    professional = Professional_Info.query.get(id)
    if professional:
        professional.is_approved = 1
        db.session.commit()
        return jsonify({"success":True, "message":"Professional is approved."})
    return jsonify({"success": False, "message":"Professional is not found."})


#block professional route
@app.route("/block_professional/<int:id>", methods=["POST"])
def block_professional(id):
    professional = Professional_Info.query.get(id)
    if professional:
        professional.is_approved = 2
        db.session.commit()
        return jsonify({"success":True, "message":"Professional is blocked."})
    return jsonify({"success": False, "message":"Professional is not found."})


#block customer route
@app.route("/block_customer/<int:id>", methods=["POST"])
def block_customer(id):
    customer = Customer_Info.query.get(id)
    if customer:
        customer.is_approved = False
        db.session.commit()
        return jsonify({"success":True, "message":"Customer is blocked."})
    return jsonify({"success": False, "message":"Customer is not found."})


#book service route
@app.route("/book_service", methods=["POST"])
def book_service():
    service_name = request.form.get("service_name")
    professional_id = request.form.get("professional_id")
    customer_id = session.get("user_id")
    
    new_request = Request_Info(customer_id=customer_id, professional_id=professional_id, service_id=service_name, date_of_request=datetime.now().date())
    db.session.add(new_request)
    db.session.commit()
    flash("Service booked successfully", "success")
    return redirect(url_for("customer_dashboard"))


#approve service route
@app.route("/approve_service/<int:id>", methods=["POST"])
def approve_service(id):
    service = Request_Info.query.get(id)
    if service:
        service.status = 1
        db.session.commit()
        return jsonify({"success":True, "message":"Service is accepted."})
    return jsonify({"success": False, "message":"Service is not found."})


#reject service route 
@app.route("/reject_service/<int:id>", methods=["POST"])
def reject_service(id):
    service = Request_Info.query.get(id)
    if service:
        service.status = 3
        db.session.commit()
        return jsonify({"success":True, "message":"Service is rejected."})
    return jsonify({"success": False, "message":"Service is not found."})


#complete service route
@app.route("/complete_service/<int:id>", methods=["POST"])
def complete_service(id):
    service = Request_Info.query.get(id)
    if service:
        service.status = 2
        service.date_of_completion = datetime.now().date()
        db.session.commit()
        return jsonify({"success":True, "message":"Service is completed."})
    return jsonify({"success": False, "message":"Service is not found."})


#cancel service route
@app.route("/cancel_service/<int:id>", methods=["POST"])
def cancel_service(id):
    service = Request_Info.query.get(id)
    if service:
        db.session.delete(service)
        db.session.commit()
        return jsonify({"success":True, "message":"Service is cancelled."})
    return jsonify({"success": False, "message":"Service is not found."})


#admin summary route for graph
@app.route('/admin_summary')
def admin_summary():
    services = Service_Info.query.all()
    professionals = Professional_Info.query.all()
    customers = Customer_Info.query.all()
    
    service_summary = {
        "service":len([service.service for service in services])
    }
    
    professional_summary = {
        "active": sum(1 for p in professionals if p.is_approved == 1),
        "blocked": sum(1 for p in professionals if p.is_approved == 2),
        "pending": sum(1 for p in professionals if p.is_approved == 0)
    }
    
    customer_summary = {
        "active": sum(1 for c in customers if c.is_approved == 1),
        "blocked": sum(1 for c in customers if c.is_approved == 0)
    }
    print(service_summary)
    print(professional_summary)
    return render_template('adminDashboardSummary.html', service_summary=json.dumps(service_summary), professional_summary=json.dumps(professional_summary), customer_summary=json.dumps(customer_summary))


#professional summary route for garph
@app.route('/professional_summary')
def professional_summary():
    
    professional_id = session["user_id"]
    
    requests = Request_Info.query.filter_by(professional_id=professional_id).all()
    
    request_summary = {
        "pending": sum(1 for r in requests if r.status == 0),
        "accepted": sum(1 for r in requests if r.status == 1),
        "completed": sum(1 for r in requests if r.status == 2),
        "rejected": sum(1 for r in requests if r.status == 3)
    }
    
    return render_template('professionalDashboardSummary.html', request_summary=json.dumps(request_summary))


#customer summary route for graph
@app.route('/customer_summary')
def customer_summary():
    
    customer_id = session["user_id"]
    
    requests = Request_Info.query.filter_by(professional_id=customer_id).all()
    
    request_summary = {
        "pending": sum(1 for r in requests if r.status == 0),
        "accepted": sum(1 for r in requests if r.status == 1),
        "completed": sum(1 for r in requests if r.status == 2),
        "rejected": sum(1 for r in requests if r.status == 3)
    }
    
    return render_template('customerDashboardSummary.html', request_summary=json.dumps(request_summary))


#search route
@app.route('/search_service', methods=["GET"])
def search_service():
    query = request.args.get('query','').strip()
    customer_id = session.get("user_id")
    
    all_services = Service_Info.query.all()
    service_list = {}
    
    for service in all_services:
        if not query or query.lower() in service.service.lower():
            professionals = Professional_Info.query.filter_by(service_name=service.id).all()
            professional_details = [{"id":professional.id, "name":professional.full_name, "experience":professional.experience, "document":professional.document} for professional in professionals]
            
            service_list[service.id] = {"service_name":service.service,"price":service.price, "description":service.description, "professionals":professional_details}
        
    customer_requests = fetch_customer_request(customer_id)
    return render_template("customerDashboard.html", services=service_list, requests=customer_requests)