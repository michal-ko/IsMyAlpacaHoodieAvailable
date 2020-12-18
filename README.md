# IsMyAlpacaHoodieAvailable
This script monitors Appalachian Gear Company website for hoodie availability and sends a notification email when provided search parameters are met and a hoodie is available to buy.

I have been trying to buy an alpaca hoodie from their website for nearly a year now and with no success. They have very limited stock and available every few months or so. Whenever new hoodies are available they are gone from the website within hours.

For the given reasons I decided to write a script that will monitor the website activity for me and send me an email when my hoodie is finally available. I thought I'd share this script with other people if anyone wants to get an alpaca hoodie from them. Hopefully it will increase your chances of buying it whlist it's available. Perfect gift for Christmas too!

## Prerequisits
1. This script requires at least Python 3.6
On how to install it on your system please follow to: https://www.python.org/downloads/

2. Install pip dependencies using: `pip3 install -r requirements.txt`

3. This script needs to be able to comunicate with your Gmail account. If you don't have 2 factor authentication set up with your Gmail account you don't need to do anything. Use your regular Gmail address and password. If you do however have 2 factor authentication set up (which, on a side note, you should) you'd have to set up app password with your Gmail account. To do it, visit your https://myaccount.google.com/apppasswords Here you'll have to choose Select app --> Mail and Select device --> Other (can call it i.e. Alpaca maaaail) Hit generate and you'll be presented with a 16 digit password. Save it somewhere safe as from now on when you use this script you will need that password.

## Running the script
In terminal run: `python3 main.py -h`
```
usage: main.py [-h] [-url URL] [-email EMAIL] [-size {Large,X-Large,XX-Large,Small,Medium}] [-colour {Charcoal,Olive,Watauga,Sanguine}] [-whatsinstock]
               [-checkfrequency CHECKFREQUENCY] [-testmail]

optional arguments:
  -h, --help            show this help message and exit
  -url URL
  -email EMAIL          email address at which you wish to be notified at. Insert in quotes "example@email.com"
  -size {Large,X-Large,XX-Large,Small,Medium}
                        desired size you're looking for
  -colour {Charcoal,Olive,Watauga,Sanguine}
                        desired colour you're looking for
  -whatsinstock         shows currently available stock
  -checkfrequency CHECKFREQUENCY
                        how often do you want to check for available stock
  -testmail             allows to test if this script can comunicate with Gmail on your machine
  ```
This shows all available options you can run this script with. 

# Testing your Gmail connectivity
I would suggest testing first if the script is able to sent you an email before actually kicking it off and leaving running for days just to realise when the hoodie was available you got an authentication error :)

To check if the script can talk to your Gmail account run the following mode. As you type the password it won't show up in the terminal.
`python3 main.py -testmail`
If you received an email that means you're good to go. Otherwise chack again your App Passwords in your Google Account settings.

# Run
An example command to run the script with would look like:
`python3 main.py -email example@mail.com -size "X-Large" -colour Olive`
And now is the waiting game...

# Checking all hoodie stock
`python3 main.py -whatsinstock`
