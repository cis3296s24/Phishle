from flask import Flask, jsonify, request
from api import get_response
import random
from random import randint

app = Flask(__name__)

# List of distinguishing element of a phishing email
elements_list = ["poor grammar and spelling mistakes", "unsecured and suspicious link", "urgency and threatening language", "unexpected or suspicious attachments"]

@app.route('/api/app', methods=['GET'])
def get_emails():

    # Select a random element from the list
    random_element = random.choice(elements_list)
    random_number = randint(1, 3)
    
    prompt = f"I want you to generate a set of 3 email. Each and every email in the set consisting of a 'from', 'to', 'subject', 'body', and a 'closing' sections. The 'from' and 'to' sections consist of an email address. The 'body' section consist of more than 3 sentences. All emails in the set are related to a certain scenario which is clearly identified at the beginning of the set. 1 of the emails in the set is a definite, but subtle phishing attempt. The other 2 emails in the set are legitimate emails that could be mistaken as a phishing attempt. The phishing email contains ONLY the following distinguishing element: {random_element}. Every other part of the phishing email must feel legitimate. If the distinguishing element is an unsecured and suspicious link, the other legitimate emails in the set contain a legitimate link. If the distinguishing element is an unexpected and suspicious attachment, the other legitimate emails in the set contains an attachment in the following format 'name.filetype'. I want the phishing email to be email number {random_number}. Do not include unnecessary information."
    
    # Getting the response from GPT-4t
    response = get_response(prompt)

    # Check if the response is valid
    if not response:
        return jsonify({'error': 'Failed to get a response from the API'})

    # Split the response into the scenario and individual emails
    response_parts = response.split("\n\n")
    scenario = response_parts[0]
    email_parts = response_parts[1:]

    emails = []

    for email_part in email_parts:
        email = {}
        email_lines = email_part.split("\n")

        email["from"] = email_lines[0].split(": ")[1]
        email["to"] = email_lines[1].split(": ")[1]
        email["subject"] = email_lines[2].split(": ")[1]

        # Find the start and end of the body
        body_start = email_part.find("Body:\n") + len("Body:\n")
        body_end = email_part.find("Closing:")
        email["body"] = email_part[body_start:body_end].strip()

        email["closing"] = email_part.split("Closing: ")[1].split("\n")[0]

        # Check if there's an attachment
        attachment_start = email_part.find("Attachment:")
        if attachment_start != -1:
            attachment_end = email_part.find("\n", attachment_start)
            email["attachment"] = email_part[attachment_start+len("Attachment:"):attachment_end].strip()
        else:
            email["attachment"] = None

        emails.append(email)

    return jsonify({'scenario': scenario, 'emails': email})


if __name__ == '__main__':
    app.run(debug=True)
