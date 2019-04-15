import smtplib
# activate less secure apps with this link
# https://myaccount.google.com/lesssecureapps


class EmailService:
    __slots__ = 'email_server', 'sender', 'receivers'

    def __init__(self, host, port, sender, receivers):
        self.email_server = smtplib.SMTP_SSL(host, port)
        self.sender = sender
        self.receivers = receivers

    def login(self, pw):
        self.email_server.ehlo()
        self.email_server.login(self.sender, pw)

    def send_message(self, message):
        self.email_server.sendmail(self.sender, self.receivers, message)

    def send_messages(self, messages):
        map(self.send_message, messages)
