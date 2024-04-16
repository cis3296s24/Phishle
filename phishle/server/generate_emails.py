from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from api.api import get_response
import random
from random import randint
import re
from apscheduler.schedulers.background import BlockingScheduler


Base = declarative_base()

# emails database model
class Email(Base):
    __tablename__ = 'Emails'
    set_id = Column(Integer, primary_key=True)
    email_id = Column(Integer, primary_key=True)
    from_email = Column(String(120), nullable=False)
    to_email = Column(String(120), nullable=False)
    subject = Column(String(120), nullable=False)
    body = Column(Text, nullable=False)
    closing = Column(String(120), nullable=False)
    attachment = Column(String(120), nullable=False)
    link = Column(String(120), nullable=False)
    is_phishing = Column(Boolean, nullable=False, default=False)


# Database connection setup
DATABASE_URI = 'mysql+pymysql://phishle:phishlepasswd@localhost/phishle_database'
engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

# List of distinguishing element of a phishing email
elements_list = ["poor grammar and spelling mistakes", "unsecured and suspicious link", "urgency and threatening language", "unexpected or suspicious attachments"]

# Create the Emails table if it doesn't exist
def initialize_database():
    Base.metadata.create_all(engine)
    latest_set_id = db_session.query(Email.set_id).order_by(Email.set_id.desc()).first()
    if latest_set_id:
        return latest_set_id[0]
    else:
        return 0

def generate_emails():

    latest_set_id = initialize_database()
    set_id = latest_set_id + 1
    
    # Select a random element and number
    random_element = random.choice(elements_list)
    random_number = randint(1, 3)

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

            db_session.add(new_email)
            email_index += 1

        db_session.commit()
        
    finally:
        db_session.close()
        print(random_element, random_number)

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


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(generate_emails, 'cron', hour=0, minute=0)
    scheduler.start()