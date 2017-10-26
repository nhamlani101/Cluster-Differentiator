from extras import utils
from extras.Type import Type
from extras.models import CompOutput


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
        return "Your input and cluster value for this config are the same, you're good to go, LEVEL:GREEN", "green"
    val1_type = utils.get_type(refVal)
    # print val1_type
    val2_type = utils.get_type(checkVal)
    # print val2_type

    if val1_type == val2_type:
        if val1_type == Type.JSON:
            return "Your threshold values seem to be off, LEVEL:YELLOW", "yellow"
        elif val1_type == Type.INT:
            if "port" in key:
                return "The port in: " + key + "is different, LEVEL:YELLOW", "yellow"
            elif "id" in key:
                return "The id of: " + key + " is different, LEVEL:YELLOW", "yellow"
            elif "memory" in key:
                if int(refVal) < int(checkVal):
                    return"Your " + key + " may be too low, LEVEL:RED", "red"
                else:
                    return "Your " + key + " may be too high, LEVEL:RED", "red"
            elif "size" in key:
                if int(refVal) < int(checkVal):
                    return"Your " + key + " may be too low, LEVEL:RED", "red"
                else:
                    return"Your " + key + " may be too high, LEVEL:RED", "red"
            else:
                return "The integer values of " + key + " are different, LEVEL:BLUE", "blue"
        elif val1_type == Type.DIRECTORY:
            return "The directory location of: " + key + " are different, LEVEL:RED", "red"
        elif val1_type == Type.BOOL:
            return "The boolean values of: " + key + " are different, LEVEL:RED", "red"
        else:
            return "Values of: " + key + "are different - Cannot determine type, LEVEL:BLUE", "blue"
    else:
        return "Oh boy, these values are different, you should look into it, LEVEL:BLUE", "blue"

