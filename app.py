import streamlit as st
import smtplib
from email.message import EmailMessage
import pandas as pd
from PIL import Image

# Streamlit app interface
st.title('Certificate Sender App')

# Input for email list
emails_input = st.text_area("Paste Emails (one email per line):")

# Input for uploading certificate images
uploaded_files = st.file_uploader("Upload Certificates (in order - filenames like 1.jpg, 2.jpg)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# Sender email credentials
sender_email = "kishoree2375@gmail.com"
app_password = "#"

# Function to send email with certificate
def send_certificate(email, certificate_data, filename, sender_email, password):
    msg = EmailMessage()
    msg['Subject'] = 'Your Certificate'
    msg['From'] = sender_email
    msg['To'] = email
    msg.set_content('Please find your certificate attached.')

    # Attach the certificate image
    msg.add_attachment(certificate_data, maintype='image', subtype='jpeg', filename=filename)

    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, password)  # Use the App Password here
            smtp.send_message(msg)
            return True, None  # No error if successful
    except Exception as e:
        return False, str(e)  # Return error message if failed

# Process the emails and certificates if submitted
if st.button('Send Certificates'):
    emails = emails_input.splitlines()
    
    if len(emails) != len(uploaded_files):
        st.error("Number of emails and certificates do not match. Please upload the same number of certificates as the emails provided.")
    else:
        # Sort uploaded files by their filenames (assuming the filenames are in the format 1.jpg, 2.jpg, etc.)
        uploaded_files = sorted(uploaded_files, key=lambda x: int(x.name.split('.')[0]))

        # Track results in a DataFrame
        results = []
        for email, file in zip(emails, uploaded_files):
            certificate_data = file.read()  # Read file data as binary
            success, error = send_certificate(email, certificate_data, file.name, sender_email, app_password)
            
            # Prepare the status
            status = 'Sent' if success else f'Failed: {error}'
            
            # Append to results
            results.append({'Email': email, 'Certificate Sent': file.name, 'Status': status})

        # Display the result in a table
        df = pd.DataFrame(results)
        st.dataframe(df)
