def send_email(subject, body):
    import smtplib

    FROM = "c.tsialamanis@cellmobile.gr"
    TO = "c.tsialamanis@cellmobile.gr"
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("cellmobile.gr", 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(FROM, TO, message)
        server.close()
        print ("successfully sent the mail")
    except:
        print("failed to send mail")