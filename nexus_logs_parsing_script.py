
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
    f = open(file, "r")
    lines = f.readlines()

    for line in lines:

        try:
            if "ADJCHANGE" in line:
                #2024 Sep 19 14:11:23 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) neighbor 10.116.27.1 Down - recv:  other configuration change
                #2024 Sep 19 14:11:34 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) neighbor 10.116.27.1 Up
                #2024 Sep 23 13:44:21 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) neighbor 10.116.27.1 Down - recv:  session closed
                #2024 Sep 23 13:44:38 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) neighbor 10.116.27.1 Up
                first_split = line.split("neighbor ")
                #RESULT:
                #2024 Sep 19 14:11:34 VOLTON-SW-CORE-25G-202 %BGP-5-ADJCHANGE:  bgp- [25132] (ISP_SERV) neighbor 
                #10.116.27.1 Up
                second_slpit = line.split(" ")
                #RESULT:
                #10.116.27.1
                #Up


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
