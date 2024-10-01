
import os

from network_objects import network_device
from network_objects import network_interface
from network_objects import connection

#list with all network devices with logs
#will contain network_device objects
network_devices_list = []

#parse the script_parameters.txt
#DEPLOYMENT
f = open(r"C:\Users\c.tsialamanis\Desktop\ansible-logs-python\script_parameters.txt", "r")
#f = open("script_parameters.txt", "r")

#read all the lines and store them in "lines"
lines = f.readlines()

#store all the log file names in an array
log_file_names_list = [] = False

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

#if the network_devices.txt file exists, parse it to get info
#DEPLOYMENT
#if os.path.isfile("./network_devices.txt"):
if True:
    #control variables for network_devices.txt parsing
    network_devices_found = False
    device_found = False
    interfaces_found = False
    connections_found = False
    #get device objects from the network_devices.txt file
    #DEPLOYMENT
    f = open(r"C:\Users\c.tsialamanis\Desktop\ansible-logs-python\network_devices.txt", "r")
    #f = open("network_devices.txt", "r")
    lines = f.readlines()
    for line in lines:


        if line.strip() == "}NETWORK_DEVICES":
            network_devices_found = False
            break
        
        elif line.strip() == "}DEVICE":
            device_found = False
        
        elif line.strip() == "}CONNECTIONS":
            connections_found = False

        elif line.strip() == "}INTERFACES":
            interfaces_found = False

        #Get Connection Data
        if network_devices_found and device_found and interfaces_found == False and connections_found:
            try:
                #Type=BGP
                first_split = line.split("=")
                #print(first_split[1])
                #if the Type is found
                if first_split[0].strip() == "Type":
                    for device in network_devices_list:
                        if device.name == temp_device_name:
                            #store the connection's type temporarily for checks State
                            temp_connection_type = first_split[1].strip()
                            new_connection = connection()
                            new_connection.type = first_split[1].strip()
                            device.connections.append(new_connection)
                #else, if the Neighbor_IP is found
                elif first_split[0].strip() == "Neighbor_IP":
                    for device in network_devices_list:
                        if device.name == temp_device_name:
                            #store the Neighbor's ip temporarily for checks in State
                            temp_neighbor_IP = first_split[1].strip()
                            #find the connection with no neighbor ip added (meaning it's new)
                            #and add this neighbor ip
                            for network_connection in device.connections:
                                #if type is correct and neighbor ip is not provided
                                if network_connection.type == temp_connection_type and network_connection.neighbor_IP == "No_IP":
                                    network_connection.neighbor_IP = first_split[1].strip()
                #else if the State is found
                elif first_split[0].strip() == "State":
                    for device in network_devices_list:
                        if device.name == temp_device_name:
                            for network_connection in device.connections:                                
                                if network_connection.type == temp_connection_type and network_connection.neighbor_IP == temp_neighbor_IP:
                                    network_connection.state == first_split[1].strip()
            except:
                pass

        #Get Interface Data
        elif network_devices_found and device_found and interfaces_found and connections_found == False:
            try:
                #Name=Interface_1
                first_split = line.split("=")
                #RESULT:
                #Name
                #Interface_1
                #if the Name is found, create the interface and assign it to the correct device
                if first_split[0].strip() == "Name":
                    #find the associated device based on its name
                    for device in network_devices_list:
                        if device.name == temp_device_name:
                            #store the interface's name temporarily for use in State Check
                            temp_interface_name = first_split[1].strip()
                            #create new network interface object
                            new_network_interface = network_interface()
                            #assign the name to the interface
                            new_network_interface.name = first_split[1].strip()
                            #append it to the device's list
                            device.network_interfaces.append(new_network_interface)
                
                #else, if the State is found
                #State=Down
                elif first_split[0].strip() == "State":
                    for device in network_devices_list:
                        if device.name == temp_device_name:

                            #assign the state to the correct interface
                            for interface in device.network_interfaces:
                                if interface.name == temp_interface_name:
                                    interface.state = first_split[1].strip()

            except:
                pass

        #Get Device Name
        elif network_devices_found and device_found and interfaces_found == False and connections_found == False:
            try:
                #Name=VOLTON-SW-CORE-25G-202
                first_split = line.split("=")
                if first_split[0].strip() == "Name":
                    #store the device name temporarily to use within the loop, to associate
                    #the connections and interfaces with the correct device
                    temp_device_name = first_split[1].strip()
                    #if the network device does not already exist, only then add it
                    guard = False
                    for device in network_devices_list:
                        if device.name == first_split[1].strip():
                            guard = True
                    if guard == False:
                        new_network_device = network_device(first_split[1].strip())
                        network_devices_list.append(new_network_device)
            except:
                pass
        

        if line.strip() == "INTERFACES{":
            interfaces_found = True

        elif line.strip() == "CONNECTIONS{":
            connections_found = True

        elif line.strip() == "DEVICE{":
            device_found = True

        elif line.strip() == "NETWORK_DEVICES{":
            network_devices_found = True
        


    f.close()

