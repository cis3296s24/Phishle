from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import pymysql

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
    user_ranks = db.Column(db.String(500), nullable=False) #user_id, currentstreak

@app.route('/joinGlobalGroup', methods=['POST'])
@cross_origin()
def joinGlobalGroup():
    data = request.json
    Username = data.get('Username')
    user = db.session.query(User).filter(User.username == Username).first()  # finds user with matching username
    if user:  # checks if user exists
        group = db.session.query(Group).filter(Group.group_name == 'Global Group').first()  # finds group with matching group name
        group.group_members = group.group_members + ',' + Username  # adds user to group
        db.session.commit()
        return jsonify({"success": True, "message": "User successfully joined global group"}), 200
    else: 
        return jsonify({"success": False, "message": "User does not exist"}), 400  # HTTP 400 Bad Request


@app.route('/joinGroup', methods=['POST'])
@cross_origin()
def joinGroup():
    data = request.json
    Username = data.get('Username')
    GroupCode = data.get('GroupCode')
    user = db.session.query(User).filter(User.username == Username).first()  # finds user with matching username
    group = db.session.query(Group).filter(Group.group_code == GroupCode).first()  # finds group with matching group code
    if user and group:  # checks if user and group exist
        if user.group_id == 0:  # checks if user is already in a group
            if group.group_leader != Username:  # checks if user is not the group leader
                group.group_members = group.group_members + ',' + Username  # adds user to group
                user.group_id = group.group_id  # sets user's group id to group's id
                db.session.commit()
                return jsonify({"success": True, "message": "User successfully joined group"}), 200
            else:
                return jsonify({"success": False, "message": "User is already the group leader"}), 400  # HTTP 400 Bad Request
        else: 
            return jsonify({"success": False, "message": "User is already in a group"}), 400  # HTTP 400 Bad Request
    else: 
        return jsonify({"success": False, "message": "User or group does not exist"}), 400  # HTTP 400 Bad Request
    
@app.route('/createGroup', methods=['POST'])
@cross_origin()
def createGroup():
    data = request.json
    Username = data.get('Username')
    GroupName = data.get('GroupName')
    user = db.session.query(User).filter(User.username == Username).first() # finds user with matching username
    code = random.randint(1,300)
    if user: # checks if user exists
        if user.group_id == 0: # checks if user is not already in a group
            while db.session.query(Group).filter(Group.group_id == code).first():
                code = random.randint(1,300)
            group = Group(group_name=GroupName, group_code=code, group_leader=Username, group_members=Username, group_leaderboard_id=0) # creates new group
            db.session.add(group)
            db.session.commit()
            user.group_id = group.group_id # sets user's group id to group's id
            db.session.commit()
            return jsonify({"success": True, "message": "Group successfully created"}), 201
        else:
            return jsonify({"success": False, "message": "User is already in a group"}), 400  # HTTP 400 Bad Request
    else:
        return jsonify({"success": False, "message": "User does not exist"}), 400  # HTTP 400 Bad Request
    
@app.route('/leaveGroup', methods=['POST'])
@cross_origin()
def leaveGroup():
    data = request.json
    Username = data.get('Username')
    user = db.session.query(User).filter(User.username == Username).first() # finds user with matching username
    if user: # checks if user exists
        if user.group_id != 0: # checks if user is in a group
            group = db.session.query(Group).filter(Group.group_id == user.group_id).first() # finds group with matching group id
            if group.group_leader == Username: # checks if user is the group leader
                if group.group_members != Username: # checks if there are other members in the group
                    group.group_leader = group.group_members.split(',')[0] # sets the first member in the group as the new group leader
                    group.group_members = group.group_members.replace(group.group_members.split(',')[0] + ',', '') # removes the new group leader from the group members
                    user.group_id = 0 # sets user's group id to 0
                    db.session.commit()
                    return jsonify({"success": True, "message": "User successfully left group"}), 200
                else:
                    db.session.delete(group) # deletes group if there are no other members
                    user.group_id = 0 # sets user's group id to 0
                    db.session.commit()
                    return jsonify({"success": True, "message": "User successfully left group"}), 200
            else:
                group.group_members = group.group_members.replace(',' + Username, '') # removes user from group members
                user.group_id = 0 # sets user's group id to 0
                db.session.commit()
                return jsonify({"success": True, "message": "User successfully left group"}), 200
        else:
            return jsonify({"success": False, "message": "User is not in a group"}), 400  # HTTP 400 Bad Request
    else:
        return jsonify({"success": False, "message": "User does not exist"}), 400  # HTTP 400 Bad Request

