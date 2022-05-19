import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import glob
import os
   
list_of_files = glob.glob('*.xlsx') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

def read(file):
    f = open(file, "r")
    content = f.read()
    f.close()
    return content

def mail():
    fromaddr = "automation.meraki@gmail.com"
    toaddr = "servier.network.in@capgemini.com"
    
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    
    # storing the senders email address  
    msg['From'] = fromaddr
    
    # storing the receivers email address 
    msg['To'] = toaddr
    
    # storing the subject 
    msg['Subject'] = "IE1-Ireland | AP Negotiating at 100Mbps Report"
    
    # string to store the body of the mail
    body = """
    <html>
      <body>
        <h5>Hello Team,<h5>
    
        <h5> Please find the attached report of AP's Negotiating at 100Mbps on IE1-Ireland Network.<h5>

        <h5>Regards,<h5>
        <h5>Meraki Automation<h5>
         </body>
    </html>
    """
    
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'html'))
    
    # open the file to be sent 
    filename = f'{latest_file}'
    attachment = open(f'{latest_file}', "rb")
    
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    
    # encode into base64
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(fromaddr, read("/home/ubuntu/private/myseckey.txt"))
    
    # Converts the Multipart msg into a string
    text = msg.as_string()
    
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    
    # terminating the session
    s.quit()

mail()
