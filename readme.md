# Email Verification Lambda Function

## Functionality

1. Processes SNS Messages:
Extracts email and verification_link from SNS messages.

2. Sends Emails:
Uses the SendGrid API to send verification emails with customizable content.

## Environment Variables

SENDGRID_API_KEY: SendGrid API key for email sending.
AWS_PROFILE: Included in the sender email (e.g., dev | demo).
DOMAIN: The domain for the sender email address.(e.g., example.com)

## Deployment

Package Code:
Include sendgrid dependency:

```bash
pip install sendgrid -t .
zip -r email_verification_lambda.zip .

```

## Sample Input

```json
{
  "Records": [
    {
      "Sns": {
        "Message": "{\"email\": \"user@example.com\", \"verification_link\": \"https://example.com/verify?token=abc123\"}"
      }
    }
  ]
}

```
