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


'''
sender = 'jojokr94@gmail.com'
receivers = ['kraemer.johannes.p@gmail.com']

message = f"""From: Jobs <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: New Job at <Company>

Job-Title: <Job Title>
Job-Team: <Job Team>
"""

message2 = f"""From: Jobs <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: New Job at <Company> 2

Job-Title: <Job Title>
Job-Team: <Job Team>
"""

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login('jojokr94@gmail.com', 'jJWyERH88E6%Em^5i^!8CmXrG$@QiM2')
server.sendmail(sender, receivers, message)
server.sendmail(sender, receivers, message2)
'''
