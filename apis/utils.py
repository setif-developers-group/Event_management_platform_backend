from datetime import date, datetime
from zoneinfo import ZoneInfo
from app_models.models import Attendance
from decouple import config
from app_models.utils import sent_email    
import jwt
from datetime import datetime, timedelta
import re
from app_models.models import Registration, Workshop



EVENT_START_DATE = date(2025, 9, 29)
EVENT_START_REGISTRATION = date(2025, 9, 25)


def get_registration_week_nuber():
    today = datetime.now(tz=ZoneInfo('Africa/Algiers')).date()

    if today < EVENT_START_DATE:
        return 1
    else:
        return ((today - EVENT_START_REGISTRATION).days // 7) + 1
    
def get_time_from_last_registration(attendance: Attendance):
    if attendance is None:
        return 24
    today = datetime.now(tz=ZoneInfo('Africa/Algiers')).date()
    return (today - attendance.attendance_date).hours


def is_workshop_finished(workshop):
    today = datetime.now(tz=ZoneInfo('Africa/Algiers')).date()
    return today > workshop.date + workshop.duration


def sent_email_confirmation_email(payload:str, data: dict):
    confirmation_url = f"{config('FRONTEND_URL', default='https://skills-lab.setif-developers-club.com')}/email-confirmation/confirm-email?token={payload}"
    subject = f'Confirm Your Email for {data.get("workshop_title")} Registration'
    body = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; background: #f2f4f7; }}
                .container {{ max-width: 600px; margin: 20px auto; padding: 0 20px; }}
                .header {{ background: linear-gradient(135deg, #1772cd 0%, #359aec 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .workshop-info {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #1772cd; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .button {{ display: inline-block; background: #1772cd; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📧 Confirm Your Email</h1>
                    <p>Welcome to SDG Skills Lab</p>
                </div>
                
                <div class="content">
                    <h2>Dear {data.get('first_name')},</h2>
                    <p>Thank you for registering for our workshop! Before we can confirm your spot, please verify your email address by clicking the button below:</p>
                    
                    <div class="workshop-info">
                        <h3>📚 {data.get('workshop_title')}</h3>
                        <p><strong>Participant:</strong> {data.get('full_name')}</p>
                    </div>

                    <p style="text-align:center;">
                        <a href="{confirmation_url}" class="button">Confirm Email Address</a>
                    </p>

                    <p>If the button above doesn't work, copy and paste the following link into your browser:</p>
                    <p style="word-break: break-all;">{confirmation_url}</p>
                    
                    <div class="footer">
                        <p><strong>Best regards,</strong><br>
                        SDG Skills Lab Team</p>
                        
                        <p><em>Questions? Reply to this email and we'll help you out!</em></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
    sent_email(
        to_email=data.get('email'),
        subject=subject,
        body=body
    )
    return True


def create_email_confirmation_token(data: dict) -> str:

    payload = {
        'email': data.get('email'),
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'workshop_id': data.get('workshop_id'),
        'phone_number': data.get('phone_number'),
        'attendance_type': data.get('attendance_type'),
        'exp': datetime.now() + timedelta(hours=12), 
        'iat': datetime.now()
    }
    token = jwt.encode(payload, config('JWT_SECRET_KEY', default='your-secret-key'), algorithm='HS256')
    return token

def decode_email_confirmation_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, config('JWT_SECRET_KEY', default='your-secret-key'), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Token has expired try to register again')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Invalid token')
    


TEMP_EMAIL_DOMAINS = [
    'temp.com', 'temp.net', 'temp.org', 'temp.co',
    'tempmail.com', 'tempmail.net', 'tempmail.org',
    '10minutemail.com', '10minutemail.net',
    'guerrillamail.com', 'guerrillamail.net', 'guerrillamail.org',
    'throwaway.email', 'throwaway.com',
    'disposable.com', 'disposable.net',
    'fake.com', 'fake.net', 'fake.org',
    'test.com', 'test.net', 'test.org',
    'example.com', 'example.net', 'example.org',
    'mailinator.com', 'mailinator.net',
    'yopmail.com', 'yopmail.net',
    'trashmail.com', 'trashmail.net',
    'temporary.email', 'temporary.com',
    'spam4.me', 'spamgourmet.com',
    'sharklasers.com', 'getnada.com'
]

def is_temp_email(email):
    """Check if email is from a temporary/disposable email service"""
    if not email:
        return False
    
    email = email.lower().strip()
    
    # Extract domain from email
    if '@' not in email:
        return False
    
    domain = email.split('@')[-1]
    
    # Check against known temp domains
    if domain in TEMP_EMAIL_DOMAINS:
        return True
    
    # Check for common temp patterns
    temp_patterns = [
        r'.*@temp\..*',
        r'.*@tmp\..*',
        r'.*@temporary\..*',
        r'.*@throwaway\..*',
        r'.*@disposable\..*',
        r'.*@fake\..*',
        r'.*@test\..*',
        r'.*@example\..*',
    ]
    
    for pattern in temp_patterns:
        if re.match(pattern, email):
            return True
    
    return False

def contains_temp_email(text):
    """Check if text contains any temp email addresses"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails_in_text = re.findall(email_pattern, text)
    
    for email in emails_in_text:
        if is_temp_email(email):
            return True, email
    
    return False, None


def validate_email_workshop(email: str, workshop_id: int) -> bool:
    
    if not email or not workshop_id:
        return 'Invalid email or workshop ID'
    if is_temp_email(email):
        return "bot detected not allowed"
    if Registration.objects.filter(email=email, workshop_id=workshop_id).exists():
        return "Registration is already exists for this email and workshop."
    if Workshop.objects.filter(id=workshop_id).first().week != get_registration_week_nuber():
        return "Registration is closed or didn't start yet"
    return False
