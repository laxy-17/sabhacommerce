from flask import Blueprint, request, jsonify
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

ops_bp = Blueprint('ops', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@ops_bp.route('/contact', methods=['POST'])
def contact():
    """Send a contact email"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data or field not in data or not data[field].strip():
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        name = data['name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        
        # In a real application, you would send an actual email
        # For this demo, we'll just log the contact attempt
        logger.info(f"Contact form submission - Name: {name}, Email: {email}, Subject: {subject}")
        
        # Simulate email sending (replace with actual email service in production)
        try:
            # This is a mock implementation
            # In production, you would use services like SendGrid, AWS SES, etc.
            mock_send_email(name, email, subject, message)
            
            return jsonify({
                'status': 'success',
                'message': 'Your message has been sent successfully! We will get back to you soon.'
            })
            
        except Exception as email_error:
            logger.error(f"Failed to send email: {str(email_error)}")
            return jsonify({
                'status': 'failure',
                'message': 'Failed to send message. Please try again later.'
            }), 500
        
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({'error': 'Failed to process contact form'}), 500

@ops_bp.route('/update-location', methods=['POST'])
def update_location():
    """Update user's current location"""
    try:
        data = request.get_json()
        
        if not data or 'location' not in data:
            return jsonify({'error': 'Missing location in request body'}), 400
        
        location = data['location']
        zip_code = data.get('zipCode', None)
        
        # In a real application, you would:
        # 1. Validate the location
        # 2. Store it in a user session or database
        # 3. Possibly geocode it to get coordinates
        
        # For this demo, we'll just validate and return success
        if not location.strip():
            return jsonify({
                'status': 'failure',
                'message': 'Location cannot be empty'
            }), 400
        
        logger.info(f"Location updated to: {location}, Zip: {zip_code}")
        
        return jsonify({
            'status': 'success',
            'message': 'Location updated successfully',
            'newLocation': location
        })
        
    except Exception as e:
        logger.error(f"Error updating location: {str(e)}")
        return jsonify({'error': 'Failed to update location'}), 500

def mock_send_email(name, email, subject, message):
    """Mock email sending function"""
    # In a real application, implement actual email sending here
    # Example using SMTP:
    
    # smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    # smtp_port = int(os.getenv('SMTP_PORT', '587'))
    # smtp_username = os.getenv('SMTP_USERNAME')
    # smtp_password = os.getenv('SMTP_PASSWORD')
    # 
    # if not smtp_username or not smtp_password:
    #     raise Exception("SMTP credentials not configured")
    # 
    # msg = MIMEMultipart()
    # msg['From'] = smtp_username
    # msg['To'] = 'contact@vibe.com'  # Your contact email
    # msg['Subject'] = f"Contact Form: {subject}"
    # 
    # body = f"""
    # New contact form submission:
    # 
    # Name: {name}
    # Email: {email}
    # Subject: {subject}
    # 
    # Message:
    # {message}
    # """
    # 
    # msg.attach(MIMEText(body, 'plain'))
    # 
    # server = smtplib.SMTP(smtp_server, smtp_port)
    # server.starttls()
    # server.login(smtp_username, smtp_password)
    # text = msg.as_string()
    # server.sendmail(smtp_username, 'contact@vibe.com', text)
    # server.quit()
    
    # For demo purposes, just log the email
    logger.info(f"Mock email sent - From: {email}, Subject: {subject}")
    return True

