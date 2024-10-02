

class network_device(object):

    #name of the device
    #name = "No_Name"
    
    
    def __init__(self, name):
        self.name = name
        self.network_interfaces = []
        self.connections = []


class network_interface(object):

    def __init__(self):
        #name of the interface
        self.name = "No_Name"

        #state of the interface - "Up" or "Down"
        self.state = "No_State"

        #monitor state changes
        self.changed_state = "False"


class connection(object):

    def __init__(self):
        #type of connection
        self.type = "No_Type"

        #ip of the neighbor
        self.neighbor_IP = "No_IP"

        #state of connection
        self.state = "No_State"

        #monitor state changes
        self.changed_state = "False"
