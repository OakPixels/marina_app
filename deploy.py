from flask import Flask, session, render_template, request, redirect, url_for
import pandas
import json
import datetime
from xlrd import XLRDError
import imaplib
import base64
import os
import email

app = Flask(__name__)

app.secret_key = b'_8#h4A"S2W9z\n\xec]/'


def getsheet(file):
    now = datetime.datetime.now()
    month = now.strftime("%B")

    # Go through last 10 days to find most recent sheet
    for backdate in range(10):
        sh_day = (datetime.datetime.today().day - backdate)
        if sh_day % 10 == 1:
            des = 'st '
        elif sh_day == 13:
            des = 'th '
        elif sh_day % 10 == 2:
            des = 'nd '
        elif sh_day % 10 == 3:
            des = 'rd '
        else:
            des = 'th '
        last_sheet = str(sh_day)+des+month
        try:
            excel_data_df = pandas.read_excel(file, sheet_name=last_sheet, usecols=['Loc A', 'Boat Name A', 'Type A', 'Length A', 'Owner A', 'Remark A', 'Phone A', 'Paid A'])
        except XLRDError:
            print("Sheet not accessible")
            continue
        session['yday'] = sh_day
        return last_sheet

    return render_template("error.html", name='No sheet found')


def checkemail():
    # This email downloader is the only third party section and was built by Sanket Doshi
    email_user = '****'
    email_pass = '****'

    mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
    mail.login(email_user, email_pass)
    type, data = mail.select('[Gmail]/Starred')
    mail_ids = data[0]
    id_list = mail_ids.split()
    # print(data[0])

    # Get last email (data[0])
    type, data = mail.fetch(data[0], '(RFC822)' )
    raw_email = data[0][1]
    # converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # download attachments
    for part in email_message.walk():
        # this part comes from the snipped I don't understand yet...
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        filePath = os.path.join('/Users/Joe/web/marina/static', fileName)
        fp = open(filePath, 'wb')
        fp.write(part.get_payload(decode=True))
        fp.close()
        print("Downloaded: " + fileName)


def get_boats():
    print("getting boat data")
    # Check if already got the data
    if session.get('boats') is not None:
        print("already got boat data")
        return render_template("index.html", boats=json.dumps(session['boats']))

    # FULL VERSION takes updates from emails with excel attachments
    # checkemail()

    # Set path
    excel_path = ('static/demo.xlsx')

    # Check file exists
    if not os.path.isfile(excel_path):
        return render_template("error.html", name='No file found')

    # FULL VERSION Gets sheet for today
    # last_sheet = getsheet(excel_path)
    last_sheet = "20th April"
    session['date'] = last_sheet

    boats = []
    # iterate through excel columns to consolidate data to boats
    for i in range(4):
        # Skip B column
        if i == 1:
            continue
        else:
            column = chr(i+65)

        # read excel
        excel_data_df = pandas.read_excel(excel_path, sheet_name=last_sheet, usecols=['Loc '+column, 'Away '+column, 'Boat Name '+column, 'Type '+column, 'Length '+column, 'Owner '+column, 'Remark '+column, 'Phone '+column, 'Paid '+column])
        boats_raw = excel_data_df.to_dict(orient='records')

        # Add each column to boats array and change keys and remove empty cells
        for boat in boats_raw:
            boat['Boat Name'] = boat['Boat Name '+column]
            del boat['Boat Name '+column]
            boat['Length'] = boat['Length '+column]
            del boat['Length '+column]
            boat['Type'] = boat['Type '+column]
            del boat['Type '+column]
            boat['Loc'] = boat['Loc '+column]
            del boat['Loc '+column]
            boat['Away'] = boat['Away '+column]
            del boat['Away '+column]
            boat['Owner'] = boat['Owner '+column]
            del boat['Owner '+column]
            boat['Remark'] = boat['Remark '+column]
            del boat['Remark '+column]
            boat['Phone'] = boat['Phone '+column]
            del boat['Phone '+column]
            boat['Paid'] = boat['Paid '+column]
            del boat['Paid '+column]
            # remove empty cells and excel legend
            if (boat['Boat Name']) == (boat['Boat Name']):
                if (boat['Boat Name']) != 'Blue ' and (boat['Boat Name']) != 'Black' and (boat['Boat Name']) != 'Grey' and (boat['Boat Name']) != 'Boat name' and (boat['Boat Name']) != 'Payment details last checked 13/2':
                    boats.append(boat)

    # save boats array to session
    session['boats'] = boats
    print('data grab successful')
    return render_template("index.html", boats=json.dumps(boats))


# URL Routes
@app.route("/")
def index():
    # session.pop('boats', None)
    if 'username' not in session:
        return render_template("login.html")
    return get_boats()

@app.route("/reload")
def reload():
    session.pop('boats', None)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    session['username'] = "User"
    print(session['username'])
    return redirect("/")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("login.html")
