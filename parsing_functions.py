
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