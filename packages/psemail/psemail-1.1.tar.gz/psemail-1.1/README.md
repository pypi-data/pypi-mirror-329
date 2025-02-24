# psemail

`psemail` is a Python library for sending emails using smtplib, designed primarily for system health monitoring notifications, with potential for future extensions. 

## Installation

```sh
pip install psemail
```

## Usage

```python
import dotenv
dotenv.load_dotenv()
from psemail.email_sender import send_email

send_email("recipient@example.com", "Subject", "Email body")
```

## Environment Variables
Create a `.env` file with the following content:

```
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_email_password
SMTP_SERVER=smtp.example.com
SMTP_PORT=465
```