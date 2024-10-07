
import re

from send_notification import send_email_aggregate

f = open("script_parameters.txt", "r")

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

counter = 0

for file in log_file_names_list:


    #open the log files one by one
    #approaching from a per device basis
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

    #write the device name to the .txt file
    #overwrite if this is the old report
    #append if it is the same and we are just adding devices
    if counter == 0:
        f1 = open ("./aggregate_report.txt", "w")
    else:
        f1 = open ("./aggregate_report.txt", "a")
    f1.write("------------------------------------\n")
    f1.write(device_name)
    f1.write("\n")
    f1.write("------------------------------------\n")

    for line in lines:
        if re.search("Down", line) or re.search("DOWN", line):
            f1.write(line)
            f1.write("\n")

    counter = counter + 1
    f1.close()

send_email_aggregate("Aggregate Network Status Report", "Aggregate Report")