def generate_report_file(check_cluster, ref_cluster, file, check_name, ref_name):
    print "Creating report..."

    output_list = []

    print_headings(check_name, ref_name, file)
    for service_name in ref_cluster.services:
        if service_name in check_cluster.services:
            service_heading_output = CompOutput("s_heading")
            service_heading_output.service = service_name
            output_list.append(service_heading_output)

            write_file("Service: " + service_name, file)
            write_file("Comparing service layer configs for " + service_name, file)

            ref_service_configs = ref_cluster.services[service_name].serviceConfigs
            check_service_configs = check_cluster.services[service_name].serviceConfigs

            no_s_config = CompOutput("no_s_config")
            if ref_service_configs is None:
                write_file(
                    "Reference cluster does not have any service layer configs for the " + service_name + " service, LEVEL:YELLOW",
                    file)
                no_s_config.refVal = "Reference cluster does not have any service layer configs for the " + service_name + " service"
            if check_service_configs is None:
                write_file(
                    "Your cluster does not have any service layer configs for the " + service_name + " service, LEVEL:YELLOW",
                    file)
                no_s_config.checkVal = "Your cluster does not have any service layer configs for the " + service_name + " service"
            no_s_config.level = "yellow"
            no_s_config.key = service_name

            if (no_s_config.refVal != None) or (no_s_config.checkVal != None):
                output_list.append(no_s_config)

            if (ref_service_configs is not None) and (check_service_configs is not None):
                for service_model in ref_service_configs:
                    service_output = CompOutput("s_config")
                    if service_model in check_service_configs:
                        service_output.service = service_name
                        if ("\n" in ref_service_configs[service_model]):
                            write_file(
                                "Reference cluster; Name: " + service_model + ", NOTE: Value of this config is large, please refer to CM",
                                file)
                            service_output.refVal = "NOTE: Value of this config is large, please refer to CM"
                            service_output.key = service_model
                        else:
                            write_file("Reference cluster; Name: " + service_model + ", Value: " + ref_service_configs[
                                service_model], file)
                            service_output.refVal = ref_service_configs[service_model]
                            service_output.key = service_model


                        if ("\n" in check_service_configs[service_model]):
                            write_file(
                                "Your cluster; Name: " + service_model + ", NOTE: Value of this config is large, please refer to CM",
                                file)
                            service_output.checkVal =  "NOTE: Value of this config is large, please refer to CM"
                            service_output.key = service_model
                        else:
                            write_file("Your cluster; Name: " + service_model + ", Value " + check_service_configs[
                                service_model], file)
                            service_output.checkVal = check_service_configs[service_model]
                            service_output.key = service_model

                        sentence, level = compare_values(service_model, ref_service_configs[service_model],
                                       check_service_configs[service_model], file)
                        write_file(sentence, file)
                        service_output.level = level
                        write_file("", file)

                    else:
                        write_file("ERROR: Your cluster does not have the " + service_model + " config", file)
                        service_output.key = service_model
                        service_output.error = "ERROR: Your cluster does not have the " + service_model + " config"
                        service_output.level = "red"

                    output_list.append(service_output)

            write_file("Comparing role configs for " + service_name, file)

            ref_role_dict = ref_cluster.services[service_name].roleConfigs
            check_role_dict = check_cluster.services[service_name].roleConfigs
            for role_model in ref_role_dict:
                if role_model in check_role_dict:
                    write_file("Role: " + role_model, file)
                    role_heading = CompOutput("r_heading")
                    role_heading.role = role_model
                    output_list.append(role_heading)

                    ref_role_config = ref_role_dict[role_model].roleConfig
                    check_role_config = check_role_dict[role_model].roleConfig

                    no_r_config = CompOutput("no_r_config")
                    if ref_role_config is None:
                        write_file(
                            "Reference cluster does not have any role configs for the " + role_model + " role, LEVEL:YELLOW",
                            file)
                        no_r_config.refVal = "Reference cluster does not have any role configs for the " + role_model + " role"
                    if check_role_config is None:
                        write_file(
                            "Your cluster does not have any role configs for the " + role_model + " role, LEVEL:YELLOW",
                            file)
                        no_r_config.checkVal = "Your cluster does not have any role configs for the " + role_model + " role"

                    no_r_config.level = "yellow"
                    no_r_config.key = role_model

                    if (no_r_config.refVal != None) or (no_r_config.checkVal != None):
                        output_list.append(no_r_config)

                    if (ref_role_config is not None) and (check_role_config is not None):
                        for role_config_item in ref_role_config:
                            role_output = CompOutput("r_config")
                            if role_config_item in check_role_config:
                                if ("\n" in ref_role_config[role_config_item]):
                                    write_file(
                                        "Reference cluster; Name: " + role_config_item + ", NOTE: Value of this config is large, please refer to CM",
                                        file)
                                    role_output.checkVal = "NOTE: Value of this config is large, please refer to CM"
                                    role_output.key = role_config_item

                                else:
                                    write_file(
                                        "Reference cluster; Name: " + role_config_item + ", Value: " + ref_role_config[
                                            role_config_item], file)
                                    role_output.checkVal = ref_role_config[role_config_item]
                                    role_output.key = role_config_item

                                if ("\n" in check_role_config[role_config_item]):
                                    write_file(
                                        "Your cluster; Name: " + role_config_item + ", NOTE: Value of this config is large, please refer to CM",
                                        file)
                                    role_output.refVal = "NOTE: Value of this config is large, please refer to CM"
                                    role_output.key = role_config_item
                                else:
                                    write_file(
                                        "Your cluster; Name: " + role_config_item + ", Value: " + check_role_config[
                                            role_config_item], file)
                                    role_output.refVal = check_role_config[role_config_item]
                                    role_output.key = role_config_item

                                r_sentence, r_level = compare_values(role_config_item, ref_role_config[role_config_item],
                                               check_role_config[role_config_item], file)
                                write_file(r_sentence, file)
                                write_file("", file)
                                role_output.level = r_level
                            else:
                                write_file(
                                    "The role config " + role_config_item + " in the role " + role_model + " is not available on your cluster",
                                    file)
                                role_output.error = "The role config " + role_config_item + " in the role " + role_model + " is not available on your cluster"
                                role_output.key = role_config_item
                                role_output.level = "red"
                            output_list.append(role_output)

                else:
                    write_file(
                        "The role " + role_model + " in the service " + service_name + " is not available on your cluster",
                        file)
                    no_role = CompOutput("no_role")
                    no_role.level = "yellow"
                    no_role.key = role_model
                    no_role.error = "The role " + role_model + " in the service " + service_name + " is not available on your cluster"
                    output_list.append(no_role)

            write_file("", file)
        else:
            write_file(
                "WARNING: The " + service_name + " service is not available in the cluster you are checking, LEVEL:YELLOW",
                file)
            no_service = CompOutput("no_service")
            no_service.level = "red"
            no_service.key = service_name
            no_service.error = "WARNING: The " + service_name + " service is not available in the cluster you are checking, LEVEL:YELLOW"
            output_list.append(no_service)


        write_file(
            "---------------------------------------------------------------------------------------------------", file)
        write_file("", file)

    return output_list