@app.route('/getGroup', methods=['POST'])
@cross_origin()
def getGroup():
    data = request.json
    Username = data.get('Username')
    user = db.session.query(User).filter(User.username == Username).first() # finds user with matching username
    if user: # checks if user exists
        if user.group_id != 0: # checks if user is in a group
            group = db.session.query(Group).filter(Group.group_id == user.group_id).first() # finds group with matching group id
            return jsonify({"success": True, "group_name": group.group_name, "group_leader": group.group_leader, "group_members": group.group_members.split(','), "group_leaderboard_id": group.group_leaderboard_id}), 200
        else:
            return jsonify({"success": False, "message": "User is not in a group"}), 400  # HTTP 400 Bad Request
    else:
        return jsonify({"success": False, "message": "User does not exist"}), 400  # HTTP 400 Bad Request
    





@app.route('/createLeaderboard', methods=['POST'])
@cross_origin()
def createLeaderboard():
    data = request.json
    group_id = data.get('group_id')
    group = db.session.query(Group).filter(Group.group_id == group_id).first() # finds group with matching id
    if group.group_id != 0: # checks if user is in a group
        leaderboard = Leaderboard(user_ranks='')
        db.session.add(leaderboard)
        db.session.commit()
        group.group_leaderboard_id = leaderboard.leaderboard_id # sets group's leaderboard id to leaderboard's id
        db.session.commit()
        return jsonify({"success": True, "message": "Leaderboard successfully created"}), 201
    else:
        return jsonify({"success": False, "message": "Group does not exist"}), 400  # HTTP 400 Bad Request
    

@app.route('/updateLeaderboard', methods=['POST'])
@cross_origin()
def updateLeaderboard():
    data = request.json
    group_id = data.get('group_id')
    group = db.session.query(Group).filter(Group.group_id == group_id).first() # finds group with matching id
    if group.group_id != 0: # checks if user is in a group
        leaderboard = db.session.query(Leaderboard).filter(Leaderboard.leaderboard_id == group.group_leaderboard_id).first() # finds leaderboard with matching leaderboard id
        user_ranks = leaderboard.user_ranks.split(',') # splits user ranks into a list
        user_ranks = [user_rank.split(':') for user_rank in user_ranks] # splits each user rank into a list
        user_ranks = [[int(user_rank[0]), int(user_rank[1])] for user_rank in user_ranks] # converts user ids and current streaks to integers
        user_ranks = sorted(user_ranks, key=lambda x: x[1], reverse=True) # sorts user ranks by current streaks in descending order
        user_ranks = [str(user_rank[0]) + ':' + str(user_rank[1]) for user_rank in user_ranks] # converts user ids and current streaks back to strings
        user_ranks = ','.join(user_ranks) # joins user ranks into a string
        leaderboard.user_ranks = user_ranks # sets leaderboard's user ranks to the new string
        db.session.commit()
        return jsonify({"success": True, "user_ranks": user_ranks}), 200
    else:
        return jsonify({"success": False, "message": "Group does not exist"}), 400  # HTTP 400 Bad Request
    
@app.route('/updateStreak', methods=['POST'])
@cross_origin()
def updateStreak():
    data = request.json
    Username = data.get('Username')
    user = db.session.query(User).filter(User.username == Username).first() # finds user with matching username
    if user: # checks if user exists
        user.currentstreak = user.currentstreak + 1 # increments user's current streak
        if user.currentstreak > user.longeststreak: # checks if user's current streak is longer than their longest streak
            user.longeststreak = user.currentstreak # sets user's longest streak to their current streak
        db.session.commit()
        return jsonify({"success": True, "message": "User's streak successfully updated"}), 200
    else:
        return jsonify({"success": False, "message": "User does not exist"}), 400  # HTTP 400 Bad Request

