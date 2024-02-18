import smtplib
import ssl
import argparse
import os
import logging
import subprocess

# logging config
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

# get gmail info from environment variables
gmail_user = os.environ["gmail_user"]
gmail_password = os.environ["gmail_password"]

# gather ip info
default_ip = subprocess.run(["/usr/bin/curl", "ifconfig.me"], capture_output=True, text=True)
parser = argparse.ArgumentParser()
parser.add_argument('--ip', help='new ip address (default = curl ifconfig.me)', default=default_ip.stdout)
args = parser.parse_args()


def send_mail(message):
    context = ssl.create_default_context()  # CREATE SECURE CONTEXT (CERTIFICATES)
    port = 465  # FOR SSL
    smtp_server = 'smtp.gmail.com'

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(gmail_user, gmail_password)
        try:
            server.sendmail(gmail_user, gmail_user,
                            message)  # SEND EMAIL FROM MYSELF TO MYSELF
            logging.info('mail sent')
        except:
            logging.critical('Unable to send')
            server.close()


def file_stuff(mode):
    try:
        with open("ip_address.txt", mode) as h:
            if mode == "w":
                logging.debug("writing to file")
                h.write(args.ip)
            else:
                logging.debug("reading file")
                return h.read()
    except FileNotFoundError:
        logging.info("file not found, creating new file")
        return "init"


def main():

    old_ip = file_stuff("r")
    if old_ip != args.ip:
        logging.info("ip address different, sending main and updating local file")
        send_mail(args.ip)
        file_stuff("w")


if __name__ == '__main__':
    main()
