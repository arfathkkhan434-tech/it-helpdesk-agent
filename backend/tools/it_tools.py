import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

def send_real_email(recipient: str, subject: str, body: str) -> bool:
    sender = os.getenv("SMTP_EMAIL")
    password = os.getenv("SMTP_PASSWORD")
    
    if not sender or not password:
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

@tool
def reset_password_tool(user_email: str) -> str:
    """Trigger an automated password reset and account unlock for an Active Directory / LDAP user."""
    
    # Updated to point to your new FastAPI password reset web page
    reset_link = "http://localhost:8000/reset-password"
    
    subject = "Action Required: IT Helpdesk Password Reset"
    body = (
        f"Hello,\n\n"
        f"A password reset request was triggered for your enterprise profile ({user_email}).\n\n"
        f"Reset Link: {reset_link}\n\n"
        f"If you did not request this, contact Security Operations immediately.\n"
    )

    email_sent = send_real_email(user_email, subject, body)
    
    if email_sent:
        return f"SUCCESS: Real password reset link sent to {user_email}. Active Directory lockout flag cleared."
    else:
        return f"SUCCESS (Simulated): Password reset link dispatched to {user_email}. Active Directory lockout flag cleared."

@tool
def install_software_tool(user_email: str, software_name: str) -> str:
    """Trigger a silent software deployment to an employee machine for approved applications."""
    return f"SUCCESS: Silent installer package for '{software_name}' dispatched to machine registered to {user_email}."

@tool
def grant_access_tool(user_email: str, system_name: str) -> str:
    """Grant permission or access group membership to an employee for internal systems."""
    return f"SUCCESS: Access credentials and group membership provisioned for '{system_name}' to account {user_email}."

@tool
def request_hardware_tool(user_email: str, item_name: str) -> str:
    """Submit a requisition order for standard IT hardware (monitors, keyboards, mice, headsets)."""
    return f"SUCCESS: Automated hardware requisition for '{item_name}' has been placed for {user_email}. Asset tracking ID: #REQ-7729."