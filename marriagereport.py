"""
To create weekly marriage report for Gainesville Sun.
On a monthly basis:
1. Create PDF of prior month's marriages at
http://isol.alachuaclerk.org/RealEstate/SearchEntry.aspx?e=newSession
2. Download PDF to working folder and convert to csv with pdf_to_csv.py
3. Run this script on that csv file.


"""


# standard libraries
import csv
import os

# installed with pip
from email.message import EmailMessage
import smtplib
import numpy as np
import pandas as pd

# custom module
import creds

# select rows in a date range
start_date = '05/20/2019'
end_date = '05/26/2019'

# who gets the email
receiver = 'doug.ray@starbanner.com'

# create dataframe from csv
cols = [
    'col1', 'date', 'col3', 'col4', 'col5', 'col6', 'col7',
    'name1', 'col9', 'col10', 'name2', 'col12', 'col13',
    'col14', 'col15'
    ]

df = pd.read_csv('output.csv',
    usecols=[1, 7, 10, 14],
    names=cols,
    encoding='ISO-8859-1'
    )

# get rid of unneeded rows
df = df[df.col15 != "Temp"]
df = df[df.col15 != "Status"]
df = df.dropna(axis=0, how='all')
df = df.dropna(subset=['name1', 'name2'])
df = df.dropna(subset=['date'])
df = df.drop('col15', axis=1)

# get names separated and organized
df.name1 = df.name1.str.title()
df.name2 = df.name2.str.title()
name1split = df.name1.str.split(" ", n=1, expand=True)
df['name1_last'] = name1split[0]
df['name1_first'] = name1split[1]
df = df.drop('name1', axis=1)
name2split = df.name2.str.split(" ", n=1, expand=True)
df['name2_last'] = name2split[0]
df['name2_first'] = name2split[1]
df = df.drop('name2', axis=1)
df = df[['name1_last', 'name1_first', 'name2_last', 'name2_first', 'date']]
df['name1'] = df[['name1_last', 'name1_first']].apply(lambda x: ', '.join(x),
    axis=1)
df['name2'] = df[['name2_last', 'name2_first']].apply(lambda x: ', '.join(x),
    axis=1)
df['couple'] = df[['name1', 'name2']].apply(lambda x: ' and '.join(x), axis=1)
df = df.drop([
    'name1_first',
    'name1_last',
    'name2_first',
    'name2_last',
    'name1',
    'name2'
    ], axis=1)

# filter for the date range
df.date = pd.to_datetime(df.date)
mask = (df.date >= start_date) & (df.date <= end_date)
df_chosenrange = df.loc[mask]
df_chosenrange = df_chosenrange.drop('date', axis=1)
df_chosenrange

# get ready to write the report for publication
marriagereport = os.path.join(path_directory, 'marriages.txt')

# Delete old report file since we'll be building a new one here.
if os.path.exists(marriagereport):
    os.remove(marriagereport)
else:
    print(f"The old file for {marriagereport} isn't there.")

# Add intro graph to the top
intro = f"These are marriage licenses recorded in Alachua County — from
    {start_date} to {end_date}\n"

f=open(marriagereport, "w+")
f.write(intro)
f.close()

# write df to txt file
np.savetxt(r'marriage.txt', df_chosenrange.values, fmt='%s')

# send the email
# send the email
with open('marriages.txt') as fp:
    msg = EmailMessage()
    msg.set_content(fp.read())

sender = 'data@sunwriters.com'
msg['Subject'] = f'Marriage licenses for Alachua County from {start_date} to {end_date}'
msg['from'] = sender
msg['To'] = receiver

        # Send the message via our own SMTP server.
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(sender, gmail_password)
    server.send_message(msg)
    server.quit()
    print('Email sent!')
except:
    print('Something went wrong...')
