import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(from_email, to_email, subject, content):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
    except Exception as e:
        print(f"An error occurred: {e}")


def lambda_handler(event, context):
    try:
        for record in event.get('Records', []):
            sns_message = record['Sns']['Message']
            message_data = json.loads(sns_message)
            
            email = message_data.get('email')
            verification_link = message_data.get('verification_link')
            
            if not email or not verification_link:
                print("Invalid message format")
                continue
            
            # Send email
            from_email = f"{os.getenv("AWS_PROFILE")}@{os.getenv("DOMAIN")}"
            subject = "Verify Your Email Address"
            content = f"Please verify your email by clicking the following link:\n{verification_link}"
            send_email(from_email, email, subject, content)
            
        return {
            'statusCode': 200,
            'body': json.dumps('Email processing completed.')
        }
    except Exception as e:
        print(f"Error processing SNS message: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing SNS message.')
        }
