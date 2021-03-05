#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText


class MailUtils(object):
    """Module implemets send email function for E-mail notification service."""

    def __init__(self, smtp_ip, smtp_port):
        """Initialize of class."""

        # Get smtp server IP and port number
        logging.info("Smtp-ip-and-port: {} {}".format(smtp_ip, smtp_port))
        self.smtp_ip = smtp_ip
        self.smtp_port = smtp_port

    def send_email(self, msg, subject, email_sender, recipients):
        """
        Send mail notification to the receipient(s).
        """
        try:
            retval = {}

            logging.info("Configured-email-recipients: {}".format(recipients))

            # split the username
            user = email_sender.split('@')[0]
            message = MIMEText(msg)
            sender = str(user) + "<" + \
                str(email_sender) + ">"
            message["SUBJECT"] = subject
            message["FROM"] = sender
            message["TO"] = ", ".join(recipients)

            # set the smtp server IP and port
            mailserver = smtplib.SMTP(self.smtp_ip,
                                      self.smtp_port)
            mailserver.ehlo()

            # send email using 'sendemail' API. API would raise
            # an exception if it is failed
            mailserver.sendmail(sender, recipients,
                                message.as_string())
            logging.info("Successfully-sent-email")
            retval["STATUS"] = "SUCCESS"
        except smtplib.SMTPException as e:
            logging.error("Unable-to-send-Email-Smtplib-exception: {}".format(e))
            retval["STATUS"] = "FAILURE"
        except BaseException as e:
            logging.error("Unable-to-send-Email-unknown-exception: {}".format(e))
            retval["STATUS"] = "FAILURE"
        return retval

if __name__ == '__main__':
    # Initialize Mail utils
    mailer = MailUtils(smtp_server_address, smtp_port)

    status = mailer.send_email(msg, mail_subject, mail_sender, mail_recipients)
    if status["STATUS"] == "FAILURE":
        logging.error("Failed-to-send-Email")
