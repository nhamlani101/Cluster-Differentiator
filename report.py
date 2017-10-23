from extras import utils
from extras.Type import Type


def write_file(string, file):
    new_string = string + "\n"
    file.write(new_string)


def print_headings(check_name, ref_name, file):
    write_file("*********************************************************************", file)
    write_file("Cluster Differentiator Report:", file)
    write_file("Cluster to check: " + check_name, file)
    write_file("Reference cluster: " + ref_name, file)
    write_file("---------------------------------------------------------------------", file)
    write_file("Levels of urgency:", file)
    write_file("RED: Urgent, should look at this right away", file)
    write_file("YELLOW: Should at look at this soon, usually won't hurt your cluster", file)
    write_file("GREEN: You're good", file)
    write_file("BLUE: Could be bad, could be good, the world may never know...", file)
    write_file("*********************************************************************\n\n", file)


def compare_values(key, refVal, checkVal, file):
    if (refVal == checkVal):
        write_file("Your input and cluster value for this config are the same, you're good to go, LEVEL:GREEN", file)
        return
    val1_type = utils.get_type(refVal)
    # print val1_type
    val2_type = utils.get_type(checkVal)
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
                if int(refVal) < int(checkVal):
                    write_file("Your " + key + " may be too low, LEVEL:RED", file)
                else:
                    write_file("Your " + key + " may be too high, LEVEL:RED", file)
            elif "size" in key:
                if int(refVal) < int(checkVal):
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


def generate_report(check_cluster, ref_cluster, file, check_name, ref_name):
    print "Creating report..."

    print_headings(check_name, ref_name, file)
    for service_name in ref_cluster.services:
        if service_name in check_cluster.services:
            write_file("Service: " + service_name, file)

            write_file("Comparing service layer configs for " + service_name, file)

            ref_service_configs = ref_cluster.services[service_name].serviceConfigs
            check_service_configs = check_cluster.services[service_name].serviceConfigs

            if ref_service_configs is None:
                write_file(
                    "Reference cluster does not have any service layer configs for the " + service_name + " service, LEVEL:YELLOW",
                    file)
            if check_service_configs is None:
                write_file(
                    "Your cluster does not have any service layer configs for the " + service_name + " service, LEVEL:YELLOW",
                    file)

            if (ref_service_configs is not None) and (check_service_configs is not None):
                for service_model in ref_service_configs:
                    if service_model in check_service_configs:

                        if ("\n" in ref_service_configs[service_model]):
                            write_file(
                                "Reference cluster; Name: " + service_model + ", NOTE: Value of this config is large, please refer to CM",
                                file)
                        else:
                            write_file("Reference cluster; Name: " + service_model + ", Value: " + ref_service_configs[
                                service_model], file)

                        if ("\n" in check_service_configs[service_model]):
                            write_file(
                                "Your cluster; Name: " + service_model + ", NOTE: Value of this config is large, please refer to CM",
                                file)
                        else:
                            write_file("Your cluster; Name: " + service_model + ", Value " + check_service_configs[
                                service_model], file)
                        compare_values(service_model, ref_service_configs[service_model],
                                       check_service_configs[service_model], file)
                        write_file("", file)

                    else:
                        write_file("ERROR: Your cluster does not have the " + service_model + " config", file)

            write_file("Comparing role configs for " + service_name, file)

            ref_role_dict = ref_cluster.services[service_name].roleConfigs
            check_role_dict = check_cluster.services[service_name].roleConfigs
            for role_model in ref_role_dict:
                if role_model in check_role_dict:
                    write_file("Role: " + role_model, file)

                    ref_role_config = ref_role_dict[role_model].roleConfig
                    check_role_config = check_role_dict[role_model].roleConfig

                    if ref_role_config is None:
                        write_file(
                            "Reference cluster does not have any role configs for the " + role_model + " role, LEVEL:YELLOW",
                            file)
                    if check_role_config is None:
                        write_file(
                            "Your cluster does not have any role configs for the " + role_model + " role, LEVEL:YELLOW",
                            file)

                    if (ref_role_config is not None) and (check_role_config is not None):
                        for role_config_item in ref_role_config:
                            if role_config_item in check_role_config:
                                if ("\n" in ref_role_config[role_config_item]):
                                    write_file(
                                        "Reference cluster; Name: " + role_config_item + ", NOTE: Value of this config is large, please refer to CM",
                                        file)
                                else:
                                    write_file(
                                        "Reference cluster; Name: " + role_config_item + ", Value: " + ref_role_config[
                                            role_config_item], file)

                                if ("\n" in check_role_config[role_config_item]):
                                    write_file(
                                        "Your cluster; Name: " + role_config_item + ", NOTE: Value of this config is large, please refer to CM",
                                        file)
                                else:
                                    write_file(
                                        "Your cluster; Name: " + role_config_item + ", Value: " + check_role_config[
                                            role_config_item], file)

                                compare_values(role_config_item, ref_role_config[role_config_item],
                                               check_role_config[role_config_item], file)
                                write_file("", file)
                            else:
                                write_file(
                                    "The role config " + role_config_item + " in the role " + role_model + " is not available on your cluster",
                                    file)
                else:
                    write_file(
                        "The role " + role_model + " in the service " + service_name + " is not available on your cluster",
                        file)
            write_file("", file)
        else:
            write_file(
                "WARNING: The " + service_name + " service is not available in the cluster you are checking, LEVEL:YELLOW",
                file)

        write_file(
            "---------------------------------------------------------------------------------------------------", file)
        write_file("", file)
