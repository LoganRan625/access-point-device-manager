# access-point-device-manager
    recieve a text notification about the status of a devices connecting to your access point.
    devices that are not in your list of known devices will be kicked from your AP and you will 
    be notified thru text message. 


***
**Dependencies include** 
   
    arp-scan
    airmon-ng
    aireplay-ng
    python3
    a Twillio account
    
PIP PACKAGES

    subprocess
    re (regular expressions)
    sys

***
**Installation**
    
    in order to work you will need to sign up for a twillio account and add all nessesary MAC information for your devices
    if you wish to complete this without a twillio account, comment out send_message() and all lines of code within the function
    as well as each function call, (line 102, 139) you can always check the file 'list_MAC.txt' for log info. 

***
**Issues**
 
    Becuase of issues i have been unable to resolve the program is unfisnished runs with an exit status of 1!
    the program typicaly runs for an average of 30 mins to 3 hours then stops working, based on issues related 
    to errors in arp-scan which i have been unable to get to the bottom of.
    
    I will be remodeling this program using static ip addresses to ping instead 
    of using arp-scan -l for checking mac addresses hopefully removing the issue.
    
***

    
