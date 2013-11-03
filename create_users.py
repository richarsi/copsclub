# usage: ./bin/instance -OPlone run create_users.py user.csv
import csv
import os
import sys, logging
import transaction
from os import environ
from StringIO import StringIO
from plone import api

email_template = """
We have updated the COPS website into a fresh more modern format which we hope you will find easier to use.
 
In order to access the new site you have been allocated a new username. The username for {fullname} is {username}.
 
We have tried to send this information to the 'preferred' contact but many of our records do not contain this information therefore we have taken the first recorded email address as the contact point. If you would like to change this to another email address please send a message to Jane Leigh via the committee pages on the new website.
 
We have compiled this information from the old website. If you have informed us of a change to your details on the new squad packs we have been unable to input this yet so we apologise for any inconvenience.

What do you need to do next?
----------------------------
Go to the COPS website (www.copsclub.co.uk) and click on the Log in button. Where it says \"Forgot your password?\" click on the text \"we can send you a new one.\". Complete the \"Lost Password\" form with your username* and an email will be sent to you with instructions to create your password. If you have difficulties then contact the site administrator using the contact form on the site.

* your user name is case sensitive and you must enter capitals for the letters.
"""

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root_logger.addHandler(handler)


# prepare a dictionary of the users on the site
users = {}
for user in api.user.get_users():
    users[user.getUserName()] = user

# get command line args
for file in sys.argv[1:]:
    # process the csv file
    root_logger.debug("Starting to process file %s", file)
    rownum = 0
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            # save header row
            # Last,First,Squad,Initials,ASA Number,User Name,Parent Email 1
            if rownum == 0:
                header = row
            elif len(row)==7:
                last = row[0].strip()
                if last == "":
                    root_logger.warn("Row %s has no last name", rownum)
                    continue
                first = row[1].strip()
                if first == "":
                    root_logger.warn("Row %s has no first name", rownum)
                    continue
                squad = row[2].strip()
                if squad == "":
                    root_logger.warn("Row %s has no squad", rownum)
                    continue
                initials = row[3].strip()
                if initials == "":
                    root_logger.warn("Row %s has no initials", rownum)
                    continue
                asanumber = row[4].strip()
                if asanumber == "":
                    root_logger.warn("Row %s has no asa number", rownum)
                    continue
                username = row[5].strip()
                if username == "":
                    root_logger.warn("Row %s has no username", rownum)
                    continue
                email = row[6].strip()
                if email == "":
                    root_logger.warn("Row %s has no email", rownum)
                    continue
                else:
                    fullname = first + " " + last
                    properties = dict(
                        fullname = fullname,
                    )
                    if users.has_key(username):
                        root_logger.warn("User \'%s\' already exists ... skipping",username)
                    else: 
                        root_logger.debug("Creating user \'%s\' with user id \'%s\' and email \'%s\'.", fullname, username, email)
                        transaction.begin()
                        user = api.user.create(
                            username=username,
                            email=email,
                            properties=properties,
                          )
                        transaction.commit()
                        api.portal.send_email(recipient=email,
                                      subject="COPS Website Registration", 
                                      body=email_template.format(fullname=fullname,
                                                              username=username))
            else:
                root_logger.warn("Row %s has %s values instead of the 7 expected.", rownum, len(row))
    
            rownum += 1
    
