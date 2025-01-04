# Email Verification Lambda Function

## CSYE-6225

- [Web Application](https://github.com/Aquabet/webapp)
- [Terraform-Infra](https://github.com/Aquabet/tf-aws-infra)
- [Serverless Lambda](https://github.com/Aquabet/serverless)

## Functionality

1. Processes SNS Messages:
Extracts email and verification_link from SNS messages.

2. Sends Emails:
Uses the SendGrid API to send verification emails with customizable content.

## Environment Variables

- `AWS_PROFILE`: Included in the sender email (e.g., dev | demo).
- `DOMAIN`: The domain for the sender email address.(e.g., example.com).
- `SECRET_NAME`: The name of aws secrets managers secret.
- `PARAMETERS_SECRETS_EXTENSION_HTTP_PORT`: Port for layer AWS-Parameters-and-Secrets-Lambda-Extension
, default 2773.

The email will send from `AWS_PROFILE@DOMAIN` (e.g., dev@example.com).

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
      "Sns": {"Message": "{\"email\": \"user@example.com\",\"verification_link\": \"https://example.com/verify?token=abc123\"}"
      }
    }
  ]
}

```
