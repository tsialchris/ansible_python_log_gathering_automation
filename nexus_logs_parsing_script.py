
import os

import json

from network_objects import network_device
from network_objects import network_interface
from network_objects import connection
from network_functions import check_for_element

#list with all network devices with logs
#will contain network_device objects
network_devices_list = []

#parse the script_parameters.txt
#DEPLOYMENT
#f = open(r"C:\Users\c.tsialamanis\Desktop\ansible-logs-python\script_parameters.txt", "r")
f = open(r"C:\Users\Chris\Desktop\ansible_python_log_gathering_automation-main\script_parameters.txt", "r")
#f = open("script_parameters.txt", "r")

#read all the lines and store them in "lines"
lines = f.readlines()

#store all the log file names in an array
log_file_names_list = [] 
log_file_names_found = False

#loop through the file line by line
for line in lines:

    if line == "}":
        log_file_names_found = False

    if log_file_names_found == True:
        log_file_names_list.append(line.strip())

    if line.strip() == "LOG_FILE_NAMES{":
        log_file_names_found = True

f.close()

#print(*log_file_names_list)



#BLOCK 1

#if the network_devices.json file exists, parse it to get info
#DEPLOYMENT
#if os.path.isfile("./network_devices.json"):
if True:
    #DEPLOYMENT
    #with open(r"network_devices.json", "r") as file:
    #with open(r"C:\Users\c.tsialamanis\Desktop\ansible-logs-python\network_devices.json", "r") as file:
    with open(r"C:\Users\Chris\Desktop\ansible_python_log_gathering_automation-main\network_devices.json", "r") as file:
        json_devices = json.load(file)

    #print(json_devices[0])
    #print(json_devices[0]['name'])
    #print(json_devices[0]['interfaces'][0])

    #print(json_devices)

#BLOCK 1 - END

#go through each log file:
#BLOCK 2
for file in log_file_names_list:


    #open the log files one by one
    #approaching from a per device basis
    #DEPLOYMENT
    #f = open(r"C:\Users\c.tsialamanis\Desktop\ansible-logs-python\logs\athe-93180-101.log")
    f = open(r"C:\Users\Chris\Desktop\ansible_python_log_gathering_automation-main\logs\athe-93180-101.log")
    #f = open("./logs/" + file, "r")
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


    for line in lines:
        #print(network_devices_list[device_position].connections[0].type)
        try:
            #check for BGP Adjacency Changes
            if "ADJCHANGE" in line:
                #print("in ADJ")
                #2024 Sep 19 14:11:23 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) neighbor 10.116.27.1 Down - recv:  other configuration change
                #2024 Sep 19 14:11:34 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) neighbor 10.116.27.1 Up
                #2024 Sep 23 13:44:21 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) neighbor 10.116.27.1 Down - recv:  session closed
                #2024 Sep 23 13:44:38 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) neighbor 10.116.27.1 Up
                first_split = line.split(" neighbor ")
                #RESULT:
                #2024 Sep 19 14:11:34 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) 
                #10.116.27.1 Up
                second_split = first_split[1].split(" ")
                #RESULT:
                #10.116.27.1
                #Up
                neighbor_IP = second_split[0].strip()
                #print(neighbor_IP)
                state = second_split[1].strip()
                #print (neighbor_IP)
                #print (state)
                #if the state is not Up, look for the connection in the device
                #if it exists, then if the state is the same, send no notification
                #if the state is NOT the same, send a notification
                guard = False

                #keep track of the initial state, if it ends up not changing
                #(in the last log entry referring to it), do not send the notification
                initial_state = state

                #print(json_devices[device_position]["connections"])
                if state != "Up":
                    #print("in")
                    #print(guard)
                    #if the connections list is not empty, look through it and find the connection
                    #if network_devices_list[device_position].connections:
                    # print(json_devices[device_position])
                    # print(json_devices[device_position]["connections"])
                    if json_devices[device_position]["connections"]:
                        for network_connection in json_devices[device_position]["connections"]:
                            #if the state is the same as the initial, break
                            if network_connection["type"] == "bgp" and network_connection["neighbor_IP"] == neighbor_IP and network_connection["state"] == state:
                                #print("in")
                                guard = True
                                break
                            #else, if the connection and neighboring IP are the same, change the state
                            elif network_connection["type"] == "bgp" and network_connection["neighbor_IP"] == neighbor_IP and network_connection["state"] != state:
                                #print("in")
                                guard = True
                                network_connection["state"] = state
                        #print (guard)
                        #if the connection was not found, but the state is down; add the connection to the device and change the changed_state var
                        if guard == False:
                            #print("in if")
                            #print (neighbor_IP)
                            #print (state)
                            new_connection = dict()
                            new_connection["type"] = "bgp"
                            new_connection["neighbor_IP"] = neighbor_IP
                            new_connection["state"] = state
                            #print ("test")
                            network_connection.append(new_connection)
                    #else, if the connections list is empty, simply add the element
                    else:
                        #print("in else")
                        #print (neighbor_IP)
                        #print (state)
                        new_connection = dict()
                        new_connection["type"] = "bgp"
                        new_connection["neighbor_IP"] = neighbor_IP
                        new_connection["state"] = state
                        #print ("test")
                        json_devices[device_position]["connections"].append(new_connection)
                            
                            
                #if state is Up, search for the connection, if it was down, update it and send notification
                else:
                    #print("else")
                    for network_connection in network_devices_list[device_position]["connections"]:
                        if network_connection["type"] == "bgp" and network_connection["neighbor_IP"] == neighbor_IP and network_connection["state"] != state:
                            #print("in")
                            network_connection["state"] = state
                    

        except:
            pass


f.close()

#SEND NOTIFICATIONS FOR ALL connections and interfaces WITH changed_state == True



#SEND NOTIFICATIONS END

#BLOCK 2 - END

# After everything is done
# Writing file in .json format
# DEPLOYMENT
#with open("write_test_json.json", "w") as outfile:
# with open("write_test_json.json", "w") as outfile:
#     json.dump(json_devices, outfile)
#     #outfile.write(json_devices)

with open('network_devices.json', 'w', encoding='utf-8') as f:
    json.dump(json_devices, f, ensure_ascii=False, indent=4)