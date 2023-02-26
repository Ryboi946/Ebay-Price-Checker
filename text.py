import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv



def text_alert(subject, body, to, user, password): 
    #load_dotenv()   
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    msg['from'] = user
    
    


    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

    
    
    