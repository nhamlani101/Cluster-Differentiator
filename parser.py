import time

from extras.config_models import *

my_store = Store


def get_name_type_dict(cm_cluster):
    all_services_names = cm_cluster.get_all_services()

    name_type_dict = {}
    for i in all_services_names:
        name_arr = str(i).split(" ")
        name_type_dict[i.type] = name_arr[1]

    return name_type_dict


def get_store(cm_cluster, standard):
    start_time = time.time()
    print "Creating object store..."

    name_to_type = get_name_type_dict(cm_cluster)

    role_config_groups_array = []
    service_configs = []

    for service_name in standard["services"]:
        current_service = cm_cluster.get_service(name_to_type[service_name])
        config_section = current_service.get_config("summary")

        for config_item in config_section[0]:
            standard_config = standard["services"][service_name]["config"]
            if config_item in standard_config:
                service_configs.append(ServiceConfigGroup(service_name,
                                                          name_to_type[service_name],
                                                          config_item,
                                                          config_section[0][config_item],
                                                          standard_config[config_item]
                                                          ))

        role_config_groups = current_service.get_all_role_config_groups()
        for role in role_config_groups:
            input_role_config_group = standard["services"][service_name]["roleConfigGroups"]
            if role.roleType in input_role_config_group:
                file_roles_in_groups = standard["services"][service_name]["roleConfigGroups"][role.roleType]
                for index in file_roles_in_groups:
                    if index in role.get_config():
                        role_config_groups_array.append(RoleConfigGroup(service_name,
                                                                        name_to_type[service_name],
                                                                        role.name,
                                                                        role.roleType,
                                                                        index,
                                                                        role.get_config()[index],
                                                                        file_roles_in_groups[index]))

    my_store = Store
    my_store.roleConfigGroups = role_config_groups_array
    my_store.serviceConfigs = service_configs

    print "Object store creation is complete"
    elapsed_time = time.time() - start_time
    print "Store creation took: " + str(elapsed_time) + " seconds"

    return my_store
