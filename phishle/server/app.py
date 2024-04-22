from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

# app.config for database
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://phishle:phishlepasswd@localhost/phishle_database'
db = SQLAlchemy(app)

class Email(db.Model):
    __tablename__ = 'Emails' 
    set_id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, primary_key=True)
    from_email = db.Column(db.String(120), nullable=False)
    to_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    closing = db.Column(db.String(120), nullable=False)
    attachment = db.Column(db.String(120), nullable=False)
    link = db.Column(db.String(120), nullable = False)
    is_phishing = db.Column(db.Boolean, nullable = False, default = False)
    feedback = db.Column(db.String(240), nullable = False)

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    currentstreak = db.Column(db.Integer, nullable=False)
    longeststreak = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, nullable=False)

class Group(db.Model):
    __tablename__ = 'Groups'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(120), nullable=False)
    group_code = db.Column(db.String(120), nullable=False)
    group_leader = db.Column(db.String(120), nullable=False)
    group_members = group_members = db.Column(db.String(500), nullable=False)
    group_leaderboard_id = db.Column(db.Integer, nullable=False)

class Leaderboard(db.Model):
    __tablename__ = 'Leaderboards'
    leaderboard_id = db.Column(db.Integer, primary_key=True) 
    userranks = db.Column(db.String(500), nullable=False) #user_id, currentstreak, longeststreak

with app.app_context():
    db.create_all()

@app.route('/userlogin', methods=['POST'])
@cross_origin()
def userlogin():
    data = request.json
    Username = data.get('Username')
    Password = data.get('Password')
    user = db.session.query(User).filter(User.username == Username).first()  # finds user with matching username
    if user and user.password == Password:  
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 


@app.route('/userregister', methods=['POST'])
@cross_origin()
def userregister():
    data = request.json
    Username = data.get('Username')
    Password = data.get('Password')
    Password2 = data.get('Password2')

    user = db.session.query(User).filter(User.username == Username).first()  # finds user with matching username
    if user:
        return jsonify({"success": False, "message": "Username already exists"}), 409  # HTTP 409 Conflict
    elif Password != Password2:  # checks if passwords match
        return jsonify({"success": False, "message": "Passwords do not match"}), 400  # HTTP 400 Bad Request
    else:
        newuser = User(username=Username, password=Password, currentstreak=0, longeststreak=0, group_id=0)
        db.session.add(newuser)
        db.session.commit()
        return jsonify({"success": True, "message": "User successfully registered"}), 201


@app.route('/play/<int:set_id>')
@cross_origin()
def play(set_id):
    emails = Email.query.filter_by(set_id=set_id).all()
    email_data = [{
                    'set_id': email.set_id,
                    'email_id': email.email_id,
                    'from_email': email.from_email,
                    'to_email': email.to_email,
                    'subject': email.subject,
                    'body': email.body,
                    'closing': email.closing,
                    'attachment': email.attachment,
                    'link': email.link,
                    'is_phishing': email.is_phishing
                } for email in emails]
    return jsonify(email_data)

@app.route('/latest_set_id')
@cross_origin()
def latest_set_id():
    latest_set_id = db.session.query(db.func.max(Email.set_id)).scalar() or 0
    return jsonify(latest_set_id=latest_set_id)

@app.route('/verify_phishing/<int:set_id>/<int:email_id>')
@cross_origin()
def verify_phishing(set_id, email_id):
    email = db.session.query(Email).filter_by(set_id=set_id, email_id=email_id).first()

    if email:
        return jsonify(is_phishing=email.is_phishing)
    return jsonify(is_phishing=email.is_phishing)
    
@app.route('/verify_phishing/<int:set_id>/<int:email_id>/feedback')
@cross_origin()
def feedback(set_id, email_id):
    email = db.session.query(Email).filter_by(set_id=set_id, email_id=email_id).first()
    return jsonify(feedback=email.feedback)

if __name__ == '__main__':
    app.run(debug=True)
