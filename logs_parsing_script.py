
import os

import json

# from network_objects import network_device
# from network_objects import network_interface
# from network_objects import connection
from checking_functions import check_line
from checking_functions import send_connection_notification
from parsing_functions import parse_parameters
from parsing_functions import parse_nexus_name
from parsing_functions import device_lookup
from parsing_functions import device_check

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
    f = open("./logs/" + file, "r")
    lines = f.readlines()

    
    if "8000v" in file:
        # if this is is an 8000v device, the log does not include its name
        # get it from the filename
        device_name = file.split(".")[0].upper()
    else:
        # get the device's name from the log once
        device_name = parse_nexus_name(lines[0])

    # add the device to the "json_devices", if it is not already in
    json_devices = device_check(json_devices, device_name)

    # return its position
    device_position = device_lookup(json_devices, device_name)
    
    

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