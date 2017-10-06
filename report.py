from extras import utils
from extras.Type import Type


def write_file(string, file):
    new_string = string + "\n"
    file.write(new_string)


def create_report(store, host_name, file):
    print_headings(host_name, file)

    compare_service_configs(store.serviceConfigs, file)
    compare_role_configs(store.roleConfigGroups, file)

    write_file("----------------", file)
    write_file("REPORT COMPLETED", file)


def compare_service_configs(service_configs, file):
    for service_conf in service_configs:
        write_file(
            "Comparing service level configurations for the service: " + service_conf.serviceType + " and config value: " + service_conf.configKey,
            file)
        write_file(service_conf.output(), file)
        if service_conf.clusterConfigValue == service_conf.inputConfigValue:
            write_file("Your input and cluster value for this config are the same, you're good to go, LEVEL:GREEN",
                       file)
            write_file("***** \n", file)
        else:
            compare_values(service_conf.configKey, service_conf.clusterConfigValue, service_conf.inputConfigValue, file)


def compare_role_configs(role_configs, file):
    for role_conf in role_configs:
        write_file(
            "Comparing service level configurations for the service: " + role_conf.serviceType + ", the role: " + role_conf.roleType + " and config value: " + role_conf.roleConfigKey,
            file)
        write_file(role_conf.output(), file)
        if role_conf.clusterRoleConfigValue == role_conf.inputRoleConfigValue:
            write_file("Your input and cluster value for this config are the same, you're good to go, LEVEL:GREEN",
                       file)
            write_file("***** \n", file)
        else:
            compare_values(role_conf.roleConfigKey, role_conf.clusterRoleConfigValue, role_conf.inputRoleConfigValue,
                           file)


def print_headings(host_name, file):
    write_file("---------------------------------------------------------------------", file)
    write_file("Cluster Differentiator Report:", file)
    write_file("Hostname: " + host_name, file)
    write_file("---------------------------------------------------------------------", file)
    write_file("Levels of urgency:", file)
    write_file("RED: Urgent, should look at this right away", file)
    write_file("YELLOW: Should at look at this soon, usually won't hurt your cluster", file)
    write_file("GREEN: You're good", file)
    write_file("BLUE: Could be bad, could be good, the world may never know...", file)
    write_file("--------------------------------------------------------------------- \n\n", file)


def compare_values(key, clusterVal, inputVal, file):
    val1_type = utils.get_type(clusterVal)
    # print val1_type
    val2_type = utils.get_type(inputVal)
    # print val2_type

    if val1_type == val2_type:
        if val1_type == Type.JSON:
            write_file("Your threshold values seem to be off, LEVEL:YELLOW", file)
        elif val1_type == Type.INT:
            if "port" in key:
                write_file("The port in: " + key + "is different, LEVEL:YELLOW", file)
            elif "id" in key:
                write_file("The id of: " + key + " is different, LEVEL:YELLOW", file)
            elif "memory" in key:
                if int(clusterVal) < int(inputVal):
                    write_file("Your " + key + " may be too low, LEVEL:RED", file)
                else:
                    write_file("Your " + key + " may be too high, LEVEL:RED", file)
            elif "size" in key:
                if int(clusterVal) < int(inputVal):
                    write_file("Your " + key + " may be too low, LEVEL:RED", file)
                else:
                    write_file("Your " + key + " may be too high, LEVEL:RED", file)
            else:
                write_file("The integer values of " + key + " are different, LEVEL:BLUE", file)
        elif val1_type == Type.DIRECTORY:
            write_file("The directory location of: " + key + " are different, LEVEL:RED", file)
        elif val1_type == Type.BOOL:
            write_file("The boolean values of: " + key + " are different, LEVEL:RED", file)
        else:
            write_file("Values of: " + key + "are different - Cannot determine type, LEVEL:BLUE", file)
    else:
        write_file("Oh boy, these values are different, you should look into it, LEVEL:BLUE", file)
    write_file("***** \n", file)