#
#
# def compare_values_html(key, refVal, checkVal, file):
#     if (refVal == checkVal):
#         yield "Your input and cluster value for this config are the same, you're good to go, LEVEL:GREEN"
#         return
#     val1_type = utils.get_type(refVal)
#     # print val1_type
#     val2_type = utils.get_type(checkVal)
#     # print val2_type
#
#     if val1_type == val2_type:
#         if val1_type == Type.JSON:
#             yield "Your threshold values seem to be off, LEVEL:YELLOW"
#         elif val1_type == Type.INT:
#             if "port" in key:
#                 yield "The port in: " + key + "is different, LEVEL:YELLOW"
#             elif "id" in key:
#                 yield "The id of: " + key + " is different, LEVEL:YELLOW"
#             elif "memory" in key:
#                 if int(refVal) < int(checkVal):
#                     yield "Your " + key + " may be too low, LEVEL:RED"
#                 else:
#                     yield "Your " + key + " may be too high, LEVEL:RED"
#             elif "size" in key:
#                 if int(refVal) < int(checkVal):
#                     yield "Your " + key + " may be too low, LEVEL:RED"
#                 else:
#                     yield "Your " + key + " may be too high, LEVEL:RED"
#             else:
#                 yield "The integer values of " + key + " are different, LEVEL:BLUE"
#         elif val1_type == Type.DIRECTORY:
#             yield "The directory location of: " + key + " are different, LEVEL:RED"
#         elif val1_type == Type.BOOL:
#             yield "The boolean values of: " + key + " are different, LEVEL:RED"
#         else:
#             yield "Values of: " + key + "are different - Cannot determine type, LEVEL:BLUE"
#     else:
#         yield "Oh boy, these values are different, you should look into it, LEVEL:BLUE"
#
# def generate_report_html(check_cluster, ref_cluster, file, check_name, ref_name):
#     print "Creating report..."
#
#     print_headings(check_name, ref_name, file)
#     for service_name in ref_cluster.services:
#         if service_name in check_cluster.services:
#             yield "Service: " + service_name
#
#             yield "Comparing service layer configs for " + service_name
#
#             ref_service_configs = ref_cluster.services[service_name].serviceConfigs
#             check_service_configs = check_cluster.services[service_name].serviceConfigs
#
#             if ref_service_configs is None:
#                 yield "Reference cluster does not have any service layer configs for the " + service_name + " service, LEVEL:YELLOW"
#             if check_service_configs is None:
#                 yield "Your cluster does not have any service layer configs for the " + service_name + " service, LEVEL:YELLOW"
#
#             if (ref_service_configs is not None) and (check_service_configs is not None):
#                 for service_model in ref_service_configs:
#                     if service_model in check_service_configs:
#
#                         if ("\n" in ref_service_configs[service_model]):
#                             yield "Reference cluster; Name: " + service_model + ", NOTE: Value of this config is large, please refer to CM"
#                         else:
#                             yield "Reference cluster; Name: " + service_model + ", Value: " + ref_service_configs[
#                                 service_model]
#
#                         if ("\n" in check_service_configs[service_model]):
#                             yield "Your cluster; Name: " + service_model + ", NOTE: Value of this config is large, please refer to CM"
#                         else:
#                             yield "Your cluster; Name: " + service_model + ", Value " + check_service_configs[
#                                 service_model]
#
#                         compare_values_html(service_model, ref_service_configs[service_model],
#                                        check_service_configs[service_model], file)
#                         yield ""
#
#                     else:
#                         yield "ERROR: Your cluster does not have the " + service_model + " config", file
#
#             yield "Comparing role configs for " + service_name
#
#             ref_role_dict = ref_cluster.services[service_name].roleConfigs
#             check_role_dict = check_cluster.services[service_name].roleConfigs
#             for role_model in ref_role_dict:
#                 if role_model in check_role_dict:
#                     yield "Role: " + role_model
#
#                     ref_role_config = ref_role_dict[role_model].roleConfig
#                     check_role_config = check_role_dict[role_model].roleConfig
#
#                     if ref_role_config is None:
#                         yield "Reference cluster does not have any role configs for the " + role_model + " role, LEVEL:YELLOW"
#                     if check_role_config is None:
#                         yield "Your cluster does not have any role configs for the " + role_model + " role, LEVEL:YELLOW"
#
#                     if (ref_role_config is not None) and (check_role_config is not None):
#                         for role_config_item in ref_role_config:
#                             if role_config_item in check_role_config:
#                                 if ("\n" in ref_role_config[role_config_item]):
#                                     yield "Reference cluster; Name: " + role_config_item + ", NOTE: Value of this config is large, please refer to CM",
#                                 else:
#                                     yield "Reference cluster; Name: " + role_config_item + ", Value: " + ref_role_config[
#                                             role_config_item]
#
#                                 if ("\n" in check_role_config[role_config_item]):
#                                     yield "Your cluster; Name: " + role_config_item + ", NOTE: Value of this config is large, please refer to CM"
#                                 else:
#                                     yield "Your cluster; Name: " + role_config_item + ", Value: " + check_role_config[
#                                             role_config_item]
#
#                                 compare_values_html(role_config_item, ref_role_config[role_config_item],
#                                                check_role_config[role_config_item], file)
#                                 yield ""
#                             else:
#                                 yield "The role config " + role_config_item + " in the role " + role_model + " is not available on your cluster"
#                 else:
#                     yield "The role " + role_model + " in the service " + service_name + " is not available on your cluster"
#             yield ""
#         else:
#             yield "WARNING: The " + service_name + " service is not available in the cluster you are checking, LEVEL:YELLOW"
#
#         yield "---------------------------------------------------------------------------------------------------"
#         yield ""