@app.route('/resetStreak', methods=['POST'])
@cross_origin()
def resetStreak():
    data = request.json
    Username = data.get('Username')
    user = db.session.query(User).filter(User.username == Username).first() # finds user with matching username
    if user: # checks if user exists
        user.currentstreak = 0 # resets user's current streak
        db.session.commit()
        return jsonify({"success": True, "message": "User's streak successfully reset"}), 200
    else:
        return jsonify({"success": False, "message": "User does not exist"}), 400  # HTTP 400 Bad Request

@app.route('/getGlobalLeaderboard', methods=['GET'])
@cross_origin()
def getGlobalLeaderboard():
    db = pymysql.connect(host='localhost', user='phishle', password='phishlepasswd', database='phishle_database')
    cursor = db.cursor()
    data = cursor.execute("SELECT username, currentstreak, longeststreak from Users order by currentstreak desc")
    data = cursor.fetchall()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"success": False, "message": "Error Fetching Leaderboard"}), 400  # HTTP 400 Bad Request
    
@app.route('/getProfileInfo/<username>', methods=['GET'])
@cross_origin()
def getProfileInfo(username):
    info = db.session.query(User).filter(User.username == username).first()
    if info:
        return jsonify({"username":info.username, "currentstreak":info.currentstreak, "longeststreak":info.longeststreak, "group_id":info.group_id}), 200
    else:
        return jsonify({"success": False, "message": "User does not exist"}), 400  # HTTP 400 Bad Request
    
@app.route('/getGroupLeaderboard/<int:groupId>', methods=['GET'])
@cross_origin()
def getGroupLeaderboard(groupId):
    db = pymysql.connect(host='localhost', user='phishle', password='phishlepasswd', database='phishle_database')
    cursor = db.cursor()
    data = cursor.execute(f"SELECT username, currentstreak, longeststreak from Users where group_id ={groupId} order by currentstreak desc")
    data = cursor.fetchall()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"success": False, "message": "Error Fetching Leaderboard"}), 400  # HTTP 400 Bad Request



@app.route('/getStreak', methods=['POST'])
@cross_origin()
def getStreak():
    data = request.json
    Username = data.get('Username')
    user = db.session.query(User).filter(User.username == Username).first() # finds user with matching username
    if user: # checks if user exists
        return jsonify({"success": True, "currentstreak": user.currentstreak, "longeststreak": user.longeststreak}), 200
    else:
        return jsonify({"success": False, "message": "User does not exist"}), 400  # HTTP 400 Bad Request
    
@app.route('/getGroupCode', methods=['POST'])
@cross_origin()
def getGroupCode():
    data = request.json
    group_id = data.get('group_id')
    group = db.session.query(Group).filter(Group.group_id == group_id).first() # finds group with matching id
    if group.group_id != 0: # checks if user is in a group
        return jsonify({"success": True, "group_code": group.group_code}), 200
    else:
        return jsonify({"success": False, "message": "Group does not exist"}), 400  # HTTP 400 Bad Request
    
@app.route('/getGroupMembers', methods=['POST'])
@cross_origin()
def getGroupMembers():
    data = request.json
    group_id = data.get('group_id')
    group = db.session.query(Group).filter(Group.group_id == group_id).first() # finds group with matching id
    if group.group_id != 0: # checks if user is in a group
        return jsonify({"success": True, "group_members": group.group_members.split(',')}), 200
    else:
        return jsonify({"success": False, "message": "Group does not exist"}), 400  # HTTP 400 Bad Request

@app.route('/getGroupLeader', methods=['POST'])
@cross_origin()
def getGroupLeader():
    data = request.json
    group_id = data.get('group_id')
    group = db.session.query(Group).filter(Group.group_id == group_id).first() # finds group with matching id
    if group.group_id != 0: # checks if user is in a group
        return jsonify({"success": True, "group_leader": group.group_leader}), 200
    else:
        return jsonify({"success": False, "message": "Group does not exist"}), 400  # HTTP 400 Bad Request
    

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
        return jsonify({"success": False}), 400

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
