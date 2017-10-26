from extras.models import *

def parse_cluster(cluster):

    theCluster = ClusterModel()
    try:
        for service in cluster['services']:
            current_service = ServiceModel()
            service_name = service['serviceType']

            serviceConfigs = {}
            try:
                for service_config in service['serviceConfigs']:
                    try:
                        value = service_config['value']
                    except:
                        try:
                            value = service_config['variable']
                        except:
                            try:
                                value = service_config['ref']
                            except:
                                print "ERRORRRRRRR"
                                continue
                    serviceConfigs[service_config['name']] = value
            except:
                serviceConfigs = None
                # print "The service " + service_name + " does not have service layer configs"

            current_service.serviceType = service_name
            current_service.serviceConfigs = serviceConfigs

            for role in service['roleConfigGroups']:
                current_role = RoleConfigModel()
                role_name = role['roleType']

                roleConfigs = {}
                try:
                    for config_item in role['configs']:
                        try:
                            value = config_item['value']
                        except:
                            try:
                                value = config_item['variable']
                            except:
                                try:
                                    value = config_item['ref']
                                except:
                                    print "ERRORRRRRRR"
                                    continue

                        roleConfigs[config_item['name']] = value
                except:
                    roleConfigs = None
                    # print "The role " + role['roleType'] + " of service " + service_name + " does not have a config"

                current_role.roleType = role_name
                current_role.roleConfig = roleConfigs
                current_service.roleConfigs[role_name] = current_role

            theCluster.services[service_name] = current_service
    except:
        print "This cluster does not any services configured, there is nothing to look at here"
        exit(1)
    return theCluster