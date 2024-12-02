import json
import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def get_secret(secret_name):
    secrets_extension_http_port = os.getenv("PARAMETERS_SECRETS_EXTENSION_HTTP_PORT", "2773")
    secrets_extension_endpoint = f"http://localhost:{secrets_extension_http_port}/secretsmanager/get?secretId={secret_name}"

    headers = {"X-Aws-Parameters-Secrets-Token": os.getenv('AWS_SESSION_TOKEN')}
    try:
        response = requests.get(secrets_extension_endpoint, headers=headers)
        response.raise_for_status()
        secret = json.loads(response.text).get("SecretString")
        if secret:
            return json.loads(secret)
        else:
            raise ValueError("No SecretString found in the response.")
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise

def send_email(sendgrid_api_key, from_email, to_email, subject, content):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
    except Exception as e:
        print(f"An error occurred: {e}")


def lambda_handler(event, context):
    try:
        secret_name = os.getenv('SECRET_NAME')
        secrets = get_secret(secret_name)
        sendgrid_api_key = secrets.get('sendgrid_api_key')

        for record in event.get('Records', []):
            sns_message = record['Sns']['Message']
            message_data = json.loads(sns_message)
            
            email = message_data.get('email')
            verification_link = message_data.get('verification_link')
            
            if not email or not verification_link:
                print("Invalid message format")
                continue
            
            # Send email
            from_email = f"{os.getenv("AWS_PROFILE_NAME")}@{os.getenv("DOMAIN")}"
            subject = "Verify Your Email Address"
            content = f"Please verify your email by clicking the following link:\n{verification_link}"
            send_email(sendgrid_api_key, from_email, email, subject, content)
            
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
