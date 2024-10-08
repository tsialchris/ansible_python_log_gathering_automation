
def parse_parameters(filename):

    f = open(filename, "r")

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

    return log_file_names_list


def parse_nexus_name(line):
    #get the device's name from the log once
    #2024 Sep 12 17:46:34 VOLTON-SW-CORE-25G-202 %DAEMON-3-SYSTEM_MSG: NTP: Peer 193.93.164.195 is unreachable - ntpd[17871]
    first_split = line.split("%")
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

    return device_name


def device_check(json_devices, device_name):
    #add the device to the list, if it is not already in:
    guard = False
    counter = 0
    for device in json_devices:
        #print(device)
        if device["name"] == device_name:
            guard = True

    #create a new object and add it to the list if it doesn't exist
    if guard == False:

        new_device = {"name": device_name, "interfaces": [], "connections": []}

        json_devices.append(new_device)

    return json_devices


def device_lookup(json_devices, device_name):
    
    counter = 0

    for device in json_devices:
        if device["name"] == device_name:
            return counter
        counter = counter + 1