import re
import sys
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
import smtplib
import argparse
import getpass


class Product:
    def __init__(self, size=None, colour=None, availability=None):
        self.size = size
        self.colour = colour
        self.availability = availability


parser = argparse.ArgumentParser()
parser.add_argument("-url",
                    default="https://appalachiangearcompany.com/collections/mens/products/mens-all-paca-fleece-hoodie?variant=37538073051334&utm_source=newsletter&utm_medium=email&utm_campaign=earlyDec_inventoryalert&utm_content=menshoodies&goal=0_9cced955d3-074039e033-414922245&mc_cid=074039e033&mc_eid=0fbdc7b9be")
parser.add_argument("-email",
                    help="email address at which you wish to be notified at. Insert in quotes \"example@email.com\"")
parser.add_argument("-size", choices={'Small', 'Medium', 'Large', 'X-Large', 'XX-Large'},
                    help="desired size you're looking for")
parser.add_argument("-colour", choices={'Charcoal', 'Olive', 'Sanguine', 'Watauga'},
                    help="desired colour you're looking for")
parser.add_argument("-whatsinstock", action='store_true', help="shows currently available stock")
parser.add_argument("-checkfrequency", default=30, help="how often do you want to check for available stock")
parser.add_argument("-testmail", action='store_true',
                    help='allows to test if this script can comunicate with Gmail on your machine')
args = parser.parse_args()


def send_gmail_email(sender_addr, password, body):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()  # encrypts the msg
            smtp.ehlo()
            smtp.login(sender_addr, password)
            body = body
            msg = f"Subject: The Appalachian Alpaca hoodie you want is available!\n\n{body}"
            smtp.sendmail(sender_addr, sender_addr, msg)
    except smtplib.SMTPAuthenticationError as ae:
        print("You might have forgotten to change a few settings in your Gmail account to receive emails from Python scripts")
        print(f"Username and Password not accepted: {ae}")
        sys.exit(-1)
    except Exception as exc:
        print(exc)
        sys.exit(-1)


def test_sending_email(sender_addr, password):
    body = "Don't get too excited. This is only a test email checking if the script can send emails to your Gmail." \
           " If you see it in you email box then you will get notified when your desired hoodie configuration is" \
           " available."
    send_gmail_email(sender_addr, password, body)


def get_page_content(website_addr):
    page = requests.get(website_addr)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id="js-product-form--3695823192148")
    results = results.find_all('div', class_="product-single__variant")
    results = str(results).split('\n')
    return results


def analise_results(results):
    for res in results:
        obj = re.findall(r'option', str(res))
        if len(obj) == 2:
            cleanedup = re.search(r'>(.*)<', str(res)).group(1)
            new_prod = Product()
            # check availability
            if bool(re.search(r'Sold Out', cleanedup)):
                new_prod.availability = False
            else:
                new_prod.availability = True
            # get size
            new_prod.size = cleanedup.split()[0]
            # get colour
            new_prod.colour = cleanedup.split()[2]
            all_products.append(new_prod)


if __name__ == "__main__":
    all_products = list()

    if args.testmail:
        _email = input("Type your Gmail address and press Enter: ")
        _pass = getpass.getpass(prompt=f"Type your password and press Enter: ")
        test_sending_email(_email, _pass)
        print("Email sent. Check your mailbox.")
        sys.exit()

    if args.whatsinstock:
        pc = get_page_content(args.url)
        analise_results(pc)
        for elem in all_products:
            print(elem.__dict__)
    else:
        # CLI argument check
        if not (args.email and args.size and args.colour):
            print("You need to provide arguments: -email, -size, -colour. For more help run: python3 main.py -h")
            sys.exit(0)
        password = getpass.getpass(prompt=f"Type your Gmail password for {args.email} and press enter: ")
        print(f"{datetime.now()} Waiting for availability: {args.size}, {args.colour}...")
        while True:
            pc = get_page_content(args.url)
            analise_results(pc)
            # check if there is a model you're looking for
            for prod in all_products:
                if prod.size == args.size and prod.colour == args.colour and prod.availability:
                    # found a match. Send email
                    print(f"Item available: {prod.__dict__}")
                    print("Sending email notification")
                    # send email
                    send_gmail_email(args.email, password, str(prod.__dict__))
                    break
            # else clear the list
            all_products.clear()
            # and wait
            time.sleep(args.checkfrequency)
