
# try to find the token, the type and
def check_line(token, line, device):
    try:
        if token in line:
            # if "bgp" is in line, then it is a connection
            if "bgp" in line:
                type = "bgp"
                network_connection = {}                
                if token == "ADJCHANGE":
                    network_connection["type"] = type
                    # create the connection
                    network_connection = get_connection_data(network_connection, line)
                    # if the "connections" list is not empty
                    if device["connections"]:
                        # look for the connection in the device
                        device["connections"] = connection_lookup(network_connection, device["connections"])
                    # else if the list is empty AND the state is Down, append the connection
                    elif network_connection["state"] == "Down":
                        # previous_state should be the opposite of state, for the notification to be sent later
                        # which is also the truth
                        network_connection["previous_state"] = "Up"
                        device["connections"].append(network_connection)

            # else if something else (other than "bgp") is in the line
            else:
                0==0
    except:
        print("Exception in check_line")
        pass
    
    return device

def get_connection_data(network_connection, line):
    network_connection["state"] = get_connection_state(line)
    network_connection["neighbor_IP"] = get_connection_neighbor_ip(line)
    return network_connection


def get_connection_state(line):
    # return state
    try:
        if "Down" in line:
            return "Down"
        elif "Up" in line:
            return "Up"
    except:
        print("Exception in get_connection_state")
        pass

def get_connection_neighbor_ip(line):
    #to get neighbor_ip just match the pattern of the ip address
    # 2024 Sep 29 23:00:19 VOLTON-SW-CORE-25G-201 %BGP-5-ADJCHANGE:  bgp- [15893] (ISP_SERV) neighbor 10.106.27.1 Down - sent:  other configuration change
    # Oct  7 09:21:00.342: %BGP-5-ADJCHANGE: neighbor 63.130.133.190 vpn vrf GN Down BGP Notification sent
    import re
    ipv4_pattern = r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)'
    match = re.search(ipv4_pattern, line)
    neighbor_IP = match.group(0)
    # print(neighbor_IP)
    return neighbor_IP
    


def connection_lookup(network_connection, connections):
    
    # returns the connections table updated
    for iterated_connection in connections:
        # if the connections is found, update its state
        if iterated_connection["neighbor_IP"] == network_connection["neighbor_IP"]:
            iterated_connection["state"] = network_connection["state"]
            return connections
    
    # if the connection has not been found (meaning "return connections" won't hit)
    # if the state is Down
    # append the connection
    if network_connection["state"] == "Down":
        # previous_state should be the opposite of state, for the notification to be sent later
        # which is also the truth
        network_connection["previous_state"] = "Up"
        connections.append(network_connection)

    return connections

def send_connection_notification(network_connection):
    from send_notification import send_email
    import json
    notification_subject = "Connection State Changed"
    notification_body = json.dumps(network_connection, ensure_ascii=False, indent=4)
    send_email(notification_subject, notification_body)