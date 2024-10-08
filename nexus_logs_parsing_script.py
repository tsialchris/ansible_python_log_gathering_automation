
import os

import json

# from network_objects import network_device
# from network_objects import network_interface
# from network_objects import connection
from checking_functions import check_line
from checking_functions import send_connection_notification
from parsing_functions import parse_parameters

#parse the script_parameters.txt
log_file_names_list = parse_parameters("script_parameters.txt")

json_devices = []

#if the network_devices.json file exists, parse it to get info
if os.path.isfile("./network_devices.json"):
    with open(r"network_devices.json", "r") as file:
        json_devices = json.load(file)


#go through each log file:
for file in log_file_names_list:
    #open the log files one by one
    #approaching from a per device basis
    #DEPLOYMENT
    f = open("./logs/" + file, "r")
    lines = f.readlines()

    #get the device's name from the log once
    #2024 Sep 12 17:46:34 VOLTON-SW-CORE-25G-202 %DAEMON-3-SYSTEM_MSG: NTP: Peer 193.93.164.195 is unreachable - ntpd[17871]
    first_split = lines[0].split("%")
    #RESULT:
    #2024 Sep 12 17:46:34 VOLTON-SW-CORE-25G-202 
    #DAEMON-3-SYSTEM_MSG: NTP: Peer 193.93.164.195 is unreachable - ntpd[17871]
    second_split = first_split[0].split(" ")
    #RESULT:
    #2024
    #Sep
    #12
    #17:46:34
    #VOLTON-SW-CORE-25G-202 
    device_name = second_split[4]
    
    #add the device to the list, if it is not already in:
    guard = False
    counter = 0
    for device in json_devices:
        #print(device)
        if device["name"] == device_name:
            guard = True
            #store the device's position to avoid going through the list every time
            device_position = counter
        counter = counter + 1
    #create a new object and add it to the list if it doesn't exist
    if guard == False:

        new_device = {"name": device_name, "interfaces": [], "connections": []}

        json_devices.append(new_device)

        #print(json_devices[0])
        #print(json_devices["name"][device_name])
        #print(json_devices)
        device_position = len(json_devices) - 1

    #print(device_position)

    # checking each line:
    for line in lines:
        # check line for this device
        json_devices[device_position] = check_line("ADJCHANGE", line, json_devices[device_position])

    # NOTIFICATIONS SENDING
    # after parsing the whole of the log file, check which notifications to send
    for device in json_devices:
        for network_connection in device["connections"]:
            if network_connection["state"] != network_connection["previous_state"]:
                #SEND-NOTIFICATION#
                send_connection_notification(network_connection)
            network_connection["previous_state"] = network_connection["state"]


f.close()

# write the output to a .json file
with open('network_devices.json', 'w', encoding='utf-8') as f:
    json.dump(json_devices, f, ensure_ascii=False, indent=4)