def send_email(subject, body):
    import smtplib


    # from email.message import EmailMessage

    # msg = EmailMessage()
    # msg["From"] = "originalflamedragon@gmail.com"
    # msg["Subject"] = subject
    # msg["To"] = "tsialchris@gmail.com"
    # msg.set_content(body)
    # msg.add_attachment(open("aggregate_report.txt", "r").read(), filename="aggregate_report.txt")

    # s = smtplib.SMTP("smtp.gmail.com", 587)
    # s.login(usr, password)
    # s.send_message(msg)

    FROM = "c.tsialamanis@cellmobile.gr"
    TO = "c.tsialamanis@cellmobile.gr"
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.cellmobile.gr", 587)
        server.ehlo()
        server.starttls()
        # server.login(username, password)
        server.login("c.tsialamanis@cellmobile.gr", "16c61t16c61tET@volton")
        server.sendmail(FROM, TO, message)
        server.close()
        print ("successfully sent the mail")
    except:
        print("failed to send mail")