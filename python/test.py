#!/usr/bin/python3
"""
:Description:  Module implements the search of the error logs and send email
               notification in case any error traced.
"""

import os
import sys
import yaml
import logging
from pprint import pformat
import argparse
from configparser import ConfigParser
import subprocess
import shlex
from datetime import date, datetime
from configparser import ConfigParser

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

today_date = None
#root_path = "/home/sramasudha/logs"
root_path = "/opt/TA/agentlog/"
ta_config_log_file = "ta_configuration.log"
ta_config_interface_log_file = "ta_configure_interfaces.log"
mail_body_file_path = "/tmp/monitoring_mail_body"
monitoring_log_path = "/var/log/error_monitoring.log"
config_file = "ta-log-monitor-config.yaml"

mail_subject = "Error detected in the ta-core logs path !!"


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
            # instance of MIMEMultipart
            message = MIMEMultipart()
            sender = str(user) + "<" + \
                str(email_sender) + ">"
            message["SUBJECT"] = subject
            message["FROM"] = sender
            message["TO"] = ", ".join(recipients)

            # attach the body with the msg instance
            message.attach(MIMEText(msg, 'plain'))

            # open the file to be sent
            filename = "/tmp/test_ta_grep.log"
            attachment = open(filename, "rb")

            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')

            # To change the payload into encoded form
            p.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(p)

            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # attach the instance 'p' to instance 'msg'
            message.attach(p)

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


def find_all_files(name, path):
    result = []
    try:
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        return result
    except BaseException as e:
        logging.error("Failed-finding-files: {}".format(e))
        sys.exit(1)


def search_in_log(filename, root_path, search_string, attachment_filename):
    global today_date
    found_files = find_all_files(filename, root_path)
    results = {}
    for file_name in found_files:
        # insert today date in the grep command
        grep_cmd = "egrep -Hn --color -A 5 -B 5 '{} .*{})'".format(today_date, "|".join(search_string))
        # grep_cmd = grep_cmd.format(today_date)

        # Append file path to the grep command
        grep_cmd = grep_cmd + " " + file_name + " >> " + attachment_filename
        try:
            run = subprocess.Popen(shlex.split(grep_cmd), stdout=subprocess.PIPE)
            stdout = run.stdout.read()
        except BaseException as e:
            logging.error("Failed-running-grep-command: {}".format(e))
            sys.exit(1)

        if stdout.decode("utf-8") != '':
            results[file_name] = stdout.decode("utf-8")
    ret_value = {}
    ret_value[filename] = {"error_detected_file_count": len(results)}
    logging.info("Error-detected-file-count: {}, filename: {}".format(len(results), filename))
    return ret_value


def execute_task(task):
    filenames = task["files"]
    root_path = task["path"]
    search_string = task["search_string"]
    attachment_filename = task["attachment_filename"]
    status = []
    for filename in filenames:
        ret_values = search_in_log(filename, root_path, search_string, attachment_filename)
        status.append(ret_values)
    return status


def main():
    global today_date
    # Get today's date
    today_date = date.today().strftime("%Y/%m/%d")

    # Configure log level
    logging.basicConfig(level=logging.INFO,
                        filename=monitoring_log_path,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Get configurations
    # config = ConfigParser()
    # config.read(config_file)
    config = None
    with open(config_file) as fp:
        config = yaml.load(fp)
    mail_config = config.get('email')
    mail_sender = mail_config['sender']
    mail_recipients = mail_config['recipients']
    smtp_config = config.get('smtp')
    smtp_server_address = smtp_config['smtp-ip']
    smtp_port = smtp_config['smtp-port']
    tasks = config.get('tasks')

    # Initialize Mail utils
    mailer = MailUtils(smtp_server_address, smtp_port)

    # Search for error logs
    task_status = []
    for task in tasks:
        status = execute_task(task)
        task_status.append(status)

    #ta_config_search_results = search_in_log(ta_config_log_file)
    #ta_config_interface_search_results = search_in_log(ta_config_interface_log_file)

    #ta_config_files = pformat(list(ta_config_search_results.keys()), compact=True, width=1)
    #ta_config_interface_files = pformat(list(ta_config_interface_search_results.keys()), compact=True, width=1)

    formatted_task_status = pformat(task_status, compact=True, width=1)

    # Frame mail body based on the search results
    with open(mail_body_file_path, "w") as fp:
        fp.write("Below are the log files on the ta-core machine, detected with error logs\n")
        current_time = datetime.now().strftime("%H:%M:%S")
        fp.write("Date: {} Time: {}\n\n".format(today_date, current_time))
        fp.write("Error detected in below ta_configuration logs\n")
        fp.write(formatted_task_status)
        # fp.write("\n\nError detected in below ta_configure_interfaces logs\n")
        # fp.write(ta_config_interface_files)
    logging.info("Mail-body-is-written-into-temporary-file: {}".format(mail_body_file_path))

    # os.system("mailx -s '{}' '{}' < {}".format(mail_subject, mail_recepients, mail_body_file_path))

    msg = ''
    with open(mail_body_file_path, "r") as fp:
        msg = fp.read()

    status = mailer.send_email(msg, mail_subject, mail_sender, mail_recipients)
    if status["STATUS"] == "FAILURE":
        logging.error("Failed-to-send-Email")


if __name__ == '__main__':
    main()
