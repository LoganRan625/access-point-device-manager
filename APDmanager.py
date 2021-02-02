#!/bin/python3

# --------------------Access Point Device Manager------------------
# this file is used like a doorbell, when a personal device gets close to your access point
# and connects it will send a message to your phone with the name of the person
#  
# it can also be used to auto kick devices you dont have saved here, this part has not been tested.
# and probably doesnt work, but will tell you in the file '/etc/rc.local/list_MAC.txt' those devices.

# must have twilio account, add account info and phone numbers where needed
# replace name1, 2, 3, 4, 5, with any name and write there MAC inside qoutes
# add all known and trusted device MAC addresses that will connect to your Access Point to "known_MACs" list
# 
# run file on startup, still having issues 
# tried in /etc/rc.local and .bashrc which works but runs everytime you open a window, as well as in profile.d 
# which has its own set of problems

from twilio.rest import Client
import time
import os
import sys
import subprocess
import re


# list all known and trusted MACs here except for the personal devices in name variables
known_MACs = ['mac address here', 'mac address here']
# these lists should be empty 
new_MACs = []
active_MACs = []

# variables for  home devices

# variables for peoples personal devices
name1 = 'mac here'
name2 = 'mac here'
name3 = 'mac here'
name4 = 'mac here'
name5 = 'mac here'
known_devices = [name1, name2, name3, name4, name5]

def kicking(bad_device):
    global BSSID
    try:
        os.system("ifconfig wlan0 down")
        os.system("airmon-ng start wlan0")
        os.system("ifconfig wlan0mon up")
        write_to_file("monitor mode started")
    except:
        write_to_file("Error: with monitor mode, in kicking(bad_device) block")
    for i in range(50):
         # need to remove quotes before deauthentication
        write_to_file(bad_device)
        BSSID = str(BSSID).strip("'")
        bad_device = str(bad_device).strip("[']")
        write_to_file(bad_device)
        try:
            os.system("aireplay-ng --deauth 2 -a " + BSSID + " -c " + bad_device + " wlan0mon")
        except:
            write_to_file("Error: with deauthentication process, interupted")

    try:
        os.system("ifconfig wlan0mon down")
        os.system("airmon-ng stop wlan0mon")
        os.system("ifconfig wlan0 up")
        write_to_file("finished kicking, will try again if device decides to connect")
    except:
        write_to_file("Error: with turning off monitor mode")

# will create 'list_MAC.txt' file in the directory this file is run
def write_to_file(text):
    with open('list_MAC.txt', 'a') as file:
        sys.stdout = file
        print(text)
        file.close()

counter = 0
tag = False
def check_status(device_name, mac_address, active_MACs, mac, date):
    global tag
    global counter
    # which device?
    if device_name == name1:
        name = 'name1'
    elif device_name == name2:
        name = 'name2'
    elif device_name == name3:
        name = 'name3'
    elif device_name == name4:
        name = 'name4'
    elif device_name == name5:
        name = 'name5'
    #add more names here
    else:
        write_to_file("Error: in check_status(device_name), device_name issue, unsure of 'name'. likely 'name' has not been added to function 'check_status()' ")
    #-----------------------------
    if device_name in active_MACs:
        if tag == False:
            tag = True
            write_to_file(name + " " + device_name + " connected to your Access Point")
            # place for sending message to phone
            send_message(name + " connected to your Access Point")
    if device_name in active_MACs:
        if device_name not in mac_address:
            counter += 1
            if counter >= 3000: # 50 iterations = 1 minute, 3000 = 1 hour
                MainLoop()
            if counter == 3000:
                tag = False
                counter = 0
                active_MACs.remove(device_name)
                write_to_file(device_name + " has not been active for 1 hour " + str(date))

switch = False         
         
def MainLoop():
    while True:
        # scanning network, extracting MAC addresses from string 'mac', printing info to '/etc/rc.local/list_MAC.txt'
        mac = os.popen('arp-scan -l').read() 
        mac = str(mac)
        date = os.popen('date').read()
        mac_address = re.findall(r'[a-zA-Z0-9][a-zA-Z0-9]\:[a-zA-Z0-9][a-zA-Z0-9]\:[a-zA-Z0-9][a-zA-Z0-9]\:[a-zA-Z0-9][a-zA-Z0-9]\:[a-zA-Z0-9][a-zA-Z0-9]\:[a-zA-Z0-9][a-zA-Z0-9]', mac)
        for i in mac_address:
            if i not in known_MACs:
                if i not in new_MACs:
                    new_MACs.append(i)
                    write_to_file("new MACs " + str(new_MACs))
                    write_to_file("UNKNOWN MAC added " + str(i) + " " + str(date))
                if i not in active_MACs:
                    active_MACs.append(i)
                    write_to_file("Active MACs " + str(active_MACs) + " " + str(date))
#from here to end, is new may have spacing syntax errors 
                if i in new_MACs:
                    if i not in known_devices:
                        if i in active_MACs:
                            if switch == False:
                                switch = True
                                write_to_file(str(i) + " is an unknown device! it has been added to new_MACs" + str(date))
                                send_message(str(i) + " is an  unknown device! it has connected to your Access Point")
                                write_to_file(mac)
                                    
                        if i not in active_MACs:
                             switch = False
                                    
# end  december 8th 2020


            # checking for personal devices           
            if i in known_devices:
                check_status(i, mac_address, active_MACs, mac, date)

# from here to end is new, may have syntax errors regarding spacing
            if i in active_MACs:
                if i not in known_devices:
                    if i not in mac_address:
                        Main_count += 1
                        if Main_counter != 50:
                            MainLoop()
                        else:
                            Main_counter = 0
                            active_MACs.remove(i)
                            write_to_file(str(i) + " has been removed from active MACs")
                            write_to_file(active_MACs)      
# end december 8th 2020
 
            if i not in known_MACs and i not in known_devices:
                  write_to_file("an unknown device has connected to your network" + str(i) + " " + str(date))
                  write_to_file(mac)
                  write_to_file("Device Needs approval, Kicking device...")
                  kicking(str(i))

#----------------------------------------------------------------------------
# TWILIO, need twilio account
def send_message(text_message):
    account_number = 'account_number_here'
    token = 'token_here'
    twilio_number = 'twilio_phone_number_here'
    my_phone = 'personal_cell_number_here'
    client = Client(account_number, token)
    client.messages.create(to=my_phone, from_=twilio_number, body=text_message)

MainLoop()
