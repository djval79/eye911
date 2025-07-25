"""
PulsePoint Partnership Request Submission Script
"""
import smtplib
from email.mime.text import MIMEText

# Email content
email_body = """
NOVUMSOLVO is developing a traffic safety monitoring system and would like to request API access.

Organization Details:
- Name: NOVUMSOLVO
- Contact: Valentine
- Email: valentine@novumsolvo.co.uk

Project Details:
- Purpose: Real-time traffic incident monitoring
- Initial Coverage: Los Angeles County
- Data Usage: Will comply with all PulsePoint guidelines
"""

msg = MIMEText(email_body)
msg['Subject'] = 'Partnership Inquiry - PulsePoint API Access'
msg['From'] = 'valentine@novumsolvo.co.uk'
msg['To'] = 'partnerships@pulsepoint.org'

print("Preparing PulsePoint partnership email...")
try:
    with smtplib.SMTP('smtp.novumsolvo.co.uk') as server:
        server.send_message(msg)
    print("Email sent successfully")
except Exception as e:
    print(f"Error sending email: {str(e)}")
