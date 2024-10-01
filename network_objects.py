

class network_device(object):

    #name of the device
    #name = "No_Name"
    network_interfaces = []
    connections = []
    
    def __init__(self, name):
        self.name = name


class network_interface(object):

    #name of the interface
    name = "No_Name"

    #state of the interface - "Up" or "Down"
    state = "No_State"


class connection(object):

    #type of connection
    type = "No_Type"

    #ip of the neighbor
    neighbor_IP = "No_IP"

    #state of connection
    state = "No_State"
