from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from api.api import get_response
import random
from random import randint
import re

app = Flask(__name__)

# app.config for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://phishle:phishlepasswd@localhost/phishle_database'
db = SQLAlchemy(app)

# List of distinguishing element of a phishing email
elements_list = ["poor grammar and spelling mistakes", "unsecured and suspicious link", "urgency and threatening language", "unexpected or suspicious attachments"]

# emails database model
class Email(db.Model):
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

# Create the Emails table if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/api/emails', methods=['GET'])
def get_emails():

    # Select a random element from the list
    random_element = random.choice(elements_list)
    random_number = randint(1, 3)

    print(random_element)

    prompt = f"""
    I want you to generate a set of 3 emails. One of the emails in the set is a subtle phishing attempt by an adversary. The other two emails in the set are legitimate emails that could be mistaken as a phishing attempt. 

    Each email should have the following sections:
    From: <email address>
    To: <email address>
    Subject: <subject line>
    Body: At least 3 sentences
    Closing: <closing statement>

    All emails in the set are related to a certain scenario which is clearly identified at the beginning of the set. 

    The phishing email contains ONLY the following distinguishing element: {random_element}. Every other part of the phishing email must feel legitimate. If the distinguishing element is an unsecured and suspicious link, the other legitimate emails in the set contain a legitimate link. If the distinguishing element is an unexpected and suspicious attachment, the other legitimate emails in the set contains an attachment in the following format 'name.filetype'.

    I want the phishing email to be email number {random_number}. Do not include any extra explanations."

    The scenario and the emails should follow this exact structure:
    Scenario: [Describe in 3 words]

    Email 1:
    From: [Insert sender's email address]
    To: [Insert recipient's email address]
    Subject: [Insert subject of the email]
    Body: [Insert a detailed message, making sure it contains multiple sentences.]
    Closing: [Insert a single sentence closing line]
    Attachment: [If there is no attachment, write 'none']
    Link: [If there is no link, write 'none']

    Email 2:   
    From: [Insert sender's email address]
    To: [Insert recipient's email address]
    Subject: [Insert subject of the email]
    Body: [Insert a detailed message, making sure it contains multiple sentences.]
    Closing: [Insert a single sentence closing line]
    Attachment: [If there is no attachment, write 'none']
    Link: [If there is no link, write 'none']

    Email 3:
    From: [Insert sender's email address]
    To: [Insert recipient's email address]
    Subject: [Insert subject of the email]
    Body: [Insert a detailed message, making sure it contains multiple sentences.]
    Closing: [Insert a single sentence closing line]
    Attachment: [If there is no attachment, write 'none']
    Link: [If there is no link, write 'none']

    Please ensure each field starts on a new line exactly as shown, and follows the punctuation and format exactly as specified. The content should be clear, professional, and realistic for a business setting.
    """
    
    # Getting the response from GPT-4t
    response = get_response(prompt) 
    scenario, parsed_emails = parse_emails(response)

    try:
        latest_set_id = db.session.query(db.func.max(Email.set_id)).scalar() or 0
        set_id = latest_set_id + 1
        email_index = 1

        for email_data in parsed_emails:
            new_email = Email(
                set_id=set_id,
                email_id=email_index,
                from_email=email_data['from'],
                to_email=email_data['to'],
                subject=email_data['subject'],
                body=email_data['body'],
                closing=email_data['closing'],
                attachment=email_data['attachment'],
                link=email_data['link'],
                is_phishing=(email_index == random_number) 
            )

            db.session.add(new_email)
            email_index += 1

        db.session.commit()
        return jsonify({"message": "Emails fetched and stored success"})
    
    except Exception as e:
        return jsonify({"error": str(e)})

def parse_emails(email_content):
    emails = []
    
    email_pattern = re.compile(
        r"From:\s*(.+?)\n" +  
        r"To:\s*(.+?)\n" +  
        r"Subject:\s*(.+?)\n" +  
        r"Body:\s*(.+?)\n" +  
        r"Closing:\s*(.+?)\n" +  
        r"Attachment:\s*(.+?)\n" +
        r"Link: \s*(.+?)(?:\n|$)",
        re.DOTALL  
    )

    # Splitting the scenario from the email content
    parts = email_content.split("Email ")
    scenario = parts[0].strip()
    email_texts = parts[1:]  

    for email_text in email_texts:
        match = email_pattern.search("Email " + email_text)
        if match:
            emails.append({
                "from": match.group(1).strip(),
                "to": match.group(2).strip(),
                "subject": match.group(3).strip(),
                "body": match.group(4).strip(),
                "closing": match.group(5).strip(),
                "attachment": match.group(6).strip(),
                "link": match.group(7).strip()
            })
        else:
            print("Failed to parse some emails correctly:", email_text)

    return scenario, emails

if __name__ == '__main__':
    app.run(debug=True)
