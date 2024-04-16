from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config for database
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

@app.route('/play/<int:set_id>')
def play(set_id):
    emails = Email.query.filter_by(set_id=set_id).all()
    email_data = [{'set_id': email.set_id,
                   'email_id': email.email_id,
                   'from_email': email.from_email,
                   'to_email': email.to_email,
                   'subject': email.subject,
                   'body': email.body,
                   'closing': email.closing,
                   'attachment': email.attachment,
                   'link': email.link,
                   'is_phishing': email.is_phishing} for email in emails]
    return jsonify(email_data)

if __name__ == '__main__':
    app.run(debug=True)