#BLOCK 1 - END

#go through each log file:
#BLOCK 2

for file in log_file_names_list:


    #open the log files one by one
    #approaching from a per device basis
    #DEPLOYMENT
    f = open 
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
    device_name = second_slpit[3]

    #add the device to the list, if it is not already in:
    guard = False
    counter = 0
    for device in network_devices_list:
        if device.name == device_name:
            guard = True
            #store the device's position to avoid going through the list every time
            device_position = counter
        counter = counter + 1
    #create a new object and add it to the list if it doesn't exist
    if guard == False:
        new_network_device = network_device(device_name)
        network_devices_list.append(new_network_device)
        device_position = len(network_devices_list) - 1

    for line in lines:

        try:
            #check for BGP Adjacency Changes
            if "ADJCHANGE" in line:
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
                state = second_split[1].strip()
                #if the state is not Up, look for the connection in the device
                #if it exists, then if the state is the same, send no notification
                #if the state is NOT the same, send a notification
                guard = False
                if state != "Up":
                    for network_connection in network_devices_list[device_position].connections:
                        if network_connection.type == "bgp" and network_connection.neighbor_IP == neighbor_IP and network_connection.state == state:
                            guard = True
                            break
                        #else, if the connection and neighboring IP are the same, change the state and send notification
                        elif network_connection.type == "bgp" and network_connection.neighbor_IP == neighbor_IP and network_connection.state != state:
                            guard = True
                            network_connection.state = state
                            #send notification#
                            #---notification---#
                            #send notification#

                #if the connection was not found, add the connection to the device and send notification:
                if guard == False:
                    new_connection = connection()
                    new_connection.type = "bgp"
                    new_connection.neighbor_IP = neighbor_IP
                    new_connection.state = state
                    network_devices_list[device_position].connections.append()
                    #send notification#
                    #---notification---#
                    #send notification#

                    

        except:
            pass


#BLOCK 2 - END

#after everything is done
#write the network_devices.txt

#DEPLOYMENT
f = open(r"C:\Users\c.tsialamanis\Desktop\ansible-logs-python\write_test.txt", "w")
#f = open("network_devices.txt", "w")

f.write("NETWORK_DEVICES{\n")

for device in network_devices_list:
    f.write("\tDEVICE{\n")
    f.write("\t\t" + str(device.name) + "\n")
    #if the network_interfaces list for this device is not empty
    if device.network_interfaces:
        f.write("\t\tINTERFACES{\n")
        for interface in device.network_interfaces:
            f.write("\t\t\tName=" + str(interface.name) + "\n")
            f.write("\t\t\tState=" + str(interface.state) + "\n")

        f.write("\t\t}INTERFACES\n")

    #if the connections list for this device is not empty
    if device.connections:
        f.write("\t\tCONNECTIONS{\n")
        for network_connection in device.connections:
            f.write("\t\t\tType=" + str(network_connection.type) + "\n")
            f.write("\t\t\tNeighbor_IP=" + str(network_connection.neighbor_IP) + "\n")
            f.write("\t\t\tState=" + str(network_connection.state) + "\n")

        f.write("\t\t}CONNECTIONS\n")

    f.write("\t}DEVICE\n")

f.write("}NETWORK_DEVICES")
