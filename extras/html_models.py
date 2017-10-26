class ClusterService():
    def __init__(self):
        self.serviceConfList = []
        self.roleConfList = []
class RoleConfigGroup():
    def __init__(self, _serviceType, _serviceName, _roleName, _roleType, _roleConfigKey,
                 _clusterRCV, _inputRCV):
        self.serviceName = _serviceName
        self.serviceType = _serviceType
        self.roleName = _roleName
        self.roleType = _roleType
        self.roleConfigKey = _roleConfigKey
        self.clusterRoleConfigValue = _clusterRCV
        self.inputRoleConfigValue = _inputRCV

    def __str__(self):
        ret_string = "ROLE CONFIG \n" + "Service Type: " + self.serviceType + " Role Type: " + self.roleType + " Config Key: " + self.roleConfigKey + " Cluster config: " + self.clusterRoleConfigValue + " Input config: " + self.inputRoleConfigValue
        return ret_string


class ServiceConfigGroup():
    def __init__(self, _serviceType, _serviceName, _configKey, _clusterConfigValue,
                 _inputConfigValue):
        self.serviceType = _serviceType
        self.serviceName = _serviceName
        self.configKey = _configKey
        self.clusterConfigValue = _clusterConfigValue
        self.inputConfigValue = _inputConfigValue

    def __str__(self):
        return "SERVICE CONFIG \n" + "Service Type: " + self.serviceType + "; Config Key: " + self.configKey + "; Cluster config: " + self.clusterConfigValue + "; Input config: " + self.inputConfigValue
