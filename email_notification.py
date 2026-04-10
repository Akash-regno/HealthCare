"""
Email Notification Service for Critical Patient Alerts
Sends email notifications to doctors when critical patients are detected
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailNotification:
    """Simple email notification service using Gmail SMTP"""
    
    def __init__(self):
        # Email Configuration
        # Use Gmail SMTP server (you can change to other providers)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        # Sender Email (loaded from environment variables — never hardcode credentials!)
        self.sender_email = os.environ.get("SENDER_EMAIL", "")      # Set via env var: SENDER_EMAIL
        self.sender_password = os.environ.get("SENDER_APP_PASSWORD", "")  # Set via env var: SENDER_APP_PASSWORD
        
        # Doctor Email (Recipient)
        self.doctor_email = "akash.wxo@gmail.com"           # Change this to doctor's email
        self.doctor_name = "Dr. Akash"                      # Doctor's name
        
        print("✅ Email notification service initialized")
    
    def send_critical_alert(self, patient_id, status, hr, spo2, temp, acc_mag):
        """
        Send email alert for critical patient
        
        Args:
            patient_id: Patient ID
            status: Patient status (CRITICAL)
            hr: Heart rate (bpm)
            spo2: Oxygen saturation (%)
            temp: Temperature (°C)
            acc_mag: Acceleration magnitude (g)
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"🚨 CRITICAL PATIENT ALERT - {patient_id}"
            message["From"] = self.sender_email
            message["To"] = self.doctor_email
            
            # Create email body (HTML format for better presentation)
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #dc2626; margin-top: 0;">🚨 CRITICAL PATIENT ALERT</h2>
                        
                        <div style="background-color: #fee2e2; border-left: 4px solid #dc2626; padding: 15px; margin: 20px 0;">
                            <p style="margin: 0; font-size: 16px; font-weight: bold;">Immediate attention required!</p>
                        </div>
                        
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr style="background-color: #f9fafb;">
                                <td style="padding: 12px; border: 1px solid #e5e7eb; font-weight: bold;">Patient ID:</td>
                                <td style="padding: 12px; border: 1px solid #e5e7eb;">{patient_id}</td>
                            </tr>
                            <tr>
                                <td style="padding: 12px; border: 1px solid #e5e7eb; font-weight: bold;">Status:</td>
                                <td style="padding: 12px; border: 1px solid #e5e7eb; color: #dc2626; font-weight: bold;">{status}</td>
                            </tr>
                            <tr style="background-color: #f9fafb;">
                                <td style="padding: 12px; border: 1px solid #e5e7eb; font-weight: bold;">Heart Rate:</td>
                                <td style="padding: 12px; border: 1px solid #e5e7eb;">{hr} bpm</td>
                            </tr>
                            <tr>
                                <td style="padding: 12px; border: 1px solid #e5e7eb; font-weight: bold;">Oxygen Saturation:</td>
                                <td style="padding: 12px; border: 1px solid #e5e7eb;">{spo2}%</td>
                            </tr>
                            <tr style="background-color: #f9fafb;">
                                <td style="padding: 12px; border: 1px solid #e5e7eb; font-weight: bold;">Temperature:</td>
                                <td style="padding: 12px; border: 1px solid #e5e7eb;">{temp}°C</td>
                            </tr>
                            <tr>
                                <td style="padding: 12px; border: 1px solid #e5e7eb; font-weight: bold;">Acceleration:</td>
                                <td style="padding: 12px; border: 1px solid #e5e7eb;">{acc_mag}g</td>
                            </tr>
                            <tr style="background-color: #f9fafb;">
                                <td style="padding: 12px; border: 1px solid #e5e7eb; font-weight: bold;">Time:</td>
                                <td style="padding: 12px; border: 1px solid #e5e7eb;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                            </tr>
                        </table>
                        
                        <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0;">
                            <p style="margin: 0; font-size: 14px;">
                                <strong>Note:</strong> This is an automated alert from the Smart Healthcare Monitoring System.
                            </p>
                        </div>
                        
                        <p style="color: #6b7280; font-size: 12px; margin-top: 30px; border-top: 1px solid #e5e7eb; padding-top: 15px;">
                            Smart Healthcare Monitoring Dashboard<br>
                            ECG-based Patient Monitoring System
                        </p>
                    </div>
                </body>
            </html>
            """
            
            # Plain text version (fallback)
            text_body = f"""
🚨 CRITICAL PATIENT ALERT

Patient ID: {patient_id}
Status: {status}
Heart Rate: {hr} bpm
Oxygen Saturation: {spo2}%
Temperature: {temp}°C
Acceleration: {acc_mag}g
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is an automated alert from the Smart Healthcare Monitoring System.
            """
            
            # Attach both versions
            part1 = MIMEText(text_body, "plain")
            part2 = MIMEText(html_body, "html")
            message.attach(part1)
            message.attach(part2)
            
            # Send email
            print("\n" + "=" * 60)
            print("📧 SENDING EMAIL ALERT")
            print("=" * 60)
            print(f"Patient: {patient_id}")
            print(f"Status: {status}")
            print(f"Doctor: {self.doctor_name}")
            print(f"Email: {self.doctor_email}")
            print("=" * 60)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.doctor_email, message.as_string())
            
            print("✅ Email sent successfully!")
            
        except Exception as e:
            print(f"❌ Email error: {str(e)}")
    
    def test_connection(self):
        """Test email configuration"""
        try:
            print("\nTesting email connection...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
            print("✅ Email configuration is working!")
            return True
        except Exception as e:
            print(f"❌ Email configuration error: {str(e)}")
            return False


# Test the email service
if __name__ == "__main__":
    print("=" * 60)
    print("EMAIL NOTIFICATION SERVICE TEST")
    print("=" * 60)
    
    email_service = EmailNotification()
    
    # Test connection
    if email_service.test_connection():
        print("\n" + "=" * 60)
        print("Sending test alert...")
        print("=" * 60)
        
        # Send test alert
        email_service.send_critical_alert(
            patient_id="P001",
            status="CRITICAL",
            hr=165,
            spo2=88.5,
            temp=39.2,
            acc_mag=22.5
        )
        
        print("\n" + "=" * 60)
        print("✅ Test completed! Check your email inbox.")
        print("=" * 60)
