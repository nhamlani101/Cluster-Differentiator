class ClusterModel:
    def __init__(self):
        # Dictionary of serviceName -> ServiceModel Object
        self.services = {}

class ServiceModel:
    def __init__(self):
        # Dictionary of serviceConfig name -> serviceConfig value
        self.serviceConfigs = {}
        self.serviceType = None
        # Dictionary of roleType name -> RoleConfigModel object
        self.roleConfigs = {}

class RoleConfigModel:
    def __init__(self):
        self.roleType = None
        # Dictionary
        self.roleConfig = {}
